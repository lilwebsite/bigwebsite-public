//most of this is pulled from the yt embed API reference. 
//I shortened a couple variable names and added a variable
//generator for each iframe

window.onload = function(){
	window.tag = document.createElement('script');
	tag.src = 'https://www.youtube.com/iframe_api';
	window.firsttag = document.getElementsByTagName('script')[0];
	firsttag.parentNode.insertBefore(tag, firsttag);

	window.iframes = document.getElementsByClassName('ytframe');
	window.videoid = [];
	window.iframeid = [];

	for (x = 0; x < iframes.length; x++){
		videoid[x] = iframes[x].attributes.ytsrc.value;
		iframeid[x] = 'iframe' + x;
		iframes[x]['id'] = iframeid[x];
	}
}

function onYouTubeIframeAPIReady(){
	for (x = 0; x < iframes.length; x++){
		window[iframeid[x]] = new YT.Player(iframeid[x], {
			height: '46vw',
			width: '80vw',
			videoId: videoid[x],
			playerVars: {
				'origin': 'https://www.bigwebsite.cool',
				'autoplay': 0,
				'controls': 0,
				'modestbranding': 1,
				'rel': 0,
				'showinfo': 0,
				'widget_referrer': 'bigwebsite.cool'
				},
			events: {
				'onStateChange': onPlayerStateChange
			}
		});
	}
}

function fixbutton(iframe){
	setTimeout(function(){iframe.style.display = 'none'}, 15);
	setTimeout(function(){iframe.style.display = 'initial'}, 20);
}

function fixzindex(){
	setTimeout(function(){document.body.style.height = '0%'}, 15);
	setTimeout(function(){document.body.style.height = '100%';}, 20);
	//make double sure chrome isn't messing with it anymore
	setTimeout(function(){document.body.style.height = '0%'}, 1215);
	setTimeout(function(){document.body.style.height = '100%';}, 1220);
}

function onPlayerStateChange(event){
	if(event.data == YT.PlayerState.PLAYING){
		chrome = /Chrome\/[\d\S]+/g;
		result = chrome.exec(window.navigator.appVersion);
		//below is to work out a bug where the player 
		//won't remove the youtube play button when
		//the video starts playing. doesn't happen in
		//chrome
		if(result === null){
			fixbutton(event.target.a);
		//below is to fix z-index problem
		}else if(result !== null){
			fixzindex();
		}
	}
}
