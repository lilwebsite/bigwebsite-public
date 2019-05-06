from os.path import (
	isdir,
	isfile
)
import shutil

def movefile(filename, src, dst):
	error = None
	if isdir(src) and isdir(dst):
		if isfile(src + filename):
			try:
				shutil.move(src + filename, dst + filename)
			except:
				error = 2
				print('shutil.move failed')
	else:
		error = 1
		print('failed to move file {dst}{filename}'.format(dst=dst, filename=filename))
	return error
