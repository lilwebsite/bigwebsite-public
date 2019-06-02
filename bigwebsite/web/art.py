from bigwebsite.include.art import *

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
		img_tag = self.element.set_img_class('art')
		pdf_tag = self.element.set_img_class('pdf')
		pdfobj_num = 0
		num = 0
		for artobj in self.art:
			num += 1
			current = {'type': artobj.type}
			if type(artobj) is i:
				uri = self.write_img_uri('{uri}{filename}.{ext}', artobj)
				thumb_uri = self.write_img_uri('{uri}{filename}-thumbnail.{ext}', artobj)
				info = {
					'main': img_tag.format(uri=uri),
					'thumbnail': img_tag.format(uri=thumb_uri),
					'uri': uri,
					'thumb_uri': thumb_uri,
					'num': num,
					'delete': 'artdel{num}'.format(num=artobj.file.number)
				}
			if type(artobj) is p:
				pdfnum = int(re.search(r'pdfobj(\d+)', artobj.pdfobj.name).group(1))
				uri = self.write_pdf_uri(pdfobj_num=pdfnum, img_name='thumbnail')
				info = {
					'main': pdf_tag.format(uri=uri),
					'uri': uri,
					'num': num,
					'delete': 'pdfobj_del{num}'.format(num=pdfnum),
					'pdfobj': '{num};{amount}'.format(num=pdfnum, amount=len(artobj.pdfobj.images))
				}
			for key,val in info.items():
				current[key] = val
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
		dbinfo = self.request.dbsession.query(Art).all()

		for artobj in dbinfo:
			time = artobj.uploadtime
			epoch = self.time2epoch([
				time.year,
				time.month,
				time.day,
				time.hour,
				time.minute,
				time.second,
				artobj.name
			])
			for key,val in epoch.items():
				epochtimes[key] = val

		sorted_list = sorted(epochtimes) #use built-in sorted to get chronological order (oldest -> newest)

		for x in range(len(sorted_list)):
			current = None
			for artobj in dbinfo:
				if artobj.name == epochtimes[sorted_list[x]]:
					if artobj.type == 'img':
						current = i('{path}{name}'.format(path=artpath, name=artobj.name))
					if artobj.type == 'pdf':
						current = p('{path}pdf/{name}/'.format(path=artpath, name=artobj.name))
					error = current.error
					break;
			if error is None:
				art.append(current)

		ordered = []
		for z in range(len(sorted_list)-1, -1, -1): #sort files (newest -> oldest)
			for x in range(len(art)):
				if type(art[x]) is p:
					if art[x].pdfobj.name == epochtimes[sorted_list[z]]:
						ordered.append(art[x])
						break;
					continue;
				elif type(art[x]) is i:
					if '{name}.{ext}'.format(name=art[x].file.name, ext=art[x].file.ext) == epochtimes[sorted_list[z]]:
						ordered.append(art[x])
						break;
		return ordered

class art_api:
	def __init__(self, request):
		self.request = request
		self.resp_status = response_status()
		self.security = user_security(self.request)
		self.settings = self.request.registry.settings
		self.artpath = '{root}{uri}'.format(root=self.settings['htmlfolder'], uri=self.settings['art.uri'])
		self.pdfpath = '{path}pdf/'.format(path=self.artpath)
		self.filetypes = r'{regx}'.format(regx=self.settings['allowed_filetypes.images'])
		self.art = art_functions(request, self.artpath)
		self.files = self.art.get_objects(self.artpath)
		self.elements = art_elements(self.files, self.settings)
		self.time_now = datetime.now() #get time in datetime format for SQLAlchemy
		self.date = self.time_now.strftime('%S%M%H%y') #use datetime.strftime to get filename date

	def object_sort(self):
		dbinfo = self.request.dbsession.query(Art).all()
		for x in range(len(dbinfo)):
			fullpath = '{path}{name}'.format(path=self.artpath, name=dbinfo[x].name)
			if isfile(fullpath) and dbinfo[x].type != 'pdf':
				subprocess.call(['touch', '-t', dbinfo[x].uploadtime.strftime('%y%m%d%H%M.%S'), fullpath])
		return
	
	def store_file(self, filename, path):
		if movefile(
			filename,
			path, #src
			self.artpath #dst
		) is not None:
			self.add_clean(self.artpath)
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
			compress = imgcompress(img, 0.1, (900, 900), (1750, 1750)) #(image file, max file size, minimum dimensions, maximum dimensions)
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
			dbimage = Art(type='pdf', name=foldername, uploadtime=self.time_now)
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
			dbimage = Art(type='img', name=artname, uploadtime=self.time_now)
			self.request.dbsession.add(dbimage)
			self.request.dbsession.flush()
		except:
			return self.resp_status.warn(2)
		return self.resp_status.ok(1)

	def add(self):
		filenum = len(
			self.request.dbsession.query(Art).order_by(Art.id).all()
		)+1

		if self.security.isadmin is False:
			return self.resp_status.error()
		if self.request.POST['art-submit'] != 'artimg':
			return self.resp_status.error(10)
		if self.request.POST['art'] is None:
			return self.resp_status.error(10)

		filetype = re.search(self.filetypes, self.request.POST['art'].filename, re.IGNORECASE) 
		if filetype is None:
			return self.resp_status.error(2)
		filetype = filetype.group(1).lower()

		if filetype == 'pdf':
			return self.add_pdf(filenum)
		else:
			return self.add_image(filenum, filetype)
	
	def remove_pdf(self, art):
		if isdir(art.pdfobj.fullpath):
			subprocess.call(['rm', '-rf', art.pdfobj.fullpath])
		try:
			self.request.dbsession.query(Art).filter(
				Art.name==art.pdfobj.name
			).delete()
			self.request.dbsession.flush()
		except (NoResultFound, DataError):
			return self.resp_status.warn(2)
		return None

	def remove_img(self, art):
		thumb = '{path}{filename}-thumbnail.{ext}'.format(
			path=art.file.path,
			filename=art.file.name,
			ext=art.file.ext
		)
		if isfile(thumb): #figure out if the thumbnail exists and delete it
			subprocess.call(['rm', '-f', thumb])
		if isfile(art.file.fullpath):
			subprocess.call(['rm', '-f', art.file.fullpath])
		try:
			self.request.dbsession.query(Art).filter(
				Art.name=='{filename}.{ext}'.format(
					filename=art.file.name,
					ext=art.file.ext
				)
			).delete()
			self.request.dbsession.flush()
		except (NoResultFound, DataError):
			return self.resp_status.warn(2)
		return None

	def remove(self):
		art = thumb = None

		if self.request.POST['art-submit'] is None:
			return self.resp_status.error(10)
		
		artnum = re.search(r'(?:artdel|pdfobj_del)(\d+)', self.request.POST['art-submit']) #check and retrieve the filename from the request
		if artnum is None:
			return self.resp_status.error(10)
		artnum = int(artnum.group(1))
		
		for x in self.files:
			if type(x) is i or type(x) is p:
				if x.number == artnum:
					art = x
					break;
		if not art:
			return self.resp_status.error(6)

		result = None
		if type(art) is p:
			result = self.remove_pdf(art)
		if type(art) is i:
			result = self.remove_img(art)
		if result:
			response = result
		else:
			response = self.resp_status.ok(2)
			response.text = response.text.format(number=artnum)
		return response
