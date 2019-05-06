from bigwebsite.include.video import *

class video:
	def __init__(self, request):
		self.request = request
		self.settings = self.request.registry.settings
		self.thumbdir = '%svideos/content/thumbs/' % self.settings['htmlfolder']
		self.htmldir = '%svideos/templates/' % self.settings['htmlfolder']

	def edithtml(self, file, tag):
		htmlfile = open(file, 'r+')
		replacetext = htmlfile.read().replace('border%s.png' % str(tag+1), 'border%s.png' % str(tag))
		htmlfile.seek(0)
		htmlfile.write(replacetext)
		htmlfile.truncate()

	def movefile(self, file, tag):
		if isfile(file % str(tag+1)):
			shutil.move(file % str(tag+1), file % str(tag))
		else:
			print('failed to move file ' + file % str(tag+1))

	def cleanurl(self, url):
		return re.search(r'(?:youtu[\.]be|youtube[\.]com)/{1}(?:watch\?v=)?(.*?)(?:&|$)', url)

	def getthumbs(self):
		thumbs = []
		for x in range(len(subprocess.check_output(['ls',self.thumbdir]).decode("utf-8").split('\n'))-1):
			thumbs.append('border%s' % str(x+1))
		return thumbs

	def add(self):
		if self.request.POST['video-submit'] == 'videourl':
			if self.request.POST['url'] != None and self.request.POST['thumbnail'] != None:
				filename = re.search(r'([.][P][N][G])', self.request.POST['thumbnail'].filename, re.IGNORECASE)
				if filename is not None:
					#get current amount of files (and their names)
					thumbs = self.getthumbs()
					#file number
					fnum = str(len(thumbs)+1)
					#setup video html and thumbnail html
					thumbtxt = '<img class="border" src="videos/content/thumbs/border%s.png" />' % fnum
					videotxt = '<div class="ytframe" ytsrc="%s"></div>'
					#directories
					thumbfp = self.thumbdir + "border%s.png" % fnum
					templatefp = self.htmldir + "video%s.html" % fnum
					#parse url
					cleanedurl = self.cleanurl(self.request.POST['url'])
					if cleanedurl is None:
						print("ERROR: URL UPLOAD")
						return Response('<p style="color: red">ERROR: bad youtube link</p>')
					videotxt = videotxt % cleanedurl.group(1)
					#save the files
					shutil.copyfileobj(self.request.POST['thumbnail'].file, open(thumbfp, 'wb'))
					open(templatefp, 'w+').write("\t\t\t" + thumbtxt + "\n\t\t\t" + videotxt)
					#successful upload
					return Response('<p style="color: green">upload success</p>')
				else:
					print("ERROR: IMAGE UPLOAD")
					return Response('<p style="color: red">ERROR: bad image file</p>')
		elif self.request.params['video-submit'] == 'videofile':
			pass
		return Response('<p style="color: red">unknown failure. contact admin</p>')

	def remove(self):
		#get video number
		vidnum = re.search('videodel(\d+)', self.request.POST['video-submit']).group(1)
		#get the file names to delete
		thumbfile = self.thumbdir + 'border' + vidnum + '.png'
		htmlfile = self.htmldir + 'video' + vidnum + '.html'
		#delete the files
		if isfile(thumbfile):
			remove(thumbfile)
		else:
			return Response('<p style="color: red">ERROR: failed to delete: file "%s" does not exist</p>' % thumbfile)
		if isfile(htmlfile):
			os(htmlfile)
		else:
			return Response('<p style="color: red">ERROR: failed to delete: file "%s" does not exist</p>' % htmlfile)
		#reorder the file numbers
		thumbs = self.getthumbs()
		tagged = None
		for x in range(len(thumbs)):
			for z in range(x+1):
				if isfile(self.thumbdir + "border%s.png" % str(z+1)) != True:
					tagged = z+1
					break;
			if tagged != None:
				#edit the html for the video template
				self.edithtml(self.htmldir + 'video%s.html' % str(tagged+1), tagged)
				#move the files to reorder them
				self.movefile(self.thumbdir + 'border%s.png', tagged)
				self.movefile(self.htmldir + 'video%s.html', tagged)
		return Response('<p style="color: green">video%s deleted successfully.</p>' % vidnum)
