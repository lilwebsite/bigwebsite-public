from bigwebsite.models import (
	User,
	AdminPage
)
from bigwebsite.include.views import *
from bigwebsite.include.os import * 
from bigwebsite import forbidden
from bigwebsite.security import user_security
from bigwebsite.web import video
from bigwebsite.web.art import art_api as art
from bigwebsite.manipulate.bandcamp import formulate_embeds as bandcamp_embeds

#alias for list()
def aliasl(l):
	return list(l)

class html_setup:
	def __init__(self):
		self.art = None

	def was_initialized(self):
		return self.art is not None

	def setup_arthtml(self):
		returnval = []
		arthtml = self.art.elements.html()
		z = len(arthtml)
		for image in arthtml:
			returnval['arthtml'].append({
				'html': image['thumbnail'],
				'num': image['num'],
				'which': z
			})
			z -= 1
		return returnval

class adminViews(html_setup):
	def __init__(self, request):
		#setup variables
		self.request = request
		self.settings = self.request.registry.settings
		#get defaults
		self.getout = self.settings['htmlfolder'] + self.settings['getout'] 
		#get the user information
		self.security = user_security(self.request)
		#initialize the site functions
		self.vid = video(self.request)
		self.art = art(self.request)

	@view_config(route_name='logout', renderer=None)
	def logout(self):
		return self.security.logout()
	
	@view_config(route_name='adminpage', renderer='templates/adminpage.jinja2')
	#@http_cache((0, {'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache'}))
	def adminpage(self):
		if self.security.isloggedin() is True and self.security.isadmin() is False:
			response = self.security.login()
			response.status = 403
			return response
		if not self.security.isadmin():
			return self.security.login()
		else:
			self.request.response.status = 202 #accepted
			returnval = {'page': 'adminpage'}
			print('permission: {user}'.format(user = self.security.user.permission))
			if self.request.params != None:
				if 'video-submit' in self.request.params:
					if self.request.POST['video-submit'] == 'videourl' or self.request.POST['video-submit'] == 'videofile': #if submitting video url or video file
						return self.vid.add() #return videoadd response
					elif re.search(r'videodel\d+', self.request.POST['video-submit']) != None: #if submitting a delete request
						return self.vid.remove() #return videoremove response
				elif 'art-submit' in self.request.params:
					if self.request.POST['art-submit'] == 'artimg':
						return self.art.add()
					elif re.search(r'artdel\d+', self.request.POST['art-submit']) != None:
						return self.art.remove()
				#elif 'checksort-submit' in self.request.params:
				#	if self.request.POST['checksort-submit'] == 'checksort':
				#		self.art.autoimagesort()
			returnval['videohtml'] = [] #prepare to list the videos for the template
			returnval['arthtml'] = self.art.elements.html()
			thumbs = self.vid.getthumbs()
			for x in range(len(thumbs)): #add the videos to the template
				returnval['videohtml'].append(
					{
						'html': open('%svideo%s.html' % (self.vid.htmldir, str(x+1)), 'r+').read(),
						'num': x+1
					}
				)
			returnval['unsorted'] = self.request.dbsession.query(AdminPage).get(1).unsorted
			return returnval
		return self.security.login() 

	@view_config(route_name='videolist', renderer='templates/videolist.jinja2')
	def videolist(self):
		if not self.security.isadmin():
			return Response(open(self.getout, 'r').read())
		else:
			thumbs = self.vid.getthumbs()
			returnval = {'videohtml': []}
			for x in range(len(thumbs)):
				#add the videos to the template
				returnval['videohtml'].append({'html': open('%svideo%s.html' % (vid.htmldir, str(x+1)), 'r+').read(), 'num': x+1})
			return returnval
		return Response(open(self.getout, 'r').read())

	@view_config(route_name='artlist', renderer='templates/artlist.jinja2')
	def artlist(self):
		if not self.security.isadmin():
			return Response(open(self.getout, 'r').read())
		else:
			returnval = {'arthtml': self.art.elements.html()}
			return returnval
		return Response(open(self.getout, 'r').read())

