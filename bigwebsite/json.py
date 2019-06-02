from bigwebsite.web.art import art_api as art
from bigwebsite.web.video import video
from bigwebsite.data.switch import switch as sw

class view_json:
	def __init__(self, request):
		self.request = request
		self.video = video(request)
		self.art = art(request)
		self.art_limit = 12
		self.video_limit = 4
		self.music_limit = 5
		self.reqtypes =\
		sw(
			values={
				0: 'art',
				1: 'video',
				2: 'music'
			},
			default=['error']
		)

	def error(self):
		return ['error']

	def query(self):
		response = []
		if self.request.params:
			#get the type of request first
			if not 'type' in self.request.POST:
				return self.error()
			reqtype = int(self.request.POST['type'])
			if type(reqtype) is not int:
				return self.error()
			reqtype = self.reqtypes.get(reqtype)

			if type(reqtype) is list:
				return self.error()

			if 'getlimit' in self.request.POST:
				if reqtype == self.reqtypes.get(0): #art
					response.append(self.art_limit)
				if reqtype == self.reqtypes.get(1): #video
					response.append(self.video_limit)
				return response

			if 'setlimit' in self.request.POST:
				limit = int(self.request.POST['setlimit'])
				if type(limit) is int:
					if reqtype == self.reqtypes.get(0): #art
						self.art_limit = limit
					if reqtype == self.reqtypes.get(1): #video
						self.video_limit = limit

			if 'query' in self.request.POST:
				num = int(self.request.POST['query'])
				if type(num) is int:
					count = 0
					reqlength = reqtarget = None

					if reqtype == self.reqtypes.get(0): #art
						reqlength = len(self.art.files)
						reqtarget = self.art.elements.html()
					if reqtype == self.reqtypes.get(1): #video
						reqlength = len(self.video.elements.html())
						reqtarget = self.video.elements.html()

					if not reqlength or not reqtarget:
						return self.error()
					response.append(reqlength)
					for element in reqtarget:
						if count >= num:
							break;
						if reqtype == self.reqtypes.get(0):
							art_type = element['type']
							info = {'type': art_type}
							if art_type == 'img':
								info['uri'] = element['thumb_uri']
								info['img'] = element['uri']
							if art_type == 'pdf':
								info['uri'] = element['uri']
								info['pdf'] = element['pdfobj']
						if reqtype == self.reqtypes.get(1):
							info = element
						if not info:
							continue
						response.append(info)
						count += 1
			return response
