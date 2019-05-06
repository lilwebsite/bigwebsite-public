import re
import subprocess
import pdb

class filename:
	def __init__(self, fullpath):
		self.fullpath = fullpath
		self.path = '/'
		self.error = self.name = None
		self.ok = False
		output = subprocess.check_output(['namei', self.fullpath]).decode('UTF-8') #individualize directories and files with namei
		output = re.findall(r'(?: ?(f|d|l|s|b|c|p|-|\?):? (.*))', output, re.MULTILINE)
		for x in range(len(output)):
			if output[x][0] == '-':
				self.name = output[x][1]
			if output[x][0] == 'd' and output[x][1] != '/':
				self.path += '{d}/'.format(d=output[x][1])
		if self.name:
			if re.search(r'no such file or directory', self.path + self.name, re.IGNORECASE) is None:
				return self.setok()
			return self.setnone(2)
		self.setnone(1)
	
	def setok(self):
		self.ok = True

	def setnone(self, error):
		self.error = error
		#if finding the file failed set all to None
		self.path = self.name = self.ext = self.number = self.images = None

	def get_imgname(self):
		if self.name is None:
			return self.setnone(5)
		output = re.search(r'(.*)(?:\.)(jpeg|jpg|gif|png|bmp|webp)', self.name, re.IGNORECASE) #clean up the file name
		if output is not None:
			self.ext = output.group(2)
			self.name = output.group(1)
			output = re.search(r'(?:\d{7}art)(?:-thumbnail)?(\d+)', self.name, re.IGNORECASE)
			if output is not None:
				self.number = int(output.group(1))
				return
			return self.setnone(4)
		self.setnone(3)
