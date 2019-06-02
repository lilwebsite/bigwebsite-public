import unittest
from pyramid import testing
from pyramid.paster import get_appsettings
from webtest import TestApp
from bigwebsite import main
from collections import OrderedDict
from bigwebsite.include.os import *

project_name = 'bigwebsite'
project_dir = '/usr/local/{project}/'.format(project=project_name)

def append_projectdir(target):
	return ('{project}' + target).format(project=project_dir)

inifile = append_projectdir('test.ini')
webroot = append_projectdir('webroot/')
permissions = append_projectdir('helpfiles/webroot_permissions.sh')
testfiles = append_projectdir('unit-tests/test-files/')
default_db = append_projectdir('test.default.sqlite')
db = append_projectdir('test.sqlite')

def rm_database():
	if isfile(db):
		subprocess.call(['rm','-f',db])

rm_database()
subprocess.call(['cp',default_db,db])

settings = get_appsettings(inifile)
global_config = OrderedDict([ #spoof argv
	('here', project_dir),
	('__file__', '{project}/{inifile}'.format(project=project_dir, inifile=inifile))
])
app = main(global_config, test_settings=settings)

def rm_webroot():
	if isdir(settings['htmlfolder']):
		return subprocess.call(['rm','-rf',settings['htmlfolder']])

def rm_testfiles():
	rm_webroot()
	rm_database()

class json_requests:
	def error(self, response):
		if response.status is 200:
			if response.json[0] != 'error':
				return False
		return True
	
	def query(self, query):
		params = {'type': self.query_type}
		for key, val in query.items():
			params[key] = val
		return self.testapp.post(self.query_uri, params, status=200)
	
	def get_limit(self):
		return self.query({'getlimit': 'dummy'})

class bigwebsite_video_tests(json_requests):
	def __init__(self, testapp, cookies):
		self.testapp = testapp
		self.cookies = cookies
		self.query_type = '1'
		self.query_uri = '/videos/query'
		self.testfile = testfiles + 'test-border.png'
		self.ytlink = 'https://www.youtube.com/watch?v=b-XiC4SkR70'

	def page(self):
		self.testapp.get('/videos', status=200)
		self.testapp.get('/adminpage/videolist', status=200, headers=self.cookies)
		limit = self.get_limit()
		if not self.error(limit):
			self.query({'query': limit[0]})
	
	def admin_add(self):
		self.testapp.post('/adminpage', {'url': self.ytlink, 'video-submit': 'videourl'}, upload_files=[('border', self.testfile)], status=200, headers=self.cookies)
		self.page()
	
	def admin_remove(self):
		self.testapp.post('/adminpage', {'video-submit': 'videodel1'}, status=200, headers=self.cookies)
		self.page()

class bigwebsite_art_tests(json_requests):
	def __init__(self, testapp, cookies=None):
		self.testapp = testapp
		self.cookies = cookies
		self.query_type = '0'
		self.query_uri = '/art/query'
		self.testfiles = (
			testfiles + 'test-art.png', 
			testfiles + 'test-art.jpeg', 
			testfiles + 'test-art.pdf'
		)

	def page(self):
		self.testapp.get('/art', status=200)
		self.testapp.get('/adminpage/artlist', status=200, headers=self.cookies)
		limit = self.get_limit()
		if not self.error(limit):
			self.query({'query': limit[0]})
	
	def admin_add(self):
		for art in self.testfiles:
			self.testapp.post('/adminpage', {'art-submit': 'artimg'}, upload_files=[('art', art)], status=200, headers=self.cookies)
			self.page()
	
	def admin_remove(self):
		for x in range(1, len(self.testfiles)):
			self.testapp.post('/adminpage', {'art-submit': 'artdel{x}'.format(x=x)}, status=200, headers=self.cookies)
			self.page()
		self.testapp.post('/adminpage', {'art-submit': 'pdfobj_del{x}'.format(x=len(self.testfiles))}, status=200, headers=self.cookies)
		self.page()

class bigwebsite_functional_tests(unittest.TestCase):
	def setUp(self):
		self.config = testing.setUp()
		self.testapp = TestApp(app)
		self.cookies = {}
		rm_webroot()
		subprocess.call(['cp','-r',webroot,settings['htmlfolder']])
		subprocess.call(['/bin/bash',permissions,settings['htmlfolder']])

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

	def test_home(self):
		self.testapp.get('/', status=200)

	def test_404(self):
		self.testapp.get('/random', status=404)
	
	def test_forbidden(self):
		self.testapp.get('/restricted/adminbanner.png', status=403)

	def test_unauthenticated(self):
		self.login('baduser', 'badpassword', 401)
	
	def test_authenticated(self):
		response = self.login('admin', 'test')
		self.testapp.get('/adminpage', status=202, headers=self.cookies)
		self.testapp.get('/restricted/adminbanner.png', status=200, headers=self.cookies)
		self.logout()
	
	def test_notadmin(self):
		response = self.login('test', 'test')
		self.testapp.get('/adminpage', status=403, headers=self.cookies)
		self.testapp.get('/restricted/adminbanner.png', status=403, headers=self.cookies)
		self.logout()

	def test_video(self):
		self.login('admin', 'test')
		test_video = bigwebsite_video_tests(self.testapp, self.cookies)
		test_video.page()
		test_video.admin_add()
		test_video.admin_remove()

	def test_art(self):
		self.login('admin', 'test')
		test_art = bigwebsite_art_tests(self.testapp, self.cookies)
		test_art.page()
		test_art.admin_add()
		test_art.admin_remove()
