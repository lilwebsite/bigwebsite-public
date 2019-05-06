window.onload = function(){
	document.getElementById('videos-svg').getSVGDocument().getElementById('svg').addEventListener('click', function(){
		window.location = window.location + 'videos'
	}, false);
	document.getElementById('contact-svg').getSVGDocument().getElementById('svg').addEventListener('click', function(){
		window.location = window.location + 'contact'
	}, false);
	document.getElementById('about-svg').getSVGDocument().getElementById('svg').addEventListener('click', function(){
		window.location = window.location + 'about'
	}, false);
	document.getElementById('art-svg').getSVGDocument().getElementById('svg').addEventListener('click', function(){
		window.location = window.location + 'art'
	}, false);
	document.getElementById('music-svg').getSVGDocument().getElementById('svg').addEventListener('click', function(){
		window.location = window.location + 'music'
	}, false);
};
