from bigwebsite.include.data.pdf import *
from bigwebsite.data.image import image as i

class filename: #inhereted from data/filename.py
	def get_pdfobj(self):
		if self.ok:
			dir_output = subprocess.check_output(['ls', self.fullpath]).decode('UTF-8').split('\n')
			files = len(dir_output)-2 #-1 for extra entry from split, -1 for the thumbnail file
			self.images = []
			for x in range(files):
				imgpath = '{fullpath}{num}.jpeg'.format(
					fullpath = self.fullpath,
					num = x
				)
				self.images.append(i(imgpath))
				if self.images[len(self.images)-1].error is not None:
					return self.setnone(3)
			self.images.append(i('{fullpath}thumbnail.jpeg'.format(fullpath=self.fullpath)))

class pdf:
	def __init__(self, fullpath):
		self.error = None
		self.fullpath = fullpath
		self.pdfobj = filename(fullpath)
		self.pdfobj.get_pdfobj()
		if self.pdfobj.images:
			return
		else:
			self.error = self.pdfobj.error
		self.fullpath = self.pdfobj = None
