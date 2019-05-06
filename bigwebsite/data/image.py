from ..include.data.image import *

class image:
	def __init__(self, fullpath, openfile=False):
		self.error = self.loadedimage = None
		self.fullpath = fullpath
		self.file = fname(fullpath)
		self.file.get_imgname()
		if self.file.name is not None:
			if openfile is True:
				self.loadedimage = pilimage.open(self.fullpath)
			return
		else:
			self.error = self.file.error
		#if file.name is None set all to None
		self.fullpath = self.file = self.loadedimage = None
