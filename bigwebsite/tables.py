from bigwebsite.include.tables import *

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(Text, nullable=False, unique=True)
	password = Column(Text, nullable=False, unique=True)
	permission = Column(Integer)

	def create_user(self, password):
		self.password = bcrypt.encrypt(password.encode('utf8'))

	def validate_password(self, password):
		if self.password is not None:
			expected_hash = self.password
			return bcrypt.verify(password.encode('utf8'), self.password)
		return False

	def __repr__(self):
		return "[[User]]\tusername='{username}', permission='{permission}'".format(
			username=self.username,
			permission=self.permission
		)

class Art(Base):
	__tablename__ = 'art'

	id = Column(Integer, primary_key=True)
	type = Column(Text(3), nullable=False)
	name = Column(Text(30), nullable=False, unique=True)
	uploadtime = Column(DateTime, nullable=False, unique=True)
	cached = Column(Boolean(create_constraint=False), nullable=False)

	def __repr__(self):
		return "\n[[Art]]\ttype='{type}', name='{name}', uploadtime='{upload}', cached='{cached}'".format(
			type = self.type,
			name = self.name,
			upload = self.uploadtime,
			cached = self.cached
		)

class Video(Base):
	__tablename__ = 'video'

	id = Column(Integer, primary_key=True)
	name = Column(Text(30), nullable=False, unique=True)
	ytid = Column(Text(15), nullable=False, unique=True)
	cached = Column(Boolean(create_constraint=False), nullable=False)

	def __repr__(self):
		return "\n[[Video]]\tname='{name}', ytid='{ytid}', cached='{cached}'".format(
			name = self.name,
			ytid = self.ytid,
			cached = self.cached
		)

class AdminPage(Base):
	__tablename__ = 'adminpage'

	id = Column(Integer, primary_key=True)
	unsorted = Column(Boolean(create_constraint=False), nullable=True)

	def __repr__(self):
		return "\n[[AdminPage]]\tunsorted='{unsorted}'".format(unsorted = self.unsorted)
