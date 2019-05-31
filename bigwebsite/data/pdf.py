from bigwebsite.include.data.pdf import *
from bigwebsite.data.image import image as i

class filename(fname): #inhereted from data/filename.py
	def get_pdfobj(self):
		if self.ok:
			self.name = re.search(r'(pdfobj\d+)', self.fullpath, re.I).group(1)
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

	def get_pdfnum(self):
		if self.error is None:
			return int(re.search(r'pdfobj(\d+)', self.name, re.I).group(1))

class pdf:
	def __init__(self, fullpath):
		self.type = 'pdf'
		self.error = None
		self.pdfobj = filename(fullpath, True)
		self.pdfobj.get_pdfobj()
		self.number = self.pdfobj.get_pdfnum()
		if self.pdfobj.images:
			return
		else:
			self.error = self.pdfobj.error
		self.fullpath = self.pdfobj = None
