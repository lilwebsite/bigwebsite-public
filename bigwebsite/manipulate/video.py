from bigwebsite.include.manipulate.video import *
from bigwebsite.include.debug import *

def genthumbnail(border, thumb, ytsrc, settings):
	colors = 128
	def get_newsize(x, y):
		return (
			border.loadedimage.size[0],
			int((x / y) * border.loadedimage.size[0])
		)
	
	#save border with specified compression
	border.loadedimage = border.loadedimage.convert(mode='P', colors=colors)
	border.loadedimage.save(border.fullpath)

	#get the youtube thumbnail
	sddefault = bytesio(subprocess.check_output([
		'curl',
		'-sG',
		'--output',
		'-',
		'http://i3.ytimg.com/vi/{ytsrc}/sddefault.jpg'.format(ytsrc=ytsrc)
	]))
	try:
		sddefault = pilimage.open(sddefault)
	except:
		return 1 #retrieving sddefault failed
	
	#calculate the new width of the image, while keeping the ratio
	if sddefault.size[1] > sddefault.size[0]:
		newsize = get_newsize(sddefault.size[0], sddefault.size[1])
	else:
		newsize = get_newsize(sddefault.size[1], sddefault.size[0])
	sddefault = sddefault.resize(newsize, pilimage.LANCZOS) #resize sddefault to the border size
	sddefault = sddefault.convert('RGBA') #convert to RGBA so we can use alpha_composite on the border and the thumbnail
	
	#if thumbnail height is greater than border height it needs to be cropped then resized so they have equal dimensions
	if sddefault.size[1] > border.loadedimage.size[1]:
		diff = int((sddefault.size[1] - border.loadedimage.size[1]) / 2) #gets the amount of space to crop
		sddefault = sddefault.crop((0, diff, sddefault.size[0], sddefault.size[1]-diff))
		sddefault = sddefault.resize(border.loadedimage.size, pilimage.LANCZOS) #resize to compensate for the crop
	
	thumbnail = pilimage.alpha_composite(sddefault, border.loadedimage.convert('RGBA')) #place the sddefault under the border
	#place the custom play button on top of the thumbnail
	play = pilimage.open('{workfiles}play.png'.format(workfiles=settings['workfiles']))
	sizeto = int(thumbnail.size[0]/10) #the play button should be one tenth in width/height of the border width
	play = play.resize((sizeto, sizeto), pilimage.LANCZOS)
	play_position = ( #get the center of the image
		int((thumbnail.size[0]/2)-(sizeto/2)),
		int((thumbnail.size[1]/2)-(sizeto/2))
	)
	thumbnail.alpha_composite(play, play_position)

	#save and close the thumbnail, so we can use our image compression function safely
	thumbnail.convert('RGB').save(thumb)
	thumbnail.close()

	thumbnail = i(thumb, True)
	compress = imgcompress(thumbnail, 0.1, (600, 600), (1100, 1100)) #generate compression object
	try: #try compressing the image
		compress.compress_image()
	except:
		return 2
	
	return None
