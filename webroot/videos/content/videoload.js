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

/*
if you're reading this well buckle up for a little story about how much
I loathe chrome browser and its ridiculous little bugs.
So the other day, (todays date, 05-20-2018) my friend (who owns
bigwebsite / tells me what to program for this site) started showing
me pictures of the youtube iframes for the /videos page completely
ignoring the z-index of the page and just displaying over everything
when played, including the pretty borders that Dylan uploads for his
videos. This only happens on chrome, the later versions to be
precise. I have a version of chromium under chrome 54 for backwards
compatibility; this problem does not occur on that, so I didn't
initially notice. I went downloaded chrome and... surprise!! I got
the problem to re-occur. I then did a lot of searching, and I pretty
much came out empty handed. All the tricks that worked for a lot of
people seem to be outdated and didn't work anymore. I just couldn't
get this bug to go away. I then tried using youtube's embed API
(code above) to see if it would fix the problem if I didn't directly
link an embed url to the iframe. (mind you, I wanted this part of
the site to have no scripts) I then had to edit quite a few things
and basically remove that no-script compatibility just to see
that... the videos STILL ignore my z-index and display on top. I
then spent a lot of time trying to figure out when this bug even
occurs because now, to me at least, its starting to look like a bug
in chrome. I noticed pretty quickly that any video out of view when
the page loads has this bug occur. If I scrolled so that all videos
were in view the bug did not occur. If I reload the page from the
bottom and scroll up, the first video that was out of view has the
problem. Vice versa if you reload at the top. After that, I pretty
threw up my hands a said "well, theres one last thing I can try". I
then played a video and then changed the body height to 0% in the
stylesheet. To my amazement, it worked, the video stopped playing on
top of the border. The code below does exactly this, only for
chrome. All it does is when the video is played, it changed the body
to 0 then 100, just to get the video to display underneath the image
borders.
*/

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
