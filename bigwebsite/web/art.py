from bigwebsite.include.art import *
import pdb

class art_elements:
	def __init__(self, art, settings):
		self.art = art
		self.settings = settings
		self.element = img_element()
	
	def write_img_uri(self, uri, image):
		return uri.format(
			uri=self.settings['art.uri'],
			filename=image.file.name,
			ext=image.file.ext
		)
	
	def write_pdf_uri(self, pdfobj_num, img_name, uri='{uri}{pdfobj}{img}.jpeg'):
		return uri.format(
			uri=self.settings['art.uri'],
			pdfobj='pdf/pdfobj{num}/'.format(num=pdfobj_num),
			img=img_name
		)

	def html(self):
		if self.art is None: #if there are no images, return None
			return [None]
		elements = []
		img_tag = self.element.set_imgclass('art')
		pdf_tag = self.element.set_imgclass('pdf')
		num = 0
		for x in self.art:
			element_type = None
			num += 1
			if type(x) != i:
				
				pdfobj = x
				if pdfobj[0] is not None:
					element_type = 'pdf'
					uri = self.write_pdf_uri(pdfobj_num=pdfobj[1], img_name='thumbnail')
				else:
					continue;
			else:
				element_type = 'img'
				uri = self.write_img_uri('{uri}{filename}.{ext}', x)
				thumb_uri = self.write_img_uri('{uri}{filename}-thumbnail.{ext}', x)
			if element_type:
				current = {'type': element_type}
				if element_type == 'img' and uri is not None and thumb_uri is not None:
					temp = {
						'main': img_tag.format(uri=uri),
						'thumbnail': img_tag.format(uri=thumb_uri),
						'uri': uri,
						'thumb_uri': thumb_uri,
						'num': num,
						'delete': 'artdel{num}'.format(num=x.file.number)
					}
				elif element_type == 'pdf' and uri is not None and pdfobj is not None:
					temp = {
						'main': pdf_tag.format(uri=uri),
						'uri': uri,
						'num': num,
						'delete': 'pdfobj_del{num}'.format(num=pdfobj[1]),
						'pdfobj': '{num};{amount}'.format(num=pdfobj[1], amount=pdfobj[1])
					}
				if temp:
					for key,val in temp.items():
						current[key] = val
			if current:
				elements.append(current)
		return elements

class art_functions:
	def __init__(self, request, artpath):
		self.pdf_regx = r'(pdfobj(\d+))'
		self.epoch_regx = r'(\d{4})-(\d{2})-(\d{2})\W(\d{2}):(\d{2}):(\d{2}).*\W(\d{8}art\d+)\..*'
		self.img_regx = r'(\d{8}art\d+).(\w+)'
		self.request = request
		self.artpath = artpath

	def ispdf(self, fileinfo):
		try:
			result = re.search(self.pdf_regx, fileinfo, re.IGNORECASE)
		except:
			raise SyntaxError
		if result is None:
			return False
		return True

	def isimg(self, fileinfo):
		try:
			result = re.search(self.epoch_regx, fileinfo, re.IGNORECASE)
		except:
			raise SyntaxError
		if result is None:
			return False
		return True
		
	def updatedb_unsorted(self, bsetting):
		try:
			self.request.dbsession.query(AdminPage).filter().update(
			values={
				'unsorted': bsetting
			})
			self.request.dbsession.flush()
		except (NoResultFound, DataError):
			print('ERROR: changing unsorted status to true failed')

	def time2epoch(self, timestamp):
		#returns a string timestamp that built-in sorted can use
		epochtime = ''
		for x in range(len(timestamp)-1):
			epochtime += str(timestamp[x])
		epochtime = int(mktime(strptime(epochtime, '%Y%m%d%H%M%S')))
		return {epochtime: timestamp[len(timestamp)-1]}

	def ls_artpath(self, child_dir='', full=True):
		if full:
			return subprocess.check_output(['ls', '-l', '--full-time', self.artpath + child_dir]).decode('UTF-8')
		return subprocess.check_output(['ls', self.artpath + child_dir]).decode('UTF-8')

	def get_objects(self, artpath):
		art = unordered = []
		epochtimes = {}
		pdf_dirs = {}
		dbinfo = self.request.dbsession.query(Art).all()

		#combine outputs
		output_image = self.ls_artpath().split('\n') #separate each file in the directory
		output_pdf = self.ls_artpath(child_dir='pdf/').split('\n')
		outputs = (output_image, output_pdf)
		output = []
		for folder in outputs:
			try:
				if re.search(r'total 0', folder[0]) is not None:
					continue;
			except IndexError:
				pass
			for fileinfo in range(1, len(folder)-1):
				output.append(folder[fileinfo])
		if not output: #if theres nothing in the directories return None
			return [None]

		files = len(output)-1 #total amount of files found
		#files_pdf = len(output_pdf)-1
		found = 0

		for fileinfo in output: #resolves timestamps and file names in the art directory
			if self.ispdf(fileinfo):
				pdfnum = re.search(self.pdf_regx, fileinfo, re.IGNORECASE)
				if pdfnum:
					for entry in dbinfo:
						if entry.name == pdfnum.group(1):
							time = entry.uploadtime
							epoch = self.time2epoch([
								time.year,
								time.month,
								time.day,
								time.hour,
								time.minute,
								time.second,
								pdfnum.group(1)
							])
							for key,val in epoch.items():
								epochtimes[key] = val
								found += 1
			elif self.isimg(fileinfo):
				epoch = re.findall(self.epoch_regx, fileinfo, re.IGNORECASE) #will return an array with a tuple which contains the matched regex ex: [(0, 1, ..., 6)]
				if epoch:
					epoch = self.time2epoch(epoch[0])
					for key,val in epoch.items():
						epochtimes[key] = val
						found += 1

