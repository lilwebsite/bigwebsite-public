from bigwebsite.include.meta import *

CONVENTION = {
	'ix': 'ix_%(column_0_label)s',
	'uq': 'uq_%(table_name)s_%(column_0_name)s',
	'ck': 'ck_%(table_name)s_%(constraint_name)s',
	'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
	'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=CONVENTION)

dbsession = scoped_session(
	sessionmaker(extension=ZopeTransactionExtension())
)
#dbsession = sessionmaker(extension=ZopeTransactionExtension())

Base = declarative_base(metadata=metadata)
#Base = declarative_base(metadata=metadata)
