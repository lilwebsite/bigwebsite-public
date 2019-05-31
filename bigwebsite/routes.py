from .include.security import (
	Allow,
	Deny,
	Everyone,
	Authenticated,
	Admin
)

def includeme(config):
	#restricted access
	config.add_static_view('restricted', 'bigwebsite:restricted', cache_max_age=900, permission='admin') #add_static_view(name, path, cache_max_age, permission)
	#general content delivery
	config.add_static_view('scripts', 'bigwebsite:scripts')
	#restricted admin pages 
	config.add_route('logout', '/logout')
	config.add_route('adminpage', '/adminpage')
	config.add_route('videolist', '/adminpage/videolist')
	config.add_route('artlist', '/adminpage/artlist')
	#js website
	config.add_route('home', '/')
	config.add_route('videos', '/videos')
	config.add_route('videoquery', '/videos/query')
	config.add_route('videocontainers', '/videos/containers')
	config.add_route('contact', '/contact')
	config.add_route('about', '/about')
	config.add_route('demands', '/about/demands')
	config.add_route('art', '/art')
	config.add_route('artquery', '/art/query')
	config.add_route('artcontainers', '/art/containers')
	config.add_route('music', '/music')
	#noscript website
	config.add_route('noscript', '/noscript')
	config.add_route('noscript-videos', '/noscript/videos')
	#DEVELOPMENT
	config.add_route('test', '/test')
	config.add_route('devtest', '/devtest')
