from bigwebsite.include.security import *

class RootFactory:
	__acl__ = [
		(Allow, Admin, 'admin'),
		(Deny, Everyone, 'admin'),
		(Allow, Authenticated, 'view'),
		(Deny, Everyone, 'view'),
		(Deny, Authenticated, 'login'),
		(Deny, Admin, 'login'),
		(Allow, Everyone, 'login')
	]

	def __init__(self, request):
		self.request = request

class AuthenticationPolicy(AuthTktAuthenticationPolicy):
	def authenticated_userid(self, request):
		user = request.user
		if user is not None:
			print('[authenticated]: {url} for user {user}'.format(url=request.url, user=request.user.username))
			return user.id
		print('[warning]: unauthenticated request made for {url}'.format(url=request.url))
		return None

def get_user(request):
	user_id = request.unauthenticated_userid
	if user_id is not None:
		user = request.dbsession.query(User).get(user_id)
		if user is not None:
			print(user)
			return user

def get_principals(userid, request):
	if request.user is None:
		return []
	if request.user.permission is 1:
		return [Admin]
	return []

def includeme(config):
	settings = config.get_settings()
	config.set_root_factory(RootFactory)
	config.set_authentication_policy(
		AuthenticationPolicy(
			secret=settings['auth.secret'],
			domain=settings['hostname'],
			hashalg='sha512',
			callback=get_principals,
			secure=True,
			http_only=True,
			wild_domain=False,
			parent_domain=True,
			samesite='strict',
			timeout=900,
			reissue_time=900,
			max_age=900
		)
	)
	config.set_authorization_policy(ACLAuthorizationPolicy())
	config.add_request_method(get_user, 'user', reify=True)

class user_security:
	def __init__(self, request):
		self.request = request
		self.settings = self.request.registry.settings
		self.user = request.user
		self.adminpage = 'https://{host}/adminpage'.format(host=self.settings['hostname'])

	def logout(self):
		return HTTPFound(location=self.adminpage, headers=forget(self.request))

	def login(self):
		status = 403
		if 'form-submit' in self.request.params:
			login = self.request.params['login']
			password = self.request.params['password']
			self.user = self.request.dbsession.query(User).filter(User.username==login).one_or_none()
			if self.user is not None and self.user.validate_password(password):
				headers = remember(self.request, self.user.id)
				response = HTTPFound(location=self.adminpage, headers=headers)
				return response
			status = 401
		response = render_to_response(
			renderer_name = 'bigwebsite:templates/adminpage.jinja2',
			value = {'page': 'login'}
		)
		response.status = status
		return response

	def isloggedin(self):
		if self.request.authenticated_userid is not None:
			return True
		return False

	def isadmin(self):
		if self.request.authenticated_userid is not None and self.request.user.permission == 1:
			return True
		return False
