window.YTloaded = false;
window.currentVideo = new Object();
currentVideo.thumbnail =
currentVideo.ytframe =
currentVideo.border =
currentVideo.html = undefined;
currentVideo.loaded = false;

function setclass(target){
	info = new Object();
	info.group = target;
	info.type_vis = info.group + '-vis';
	info.type_nonvis = info.group + '-nonvis';
	return info;
}

window.classes = {
	thumbnail: setclass('thumbnail'),
	ytframe: setclass('ytframe'),
	border: setclass('border')
};

function scan4id(targetID, targetList){
	for(x = 0; x < targetList.length; x++){
		if(targetList[x].id == targetID)
		{return targetList[x];}
	}
	return undefined;
}

function getYTframeById(target)
{return scan4id(target, window.iframes);}

function getThumbnailById(target)
{return scan4id(target, window.thumbnails);}

function getBorderById(target)
{return scan4id(target, window.borders);}

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

function unloadVideo(){
	if(!currentVideo.loaded)
	{return;}
	currentVideo.thumbnail.className = `${classes.thumbnail.group} ${classes.thumbnail.type_vis}`;
	currentVideo.border.className = `${classes.border.group} ${classes.border.type_nonvis}`;
	currentVideo.ytframe.className = `${classes.ytframe.group} ${classes.ytframe.type_nonvis}`;
	currentVideo.ytframe.a.outerHTML = currentVideo.html;
}

function loadVideo(){
	if(!currentVideo.loaded)
	{return;}
	currentVideo.thumbnail.className = `${classes.thumbnail.group} ${classes.thumbnail.type_nonvis}`;
	currentVideo.border.className = `${classes.border.group} ${classes.border.type_vis}`;
	currentVideo.ytframe.className = `${classes.ytframe.group} ${classes.ytframe.type_vis}`;
	currentVideo.ytframe.id = 'current_video'
	currentVideo.ytframe = new YT.Player('current_video', {
		height: '46vw',
		width: '80vw',
		videoId: currentVideo.ytframe.attributes.ytsrc.value,
		playerVars: {
			'origin': `https://${location.host}`,
			'autoplay': 0,
			'controls': 0,
			'modestbranding': 1,
			'rel': 0,
			'showinfo': 0,
			'widget_referrer': location.host
			},
		events: {'onReady': function(){
			currentVideo.ytframe.playVideo();
		}}
	});
}

function onYouTubeIframeAPIReady(){
	loadVideo();
	YTloaded = true;
}

function initYTscripts(){
	if(YTloaded){return;}
	window.tag = document.createElement('script');
	tag.src = 'https://www.youtube.com/iframe_api';
	window.firsttag = document.getElementsByTagName('script')[0];
	firsttag.parentNode.insertBefore(tag, firsttag);
}

function initPage(){
	window.iframes = document.getElementsByClassName('ytframe');
	window.thumbnails = document.getElementsByClassName('thumbnail');
	window.borders = document.getElementsByClassName('border');
	for(x = 0; x < thumbnails.length; x++){
		thumbnails[x].addEventListener('click', function(){
			if(currentVideo)
			{unloadVideo();}
			currentVideo.thumbnail = this;
			currentVideo.ytframe = getYTframeById(this.id);
			currentVideo.border = getBorderById(this.id);
			currentVideo.html = currentVideo.ytframe.outerHTML;
			currentVideo.loaded = true;
			if(!YTloaded)
			{return initYTscripts();}
			loadVideo();
		});
	}
}
