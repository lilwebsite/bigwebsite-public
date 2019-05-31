from pyramid.session import (
	SignedCookieSessionFactory,
	JSONSerializer
)
from pyramid.config import Configurator
from pyramid.response import Response

from sqlalchemy import engine_from_config

from .meta import (
	dbsession, 
	Base
)

from .elements.status import response_status

from pyramid.renderers import JSON

resp_status = response_status()

def forbidden(request, status=403):
	response = resp_status.error(0)
	response.status = status
	return response

def main(global_config, test_settings=None, **settings):
	if test_settings is None:
		engine = engine_from_config(settings, 'sqlalchemy.')
		dbsession.configure(bind=engine)
		Base.metadata.bind = engine
		config = Configurator(settings=settings)
		session_factory = SignedCookieSessionFactory(
			secret=settings['session.secret'],
			domain=settings['hostname'],
			secure=True,
			httponly=True,
			samesite='strict',
			reissue_time=900,
			max_age=900,
			serializer=JSONSerializer()
		)
	else:
		engine = engine_from_config(test_settings, 'sqlalchemy.')
		dbsession.configure(bind=engine)
		Base.metadata.bind = engine
		config = Configurator(settings=test_settings)
		session_factory = SignedCookieSessionFactory(
			secret=test_settings['session.secret'],
			domain=test_settings['hostname'],
			secure=True,
			httponly=True,
			samesite='strict',
			reissue_time=900,
			max_age=900,
			serializer=JSONSerializer()
		)

	config.add_renderer('json', JSON(indent=4))

	config.set_session_factory(session_factory)
	config.add_forbidden_view(forbidden)
	config.include('pyramid_jinja2')

	def page_controller(page):
		if page == 'adminpage':
			return True
		if page == 'login':
			return False
		return False

	def check_sort(unsorted):
		return unsorted
	
	def img(imgtype):
		if imgtype == 'img':
			return True
		return False

	def pdf(imgtype):
		if imgtype == 'pdf':
			return True
		return False
	
	def setup_jinja2_env():
		jinja_environment = config.get_jinja2_environment()
		tests = {
			'page_controller': page_controller,
			'check_sort': check_sort,
			'img': img,
			'pdf': pdf
		}
		for key,val in tests.items():
			jinja_environment.tests[key] = val

	config.action(None, setup_jinja2_env, order=999)

	config.include('.models')
	config.include('.routes')
	config.include('.security')
	config.scan('bigwebsite')

	return config.make_wsgi_app()
