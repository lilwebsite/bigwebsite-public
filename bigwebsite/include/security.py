from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import (
	Allow,
	Deny,
	Everyone,
	Authenticated,
	remember,
	forget
)
from pyramid.httpexceptions import (
	HTTPFound,
	HTTPUnauthorized
)
from pyramid.renderers import render_to_response
from ..models import User
Admin = 'system.Admin' #special permission
