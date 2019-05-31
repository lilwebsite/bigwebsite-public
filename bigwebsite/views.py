from bigwebsite.models import (
	User,
	AdminPage,
	Art
)
from bigwebsite.include.views import *
from bigwebsite.include.os import * 
from bigwebsite import forbidden
from bigwebsite.json import view_json
from bigwebsite.security import user_security
from bigwebsite.web.video import video
from bigwebsite.web.art import art_api as art
from bigwebsite.manipulate.bandcamp import formulate_embeds as bandcamp_embeds
from bigwebsite.include.debug import *

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
		self.getout = Response(open(self.getout, 'r').read())
		#get the user information
		self.security = user_security(self.request)
		#initialize the site functions
		self.video = video(self.request)
		self.art = art(self.request)

	@view_config(route_name='logout', renderer=None)
	def logout(self):
		return self.security.logout()
	
	def return_login(self):
		response = self.security.login()
		if self.request.params and not 'form-submit' in self.request.params:
			response = self.getout
			response.status = 403
		return response

	@view_config(route_name='adminpage', renderer='templates/adminpage.jinja2')
	#@http_cache((0, {'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache'}))
	def adminpage(self):
		if self.security.isloggedin() is True and self.security.isadmin() is False:
			return self.return_login()
		if not self.security.isadmin():
			return self.return_login()
		else:
			self.request.response.status = 202 #accepted
			returnval = {'page': 'adminpage'}
			print('permission: {user}'.format(user = self.security.user.permission))
			if self.request.params:
				if 'video-submit' in self.request.params:
					if self.request.POST['video-submit'] == 'videourl' or self.request.POST['video-submit'] == 'videofile': #if submitting video url or video file
						return self.video.add() #return videoadd response
					elif re.search(r'videodel\d+', self.request.POST['video-submit']) != None: #if submitting a delete request
						return self.video.remove() #return videoremove response
				elif 'art-submit' in self.request.params:
					if self.request.POST['art-submit'] == 'artimg':
						return self.art.add()
					elif re.search(r'(artdel|pdfobj_del)\d+', self.request.POST['art-submit']) != None:
						return self.art.remove()
				elif 'checksort-submit' in self.request.params:
					if self.request.POST['checksort-submit'] == 'checksort':
						self.art.object_sort()
			returnval['videohtml'] = self.video.elements.html()
			returnval['arthtml'] = self.art.elements.html()
			returnval['unsorted'] = self.request.dbsession.query(AdminPage).get(1).unsorted
			return returnval
		return self.return_login()

	@view_config(route_name='videolist', renderer='templates/videolist.jinja2')
	def videolist(self):
		if not self.security.isadmin():
			return self.getout
		else:
			return {'videohtml': self.video.elements.html()}
		return self.getout

	@view_config(route_name='artlist', renderer='templates/artlist.jinja2')
	def artlist(self):
		if not self.security.isadmin():
			return self.getout
		else:
			returnval = {'arthtml': self.art.elements.html()}
			return returnval
		return self.getout

class bigwebsiteViews:
	def __init__(self, request):
		self.request = request
		self.settings = self.request.registry.settings
		self.video = video(request)
		self.art = art(request)
		self.response = {'hostname': self.settings['hostname']}
		self.json = view_json(self.request)

	def checkemail(self, email):
		return re.search(r'[A-Z0-9.%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}', email, re.IGNORECASE)

	@view_config(route_name='devtest', renderer='templates/dev.jinja2')
	def devtest(self):
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
		thumbs = self.video.elements.html()
		self.response['videohtml'] = self.video.elements.html()
		return self.response

	@view_config(route_name='videoquery', renderer='json')
	def video_query(self):
		return self.json.query()
	
	@view_config(route_name='videocontainers', renderer='templates/videocontainers.jinja2')
	def video_containers(self):
		if self.request.params is not None and 'videocontainers' in self.request.POST:
			limit = int(self.request.post['videocontainers'])
			if type(limit) is int:
				self.art_limit = limit
		self.response['arthtml'] = self.get_videocontainers()
		return self.response
	
	@view_config(route_name='contact', renderer='templates/contact.jinja2')
	def bigwebsite_contact(self):
		if 'email' in self.request.params:
			if self.checkemail(self.request.POST['email']) is not None:
				message = 'Someone has submitted a new email request for {email} on the contact page. Send a message their way in response.'.format(email = self.request.POST['email'])
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

	def get_artcontainers(self):
		all_images = self.art.elements.html()
		images = []
		for x in range(len(all_images)):
			if x >= self.json.art_limit:
				break;
			images.append(all_images[x])
		return images
	
	@view_config(route_name='art', renderer='templates/art.jinja2')
	def bigwebsite_art(self):
		self.response['loneimage'] = False
		self.response['arthtml'] = self.get_artcontainers()
		if 'img' in self.request.params:
			for x in self.art.formathtml():
				if x[3] == self.request.GET['img']:
					self.response['loneimage'] = True
					self.response['arthtml'] = self.request.GET['img']
					return self.response
		return self.response

	@view_config(route_name='artquery', renderer='json')
	def art_query(self):
		return self.json.query()
	
	@view_config(route_name='artcontainers', renderer='templates/artcontainers.jinja2')
	def art_containers(self):
		if self.request.params is not None and 'artcontainers' in self.request.POST:
			limit = int(self.request.post['artcontainers'])
			if type(limit) is int:
				self.art_limit = limit
		self.response['arthtml'] = self.get_artcontainers()
		return self.response

	@view_config(route_name='music', renderer='templates/music.jinja2')
	def bigwebsite_music(self):
		self.response['embeds'] = bandcamp_embeds(self.settings['bandcamp'])
		return self.response

	@view_config(route_name='test', renderer='templates/testpage.jinja2')
	def test(self):
		return self.response

class noscriptViews:
	def __init__(self, request):
		self.request = request
		self.settings = self.request.registry.settings
		self.video = video(self.request)
		#self.art = art(self.art)
		self.response = {'hostname': self.settings['hostname']}

	@view_config(route_name='noscript', renderer='templates/noscript.jinja2')
	def bigwebsite_noscript(self):
		return self.response

	@view_config(route_name='noscript-videos', renderer='templates/noscript-videos.jinja2')
	def videos_noscript(self):
		self.response['videos'] = self.video.elements.html()
		return self.response
