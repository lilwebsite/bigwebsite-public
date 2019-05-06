import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
	'passlib',
	'bcrypt',
	'pyramid',
	'pyramid_jinja2',
	'pyramid_tm',
	'SQLAlchemy',
	'transaction',
	'zope.sqlalchemy',
	'zope.interface',
	'waitress',
	'gevent',
	'gunicorn',
	'Pillow',
	'PyPDF2'
	]

dev_requires = [
	'pyramid_debugtoolbar',
	'pytest',
	'WebTest'
]

setup(
	name='bigwebsite',
	version='1.0',
	description='Dylans Website',
	long_description='Bigwebsite is a website for Dylan Boroqhuez and his projects. The site is programmed by me (Carl Gessau) and can be managed by either dylan or me thanks to pyramid\'s framework.',
	classifiers=[
		"Programming Language :: Python",
		"Framework :: Pyramid",
		"Topic :: Internet :: WWW/HTTP",
		"Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
	],
	author='Carl Gessau',
	author_email='carl@bigwebsite.cool',
	url='www.bigwebsite.cool',
	keywords='',
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	install_requires=requires,
	extras_require={
		'dev': dev_requires
	},
	#entry_points="""\
	#[paste.app_factory]
	#main = bigwebsite:main
	#[console_scripts]
	#initialize_bigwebsite_db = bigwebsite.scripts.initializedb:main
	#"""
	entry_points={
		'paste.app_factory': [
			'main = bigwebsite:main'
		],
		'console_scripts': [
			'initialize_bigwebsite_db = bigwebsite.init_scripts.initializedb:main'
		]
	}
)
