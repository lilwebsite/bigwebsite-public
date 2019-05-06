import os
import sys
import transaction
import pdb

from pyramid.paster import (
	get_appsettings,
	setup_logging
)
from pyramid.scripts.common import parse_vars
from ..meta import Base

from sqlalchemy import engine_from_config
from ..models import (
	dbsession,
	User,
	Art,
	AdminPage
)

def usage(argv):
	cmd = os.path.basename(argv[0])
	print('usage: %s <config_uri> [var=value]\n'
		'(example: "%s development.ini")' % (cmd, cmd))
	sys.exit(1)

def main(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)

	config_uri = argv[1]
	#options = parse_vars(argv[2:])
	setup_logging(config_uri)
	#settings = get_appsettings(config_uri, options=options)
	settings = get_appsettings(config_uri)
	engine = engine_from_config(settings, 'sqlalchemy.')
	dbsession.configure(bind=engine)
	Base.metadata.create_all(engine)
	#session_factory = get_session_factory(engine)

	with transaction.manager:
		#dbsession = get_tm_session(session_factory, transaction.manager)
		while True:
			admin = User(
				username=input('first time username: '),
				permission=int(input('permission(0/1): '))
			)
			admin.create_user(input('first time password: '))
			dbsession.add(admin)
			if input('create another user? y/n\n') != 'y':
				break;

		#testimg = Art(
		#	name='testimg1.jpg',
		#	uploadtime='2018-06-09 20:56:38.893657',
		#	cached=False
		#)
		adminpage = AdminPage(
			unsorted=False
		)

		dbsession.add(adminpage)
		dbsession.add(admin)
