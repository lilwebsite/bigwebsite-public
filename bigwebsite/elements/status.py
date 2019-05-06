import bigwebsite.include.debug
from ..include.elements.status import *
status = s()

def resp_err(txt):
	return status.error.format(line='{line}', txt='ERROR -- > {txt}'.format(txt=txt))

def resp_warn(txt):
	return status.warning.format(txt='WARN -- > {txt}'.format(txt=txt))

def resp_ok(txt):
	return status.ok.format(txt=txt)

class response_status:
	def __init__(self):
		self.error_callinfo = ci('error') #creates a frame of the current call stack when response_status.error is called
		self.errors =\
		sw(
			values={#value comparison
				1: resp_err('Unknown failure. Contact admin.'),
				2: resp_err('Upload failed. Filetype not allowed. Rejected file [{filename}] for user [{username}]'),
				3: resp_err('Upload failed. File could not be loaded, internal read error.'),
				4: resp_err('Upload failed. File compression failed.'),
				5: resp_err('Filename format does not match binary format.'),
				6: resp_err('Failed to delete. File not found.'),
				7: resp_err('Failed to delete. Thumbnail file not found.'),
				8: resp_err('Failed to move file into web directory.'),
				9: resp_err('SQL failed.'),
				10: resp_err('Request sent is invalid. Contact admin.'),
				11: resp_err('Failed to move file into .cached directory')
			},
			default=Response('access denied')
		)
		self.warnings =\
		sw(
			values={
				1: resp_warn('failed to compress image'),
				2: resp_warn('SQL failed. Will not affect website.')
			},
			default=Response('unknown failure')
		)
		self.OK =\
		sw(
			values={
				1: resp_ok('Upload success.'),
				2: resp_ok('art{number} deleted successfully.')
			},
			default=Response('OK')
		)
	
	def error(self, num=0):
		if num != 0:
			line = 'L0:'
			if self.error_callinfo.frame is not None:
				line = '{filename}:L{line}:'.format(filename=self.error_callinfo.get_file(), line=self.error_callinfo.get_line())
			resp_text = self.errors.get(num).format(line=line)
			return Response(resp_text)
		return self.errors.get(num)

	def warn(self, num=0):
		return Response(self.warnings.get(num))
	
	def ok(self, num=0):
		return Response(self.OK.get(num))
