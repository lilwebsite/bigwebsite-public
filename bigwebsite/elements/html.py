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
		self.border = img_element()
		self.thumb = img_element()
		self.frame = div_element()

	def set_frame_params(self, params, id):
		frame = self.frame.set_div_class_id('ytframe ytframe-nonvis', id)
		return frame.format(params=params)
	
	def set_border_src(self, uri, id): #sets the uri for the border image
		border = self.border.set_img_class_id('border border-nonvis', id)
		return border.format(uri=uri)

	def set_thumb_src(self, uri, id): #sets the uri for the thumbnail
		thumb = self.thumb.set_img_class_id('thumbnail thumbnail-vis', id)
		return thumb.format(uri=uri)

class img_element:
	img_class = '<img class="{classname}"'
	img_id = ' id="{idname}" '
	img_src = ' src="{uri}" />'
	
	def set_img_class_id(self, classname, idname):
		return element[1].format(
			begin = self.img_class.format(classname=classname),
			mid = self.img_id.format(idname=idname),
			end = self.img_src
		)

	def set_img_class(self, classname):
		return element[2].format(
			begin = self.img_class.format(classname=classname),
			end = self.img_src
		)

class div_element:
	close = '</div>'
	div_class_params = '<div class="{classname}" {params}>'
	div_class_id_params = '<div class="{classname}" id="{idname}" {params}>'

	def set_div_class_id(self, classname, idname):
		return element[2].format(
			begin = self.div_class_id_params.format(classname=classname, idname=idname, params=params),
			end = self.close
		)
	
	def set_div_class(self, classname):
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
