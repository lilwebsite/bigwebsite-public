from bigwebsite.include.manipulate.image import *

def set_mode_rgb(image=None):
	if not image:
		return image
	try:
		image = image.convert(mode='RGB') #make sure that our image is able to be saved as JPEG
	except:
		return OSError
	return image

def get_size(tempfile=None):
	if not tempfile:
		return None
	tempfile.save('/tmp/tempimage.jpg', 'JPEG')
	pipe = subprocess.Popen(['cat', '/tmp/tempimage.jpg'], stdout=subprocess.PIPE)
	size = subprocess.check_output(['wc', '-c'], stdin=pipe.stdout).decode('UTF-8')
	return float(size) / 1000000

def solve_compression(image=None, size_limit=None, min_limit=None, max_limit=None, mode='RGB'): #returns compression number
	if not image or not size_limit or not min_limit or not max_limit:
		return None
	x = 1 #starting at 1 will check if the default height / width is OK
	increment = False #increment and loop makes sure that we don't get stuck in a infinite loop
	loop = 0
	tempfile = None
	def load_image():
		nonlocal tempfile
		nonlocal mode
		tempfile = pilimage.open(image.fullpath) #temporary manipulation
		tempfile.load()
		if mode == 'RGB' or tempfile.mode == 'P':
			tempfile = set_mode_rgb(tempfile)
	def reload_image():
		nonlocal tempfile
		tempfile.close()
		tempfile = None
		load_image()
	def increment_up():
		nonlocal increment
		nonlocal loop
		nonlocal x
		if increment == False:
			loop += 1
		increment = True
		x += 0.5
		reload_image()
	def increment_down():
		nonlocal increment
		nonlocal loop
		nonlocal x
		if increment == True:
			loop += 1
		increment = False
		x -= 0.5
		reload_image()
	load_image()
	while True:
		if loop > 3 or x <= 0:
			break;
		currentsize = (round(tempfile.size[0] / x), round(tempfile.size[1] / x))
		if currentsize[0] <= max_limit[0] or currentsize[1] <= max_limit[1]:
			if currentsize[0] >= min_limit[0] and currentsize[1] >= min_limit[1]:
				tempfile = tempfile.resize(currentsize, pilimage.LANCZOS)
				if get_size(tempfile) <= size_limit:
					return x
				increment_up()
			else:
				increment_down()
		else:
			increment_up()
	if x <= 0:
		return 1
	return x

class imgcompress:
	#if successful all functions return None
	def __init__(self, image, limit_size=0.1, limit_min=(600, 600), limit_max=(900, 900)):
		#limits are ratio independent, ex. (if W == 900 or H == 1000) True, (if W == 2000 or H == 1200) False
		self.limit_size = limit_size #max file size
		self.limit_max = limit_max #max height / width
		self.limit_min = limit_min #min height / width
		self.image = image #load an image object (specifically defined by bigwebsite/data/image)

	def compress(self, compression = 3, thumbnail = False, savetype = 'JPEG', mode='RGB', saveas=None):
		if not self.activefile:
			return None
		self.activefile.load()
		currentsize = self.activefile.size
		if mode == 'RGB' or self.activefile.mode == 'P':
			self.activefile	= set_mode_rgb(self.activefile)
		self.activefile = self.activefile.resize(
			(
				round(currentsize[0]/compression),
				round(currentsize[1]/compression)
			),
			pilimage.LANCZOS
		)
		previous = self.image.fullpath
		if self.image.file.ext.upper() is not savetype: #if the file extension is not jpeg, rename it
			current = '{path}{name}.{ext}'.format(path=self.image.file.path, name=self.image.file.name, ext=savetype.lower())
			rename(previous, current)
			self.image = i(current)
		if self.image.error is not None:
			return IOError
		if saveas is not None:
			self.activefile.save(saveas, savetype)
			return i(saveas)
		self.activefile.save(self.image.fullpath, savetype)
		return i(self.image.fullpath)

	def compress_pdf(self): #designed to compress images extracted from a pdf
		self.activefile = self.image.loadedimage
		return self.compress(
			solve_compression(
				self.image,
				self.limit_size,
				self.limit_min,
				self.limit_max,
				mode = 'any'
			),
			mode = 'any'
		)

	def generate_thumbnail(self):
		fp = '{path}{name}-thumbnail.jpeg'.format(path=self.image.file.path, name=self.image.file.name) #point to the desired file we want to generate
		self.activefile = pilimage.open(self.image.fullpath) #open and load original file
		self.activefile.load()
		self.activefile.save(fp, 'JPEG') #save original data to new thumbnail file
		self.image = i(fp, openfile=True) #now we can load the thumbnail file since it has been created
		if self.image.error is not None:
			return IOError
		self.activefile = self.image.loadedimage
		return self.compress(thumbnail=True)

	def compress_image(self):
		self.activefile = self.image.loadedimage
		return self.compress(
			solve_compression(
				self.image,
				self.limit_size,
				self.limit_min,
				self.limit_max
			)
		)
	
	def compress_default(self, saveas=None): #use saveas to define save path
		self.activefile = self.image.loadedimage
		return self.compress(mode='any', saveas=saveas)