class bigwebsiteViews:
	def __init__(self, request):
		self.request = request
		self.settings = self.request.registry.settings
		self.vid = video(self.request)
		self.art = art(self.request)
		self.response = {'hostname': self.settings['hostname']}

	def checkemail(self, email):
		return re.search(r'[A-Z0-9.%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}', email, re.IGNORECASE)

	@view_config(route_name='devtest', renderer='templates/dev.jinja2')
	def devtest(self):
		image = Art(name='test.jpg', uploadtime=datetime.now())
		self.request.dbsession.add(image)
		self.request.dbsession.flush()
		return self.response

	@view_config(route_name='home', renderer='templates/site.jinja2')
	def bigwebsite(self):
		if 'buttonbroke' in self.request.params and self.request.user == None:
			response = HTTPOk()
			response.set_cookie('button', value='buttonisbroken', max_age=604800)
			return response
		if 'button' in self.request.cookies:
			self.response['button'] = 0
		else:
			self.response['button'] = 1
		return self.response

	@view_config(route_name='videos', renderer='templates/videos.jinja2')
	def bigwebsite_videos(self):
		thumbs = self.vid.getthumbs()
		self.response['videohtml'] = []
		for x in range(len(thumbs)-1, -1, -1):
			self.response['videohtml'].append(open('%svideo%s.html' % (self.vid.htmldir, str(x+1)), 'r+').read())
		return self.response

	@view_config(route_name='contact', renderer='templates/contact.jinja2')
	def bigwebsite_contact(self):
		if 'email' in self.request.params:
			if self.checkemail(self.request.POST['email']) is not None:
				message = 'Someone has submitted a new email request for {email} on the contact page.'.format(email = self.request.POST['email'])
				pipe = subprocess.Popen(('echo', message), stdout=subprocess.PIPE)
				subprocess.call(('mail', '-s', 'email request', 'dylan@localhost'), stdin=pipe.stdout)
				return Response('ok')
			return error.get(1)
		return self.response

	@view_config(route_name='about', renderer='templates/about.jinja2')
	def bigwebsite_about(self):
		return self.response

	@view_config(route_name='demands', renderer='templates/demands.jinja2')
	def bigwebsite_demands(self):
		return self.response

	@view_config(route_name='art', renderer='templates/art.jinja2')
	def bigwebsite_art(self):
		self.response['loneimage'] = False
		self.response['arthtml'] = self.art.elements.html()
		if 'img' in self.request.params:
			for x in self.art.formathtml():
				if x[3] == self.request.GET['img']:
					self.response['loneimage'] = True
					self.response['arthtml'] = self.request.GET['img']
					return self.response
		return self.response

	@view_config(route_name='music', renderer='templates/music.jinja2')
	def bigwebsite_music(self):
		self.response['embeds'] = bandcamp_embeds()
		return self.response

	@view_config(route_name='test', renderer='templates/testpage.jinja2')
	def test(self):
		return self.response

class noscriptViews:
	def __init__(self, request):
		self.request = request
		self.settings = self.request.registry.settings
		self.vid = video(self.request)
		#self.art = art(self.art)
		self.response = {'hostname': self.settings['hostname']}

	@view_config(route_name='redir', renderer='templates/scripts/redir.jinja2')
	def noscript_redirect(self):
		return self.response

	@view_config(route_name='noscript', renderer='templates/noscript.jinja2')
	def bigwebsite_noscript(self):
		return self.response

	@view_config(route_name='noscript-videos', renderer='templates/noscript-videos.jinja2')
	def videos_noscript(self):
		thumbs = self.vid.getthumbs()
		self.response['videos'] = []
		for x in range(len(thumbs)-1, -1, -1):
			self.response['videos'].append(open('%svideo%s.html' % (self.vid.htmldir, str(x+1)), 'r+').read())
		return self.response
