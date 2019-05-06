from inspect import getmembers
from sys import setprofile
import re

def list_members(obj):
	for x in getmembers(obj):
		if re.search(r'__.+__', x[0]) is None:
			print(x[0])
	
class callinfo:
	def __init__(self, tracefunc):
		self.tracefunc = tracefunc
		self.frame = None
		setprofile(self.trace)
	
	def trace(self, frame, event, arg):
		if event == 'call' and frame.f_code.co_name == self.tracefunc:
			self.frame = frame
			setprofile(None)
		return None
	
	def target_frame(self, funcname=None):
		if funcname is None:
			print('no funcname variable provided')
			return funcname
		tempframe = self.frame
		while True:
			if tempframe is None:
				print('"{func}" not in call stack'.format(func=funcname))
				break;
			if tempframe.f_code.co_name == funcname and tempframe.f_back is not None:
				tempframe = tempframe.f_back
				break;
			tempframe = tempframe.f_back
		return tempframe
	
	def get_line(self, funcname=None):
		if funcname is None:
			funcname = self.tracefunc
		lineno = self.target_frame(funcname)
		if lineno is not None:
			lineno = lineno.f_lineno
		return lineno
	
	def get_file(self, funcname=None):
		if funcname is None:
			funcname = self.tracefunc
		filename = self.target_frame(funcname)
		if filename is not None:
			filename = re.search(r'\w+\.py', filename.f_code.co_filename, re.IGNORECASE)
			if filename is not None:
				filename = filename.group(0)
		return filename

