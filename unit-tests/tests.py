import unittest
from pyramid import testing
from pyramid.paster import get_appsettings
from webtest import TestApp
from bigwebsite import main
from collections import OrderedDict
import pdb
from bigwebsite.data.stack import list_members

project_name = 'bigwebsite'
project_dir = '/usr/local/{project}'.format(project=project_name)
inifile = '{project}/test.ini'.format(project=project_dir)
settings = get_appsettings(inifile)

global_config = OrderedDict([ #spoof argv
	('here', project_dir),
	('__file__', '{project}/{inifile}'.format(project=project_dir, inifile=inifile))
])

app = main(global_config, test_settings=settings)

class bigwebsite_functional_tests(unittest.TestCase):
	def setUp(self):
		self.config = testing.setUp()
		self.testapp = TestApp(app)
		self.cookies = {}

	def tearDown(self):
		testing.tearDown()
	
	def login(self, user, password, status=302):
		response = self.testapp.post('/adminpage', {'login': user, 'password': password, 'form-submit': 'yes'}, status=status)
		if status == 302 and 'Set-Cookie' in response.headers:
			self.cookies['Cookie'] = response.headers['Set-Cookie']
		return response

	def logout(self, status=302):
		self.testapp.get('/logout', status=status)
		self.cookies = {} #clear cookies

	def test_bigwebsite(self):
		self.test_home()
		self.test_404()
		self.test_forbidden()
		self.test_unauthenticated()
		self.test_authenticated()
		self.test_notadmin()

	def test_home(self):
		self.testapp.get('/', status=200)

	def test_404(self):
		self.testapp.get('/random', status=404)
	
	def test_forbidden(self):
		self.testapp.get('/restricted/adminbanner.png', status=403)

	def test_unauthenticated(self):
		self.login('baduser', 'badpassword', 401)
	
	def test_authenticated(self):
		response = self.login('test', 'test')
		self.testapp.get('/adminpage', status=202, headers=self.cookies)
		self.testapp.get('/restricted/adminbanner.png', status=200, headers=self.cookies)
		self.logout()
	
	def test_notadmin(self):
		response = self.login('test_notadmin', 'test')
		self.testapp.get('/adminpage', status=403, headers=self.cookies)
		self.testapp.get('/restricted/adminbanner.png', status=403, headers=self.cookies)
		self.logout()