####			pdf_dirs[int(pdfnum[0])] = len(
####				subprocess.check_output(
####					['ls', self.artpath + 'pdf/pdfobj{num}/'.format(num=pdfnum[0])]
####				).decode('UTF-8').split('\n')
####			)-1
	
		unordered = sorted(epochtimes) #use built-in sorted to get chronological order (oldest -> newest)
		if len(unordered) == found:
			self.updatedb_unsorted(False)
		else:
			self.updatedb_unsorted(True)

		for x in range(len(unordered)): #formulate usable info from what we got
			current = None
			for fileinfo in output:
				if self.ispdf(fileinfo):
					current = re.search(self.pdf_regx, fileinfo, re.IGNORECASE)
					if current:
						pdf_images = len(
							self.ls_artpath(
								child_dir='pdf/{pdfobj}'.format(
									pdfobj=current.group(1)
								),
								full=False
							).split('\n')
						)-1
						current = (current.group(1), pdf_images) #(pdf folder name, amount of images in pdf)
						break;
				elif self.isimg(fileinfo):
					error = 0
					current = re.findall(self.img_regx, fileinfo, re.IGNORECASE)
					if current:
						current = current[0]
						current = i('{path}{name}.{ext}'.format(path=artpath, name=current[0], ext=current[1]))
						if current.error is None:
							error = None
						if current.file.name == epochtimes[unordered[x]]:
							break;
			if error is None:
				art.append(current)
			else:
				print('ERROR: no valid format')


		ordered = []
		for z in range(len(unordered)-1, -1, -1): #sort files (newest -> oldest)
			for x in range(len(art)):
				if type(art[x]) is tuple:
					if art[x][0] == 'pdfobj{num}'.format(num=z):
						ordered.append(art[x])
						break;
					continue;
				elif type(art[x]) is i:
					if art[x].file.name == epochtimes[unordered[z]]:
						ordered.append(art[x])
						break;

		for key,val in pdf_dirs.items():
			ordered.insert(key-1, 'pdfobj{num};{val}'.format(num=key, val=val))

		return ordered

