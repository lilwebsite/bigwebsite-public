from bigwebsite.include.manipulate.pdf import *

def extract_pdf_objects(pdf, subtype='/Image'):
	if pdf is None or type(pdf) is not BufferedReader:
		raise TypeError
	try:
		pdf = pypdf.PdfFileReader(pdf)
	except:
		print('failed to open pdf file')
		raise OSError

	page = []
	for x in range(pdf.getNumPages()):
		page.append(pdf.getPage(x))

	xobjs = []
	for x in range(len(page)):
		xobjs.append(page[x]['/Resources']['/XObject'])

	image = []
	for entry in xobjs:
		for key,val in entry.items():
			xobject = entry[key]
			if xobject['/Subtype'] == subtype:
				image.append(xobject)
	return image

def xobj2image(image):
	def isobj(obj):
		if '/Subtype' not in obj or obj['/Subtype'] != '/Image':
			raise TypeError

	def loadimg(obj):
		data = BytesIO(obj._data)
		return pilimage.open(data)

	if type(image) is list:
		for o in image:
			isobj(o)
	else:
		isobj(image)

	if type(image) is list:
		loaded = []
		for o in image:
			loaded.append(loadimg(o))
	else:
		loaded = loadimg(image)
	return loaded

#pdf2images(open('file.pdf', 'rb'))
def pdf2images(pdf):
	pdf_images = extract_pdf_objects(pdf)
	return xobj2image(pdf_images)
