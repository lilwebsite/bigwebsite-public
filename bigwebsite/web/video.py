from bigwebsite.include.video import *
from bigwebsite.include.debug import *

class video_elements:
	def __init__(self, dbinfo, settings):
		self.dbinfo = dbinfo
		self.settings = settings
		self.element = video_element()

	def write_img_uri(self, name, uri='/{uri}{name}'):
		return uri.format(
			uri=self.settings['video.uri'],
			name=name
		)
	
	def write_ytsrc_param(self, ytsrc):
		return 'ytsrc="{ytsrc}"'.format(
			ytsrc=ytsrc
		)

	def html(self):
		elements = []
		for vidobj in self.dbinfo:
			self.element.__init__()
			vidobj_id = 'video{id}'.format(id=vidobj.id)
			thumb_tag = self.element.set_thumb_src(
				self.write_img_uri(vidobj.thumbnail),
				vidobj_id
			)
			border_tag = self.element.set_border_src(
				self.write_img_uri(vidobj.border),
				vidobj_id
			)
			frame_tag = self.element.set_frame_params(
				self.write_ytsrc_param(vidobj.ytid),
				vidobj_id
			)
			elements.append({
				'thumbnail': thumb_tag,
				'border': border_tag,
				'ytframe': frame_tag,
				'num': vidobj.id,
				'type': 'video'
			})
		ordered = []
		for x in range(len(elements)-1, -1, -1):
			ordered.append(elements[x])
		return ordered

class video:
	def __init__(self, request):
		self.request = request
		self.settings = self.request.registry.settings
		self.resp_status = response_status()
		self.border_root = '{root}{uri}'.format(
			root=self.settings['htmlfolder'],
			uri=self.settings['video.uri']
		)
		self.border = '{date}border{num}.png'
		self.time_now = datetime.now() #get time in datetime format for SQLAlchemy
		self.date = self.time_now.strftime('%S%M%H%y') #use datetime.strftime to get filename date
		self.dbinfo = self.request.dbsession.query(Video).all()
		self.elements = video_elements(self.dbinfo, self.settings)

	def cleanurl(self, url):
		return re.search(r'(?:youtu[\.]be|youtube[\.]com)/{1}(?:watch\?v=)?(.*?)(?:&|$)', url).group(1)
	
	def format_name(self, template):
		return template.format(
			date=self.date,
			num=len(self.dbinfo)+1
		)
	
	def format_fullpath(self, name):
		return '{path}{name}'.format(
			path=self.border_root,
			name=name
		)

	def add(self):
		if self.request.POST['video-submit'] == 'videourl':
			if self.request.POST['url'] != None and self.request.POST['border'] != None:
				bordername = re.search(r'(.PNG)', self.request.POST['border'].filename, re.IGNORECASE)
				if bordername is not None:
					colors = 32
					if 'colors' in self.request.POST:
						if type(int(self.request.POST['colors'])) is int: 
							colors = int(self.request.POST['colors'])

					bordername = self.format_name('{date}border{num}.png')
					thumbname = self.format_name('{date}video-thumbnail{num}.jpeg')
					border = self.format_fullpath(bordername)
					thumb = self.format_fullpath(thumbname)

					shutil.copyfileobj(
						self.request.POST['border'].file,
						open(border, 'wb')
					)
					try:
						border = i(border, True)
					except:
						return self.resp_status.error(0) #image load error

					cleanedurl = self.cleanurl(self.request.POST['url'])
					if cleanedurl is None:
						print("ERROR: URL UPLOAD")
						return self.resp_status.error(0)
						#return Response('<p style="color: red">ERROR: bad youtube link</p>')

					#genthumbnail() border image object, thumbnail destination, youtube id and settings
					gen_status = genthumbnail(border, thumb, cleanedurl, self.settings)
					if gen_status:
						return self.resp_status.error(0)

					try: #add the time file was uploaded to the database
						dbvideo = Video(border=bordername, thumbnail=thumbname, ytid=cleanedurl, uploadtime=self.time_now)
						self.request.dbsession.add(dbvideo)
						self.request.dbsession.flush()
					except:
						return self.resp_status.error(9)
					#successful upload
					return self.resp_status.ok(1)
				else:
					print("ERROR: VIDEO UPLOAD")
					return self.resp_status.error(0)
		elif self.request.params['video-submit'] == 'videofile':
			pass
		return Response('<p style="color: red">unknown failure. contact admin</p>')

	def remove(self):
		vidnum = re.search('videodel(\d+)', self.request.POST['video-submit']).group(1)
		dbentry = self.request.dbsession.query(Video).filter(Video.id==vidnum)
		if not dbentry.one():
			return self.resp_status.error(0)
		borderfile = self.format_fullpath(dbentry.one().border)
		thumbfile = self.format_fullpath(dbentry.one().thumbnail)
		if isfile(borderfile):
			remove(borderfile)
		if isfile(thumbfile):
			remove(thumbfile)
		try:
			dbentry.delete()
			self.request.dbsession.flush()
		except (NoResultFound, DataError):
			return self.resp_status.warn(2)
		return self.resp_status.ok(1)
