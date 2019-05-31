from ..include.data.image import *

class filename(fname): #inhereted from data/filename.py
	def get_imgname(self):
		if self.name is None:
			return self.setnone(5)
		output = re.search(r'(.*)(?:\.)(jpeg|jpg|gif|png|bmp|webp)', self.name, re.IGNORECASE) #clean up the file name
		if output is not None:
			self.ext = output.group(2)
			self.name = output.group(1)
			output = re.search(r'(?:\d{8}art)?(?:\d+)?(?:-thumbnail)?(\d+|thumbnail)', self.name, re.IGNORECASE)
			if output is not None:
				if output.group(1) == 'thumbnail':
					self.number = 0
					return
				self.number = int(output.group(1))
				return
			return self.setnone(4)
		self.setnone(3)
	
	def get_imgnum(self):
		if self.error is None:
			return self.number

class image:
	def __init__(self, fullpath, openfile=False):
		self.type = 'img'
		self.error = self.loadedimage = None
		self.fullpath = fullpath
		self.file = filename(fullpath)
		self.file.get_imgname()
		self.number = self.file.get_imgnum()
		if self.file.name is not None:
			if openfile is True:
				self.loadedimage = pilimage.open(self.fullpath)
			return
		else:
			self.error = self.file.error
		#if file.name is None set all to None
		self.fullpath = self.file = self.loadedimage = None
