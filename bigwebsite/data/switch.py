class switch:
	def __init__(self, values, default):
		self.values = values
		self.default = default
	
	def get(self, value):
		return self.values.get(value, self.default)