class art_api:
	def __init__(self, request):
		self.request = request
		self.resp_status = response_status()
		self.security = user_security(self.request)
		self.settings = self.request.registry.settings
		self.artpath = '{root}{uri}'.format(root=self.settings['htmlfolder'], uri=self.settings['art.uri'])
		self.filetypes = r'{regx}'.format(regx=self.settings['allowed_filetypes.images'])
		art = art_functions(request, self.artpath)
		self.files = art.get_objects(self.artpath)
		self.elements = art_elements(self.files, self.settings)
	
	def store_file(self, filename, path):
		if movefile(
			filename,
			path, #src
			self.artpath #dst
		) is not None:
			self.add_clean(artfp)
			return self.resp_status.error(8)
		return None

	def add_clean(self, filepath):
		subprocess.call(['rm', '-f', filepath])
	
	def add_pdf(self, filenum):
		foldername = 'pdfobj{num}'.format(num=filenum)
		tmpfp = '/tmp/{name}'.format(name=foldername)
		pdf_folder = '{artpath}pdf/'.format(artpath=self.artpath)
		fullpath = '{pdf_folder}{foldername}'.format(pdf_folder=pdf_folder, foldername=foldername)
		if not isdir(fullpath):
			mkdir(path=fullpath)
			subprocess.call(['chmod', '755', fullpath]) #using the mode argument for mkdir does silly things, so we use chmod directly

		shutil.copyfileobj(
			self.request.POST['art'].file,
			open(tmpfp, 'wb')
		)
		pdf_images = pdf2images(open(tmpfp, 'rb'))
		
		for x in range(len(pdf_images)):
			img = '{fullpath}/{num}.jpeg'.format(fullpath=fullpath, num=x)
			if pdf_images[x].mode == 'P':
				pdf_images[x].convert(mode='RGB')
			pdf_images[x].save(img, format='JPEG')
			pdf_images[x] = img

		for x in range(len(pdf_images)):
			img = i(pdf_images[x], openfile=True)
			compress = imgcompress(img, 0.1, (600, 600), (1250, 1250)) #(image file, max file size, minimum dimensions, maximum dimensions)
			try:
				newimg = compress.compress_pdf()
				if newimg is (IOError or OSError):
					raise newimg
			except:
				print('failed on iteration #{x}'.format(x=x))
				return self.resp_status.error(4)
			pdf_images[x] = newimg
		
		thumbnail = i(pdf_images[0].fullpath, openfile=True)
		compress = imgcompress(thumbnail)
		try:
			thumbnail = compress.compress_default(saveas='{fullpath}/thumbnail.jpeg'.format(fullpath=fullpath))
			if thumbnail is (IOError or OSError):
				raise thumbnail
		except:
			return self.resp_status.error(4)

		try: #add the time file was uploaded to the database
			dbimage = Art(type='pdf', name=foldername, uploadtime=self.time_now, cached=False)
			self.request.dbsession.add(dbimage)
			self.request.dbsession.flush()
		except:
			return self.resp_status.warn(2)
		return self.resp_status.ok(1)
		

	def add_image(self, filenum, filetype):
		artname = '{date}art{num}.{ext}'.format(date=self.date, num=filenum, ext=filetype)
		artfp = '/tmp/{name}'.format(name=artname)
		shutil.copyfileobj( #save the file
			self.request.POST['art'].file,
			open(artfp, 'wb')
		)

		imagefile = i(artfp, openfile=True) #load the image
		if imagefile.error is not None:
			self.add_clean(artfp)
			return self.resp_status.error(3)
		if re.search(self.filetypes, imagefile.loadedimage.format, re.IGNORECASE) is None:
			return self.resp_status.error(5)
		compress = imgcompress(imagefile) #generate compression object
		try: #try compressing the image
			newimg = compress.compress_image() #returns the new image object (not loaded)
			if newimg is (IOError or OSError):
				raise newimg
		except:
			self.add_clean(artfp)
			return self.resp_status.error(4)
		compress = imgcompress(newimg) #reload the file
		try: #try creating the thumbnail
			thumb = compress.generate_thumbnail()
			if thumb is (IOError or OSError):
				raise thumb
		except:
			self.add_clean(artfp)
			return self.resp_status.error(4)

		form = '{name}.{ext}'
		artname = form.format(name=newimg.file.name, ext=newimg.file.ext)
		thumbname = form.format(name=thumb.file.name, ext=thumb.file.ext)
		newimg = self.store_file(artname, newimg.file.path)
		thumb = self.store_file(thumbname, thumb.file.path)
		if newimg is not None:
			return newimg
		if thumb is not None:
			return thumb

		try: #add the time file was uploaded to the database
			dbimage = Art(type='img', name=artname, uploadtime=self.time_now, cached=False)
			self.request.dbsession.add(dbimage)
			self.request.dbsession.flush()
		except:
			return self.resp_status.warn(2)
		return self.resp_status.ok(1)

	def add(self):
		self.time_now = datetime.now() #get time in datetime format for SQLAlchemy
		self.date = self.time_now.strftime('%S%M%H%y') #use datetime.strftime to get filename date
		filenum = len(
			self.request.dbsession.query(Art).order_by(Art.id).all()
		)+1

		if self.security.isadmin is False:
			return self.resp_status.error()
		if self.request.POST['art-submit'] != 'artimg':
			return self.resp_status.error(10)
		if self.request.POST['art'] is None or self.request.POST['filename'] is None:
			return self.resp_status.error(10)

		filetype = re.search(self.filetypes, self.request.POST['filename'], re.IGNORECASE) 
		if filetype is None:
			return self.resp_status.error(2)
		filetype = filetype.group(1).lower()

		if filetype == 'pdf':
			return self.add_pdf(filenum)
		else:
			return self.add_image(filenum, filetype)

	def remove(self):
		art = thumb = None
		art_dst = '/usr/local/{projectname}/.cached/'.format(projectname=self.settings['project_name'])

		if self.request.POST['art-submit'] is None:
			return self.resp_status.error(10)
		
		artnum = re.search(r'artdel(\d+)', self.request.POST['art-submit']) #check and retrieve the filename from the request
		if artnum is None:
			return self.resp_status.error(10)
		artnum = int(artnum.group(1))
		
		for x in self.files:
			if x.file.number == artnum:
				art = x
				break;
		if not art:
			return self.resp_status.error(6)

		if isfile(art.fullpath): #figure out if the thumbnail exists and delete it
			thumb = i(
				'{path}{filename}-thumbnail.{ext}'.format(
					path=art.file.path,
					filename=art.file.name,
					ext=art.file.ext
				)
			)
			if thumb.error is not None:
				return self.resp_status.error(7)
			if isfile(thumb.fullpath):
				subprocess.call(['rm', '-f', thumb.fullpath])
			else:
				return self.resp_status.error(7)
		else:
			return self.resp_status.error(6)

		if movefile(
			'{name}.{ext}'.format(name=art.file.name, ext=art.file.ext), #filename
			art.file.path, #src
			art_dst #dst
		) is not None:
			return self.resp_status.error(11)

		try:
			self.request.dbsession.query(Art).filter(
				Art.name=='{filename}.{ext}'.format(
					filename=art.file.name,
					ext=art.file.ext
				)
			).update(values={'cached': True})
			self.request.dbsession.flush()
		except (NoResultFound, DataError):
			return self.resp_status.warn(2)

		response = self.resp_status.ok(2)
		response.text = response.text.format(number=artnum)
		return response
