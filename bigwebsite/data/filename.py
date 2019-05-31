import re
import subprocess
from os.path import (isfile, isdir)

class filename:
	def __init__(self, fullpath, directory = False):
		self.fullpath = fullpath
		self.path = '/'
		self.error = self.name = None
		self.ok = False
		if not isfile(self.fullpath) and not isdir(self.fullpath):
			return self.setnone(6)
		output = subprocess.check_output(['namei', self.fullpath]).decode('UTF-8') #individualize directories and files with namei
		output = re.findall(r'(?: ?(f|d|l|s|b|c|p|-|\?):? (.*))', output, re.MULTILINE)
		for x in range(len(output)):
			if output[x][0] == '-':
				self.name = output[x][1]
			if output[x][0] == 'd' and output[x][1] != '/':
				self.path += '{d}/'.format(d=output[x][1])
		nofile = r'no such file or directory'
		if self.name or directory:
			if not directory:
				if re.search(nofile, self.path + self.name, re.I) is None:
					return self.setok()
			else:
				if re.search(nofile, self.path, re.I) is None:
					return self.setok()
			return self.setnone(2)
		self.setnone(1)
	
	def setok(self):
		self.ok = True

	def setnone(self, error):
		self.error = error
		#if finding the file failed set all to None
		self.path = self.name = self.ext = self.number = self.images = None
