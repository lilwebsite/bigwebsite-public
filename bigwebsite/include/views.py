from pyramid.response import Response
from pyramid.view import view_config

from pyramid.httpexceptions import (
	HTTPForbidden,
	HTTPNotFound,
	HTTPOk
)

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import (
	DBAPIError,
	DataError
)

from sqlalchemy import (
	update,
	Table
)

from bigwebsite.data.switch import switch as sw
