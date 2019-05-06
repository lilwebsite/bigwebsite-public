#this document is an html assembler. it preloads certain elements for jinja2 to use
#all set_* functions return the formatted html, even if its not required
element = [ #element formats
	'{begin}{line}{mid}{end}',
	'{begin}{mid}{end}',
	'{begin}{end}'
]
txt = '{txt}' #placeholder for external text
line = '{line}' #placeholder for sepcifying what line an error occured
params = '{params}' #placeholder for additional element values (for the DOM)

class video_element:
	def __init__(self):
		border = img_element()
		frame = div_element()
		self.border = border.set_imgclass('border')
		#youtube stuff
		frame = frame.set_divclass('ytframe')
		ytsrc = 'ytsrc="{ytsrc}"'

	def set_frame_params(self, params):
		self.frame = self.frame.format(params=params)
		return self.frame
	
	def set_border_src(self, uri): #sets the uri for the border image
		self.border = self.border.format(uri=uri)
		return self.border

class img_element:
	img_class = '<img class="{classname}"'
	img_src = ' src="{uri}" />'
	
	def set_imgclass(self, classname):
		return element[2].format(
			begin = self.img_class.format(classname=classname),
			end = self.img_src
		)

class div_element:
	close = '</div>'
	div_class_params = '<div class="{classname}" {params}>'
	
	def set_divclass(self, classname):
		return element[2].format(
			begin = self.div_class_params.format(classname=classname, params=params),
			end = self.close
		)

class p_element:
	close = '</p>'
	status = '<p style="color: {color}">'

	def set_status_error(self, color):
		return element[0].format(
			begin = self.status.format(color=color),
			line = line,
			mid = txt,
			end = self.close
		)
	
	def set_status(self, color):
		return element[1].format(
			begin = self.status.format(color=color),
			mid = txt,
			end = self.close
		)

class status:
	def __init__(self):
		p = p_element()
		self.error = p.set_status_error('red')
		self.warning = p.set_status('orange')
		self.ok = p.set_status('green')
