var contents = [$('#videocontainer')[0], $('#artcontainer')[0], $('#settingscontainer')[0]];
var loading = '<p style="color: yellow">uploading...</p>'

function handleResponse(resp){
	if(resp.status == 403)
	{window.location.href = 'logout';}
}

function refreshVideos(){
	$.ajax({
		type: 'GET',
		url: window.location.href + '/videolist'
	}).done(function(resp){
		$('#videodelete').html(resp);
	}).always(function(response){
		handleResponse(response);
	});
}

function refreshArt(){
	$.ajax({
		type: 'GET',
		url: window.location.href + '/artlist'
	}).done(function(resp){
		$('#artdelete').html(resp);
	}).always(function(response){
		handleResponse(response);
	});
}

function buttonSelect(button){
	if(button.style.background === ''){
		button.style.background = '#BDBDBD';
		button.style.color = 'black';
	}
	tabs = $('.tab');
	for(x = 0; x < tabs.length; x++){
		if(tabs[x] != button){
			tabs[x].style.background = '';
			tabs[x].style.color = '';
		}
	}
}

function contentSelect(contentid){
	for(x = 0; x < contents.length; x++){
		if(contents[x].attributes.id.value !== contentid.value){
			contents[x].style.display = 'none';
		}else{
			contents[x].style.display = 'inline-block';
		}
	}
}

function switchTabs(target){
	buttonSelect(target);
	contentSelect(target.attributes.contentid);
}

$('#formytadd').on('submit', function(event){
	event.preventDefault();
	videoadd = new FormData($(this)[0]);
	videoadd.append('video-submit', 'videourl');
	$('#videoadd-result').html(loading);
	$.ajax({
		type: 'POST',
		url: window.location.href,
		data: videoadd,
		cache: false,
		processData: false,
		contentType: false
	}).done(function(response){
		$('#videoadd-result').html(response);
		refreshVideos();
	}).always(function(response){
		handleResponse(response);
	});
});

$('#videodelete').on('submit', '.videodelete', function(event){
	event.preventDefault();
	videodel = new FormData();
	videodel.append('video-submit', $(this).children('button')[0].value);
	$.ajax({
		type: 'POST',
		url: window.location.href,
		data: videodel,
		cache: false,
		processData: false,
		contentType: false
	}).done(function(response){
		$('#videodel-result').html(response);
		refreshVideos();
	}).always(function(response){
		handleResponse(response);
	});
});

$('#formartadd').on('submit', function(event){
	event.preventDefault();
	artadd = new FormData($(this)[0]);
	artadd.append('art-submit', 'artimg');
	file = $(this)[0][0];
	if(file != undefined){
		$('#artadd-result').html(loading);
		$.ajax({
			type: 'POST',
			url: window.location.href,
			data: artadd,
			cache: false,
			processData: false,
			contentType: false
		}).done(function(response){
			$('#artadd-result').html(response);
			refreshArt();
		}).always(function(response){
			handleResponse(response);
		});
	}
});

$('#artdelete').on('submit', '.artdelete', function(event){
	event.preventDefault();
	artdel = new FormData();
	artdel.append('art-submit', $(this).children('button')[0].value);
	$.ajax({
		type: 'POST',
		url: window.location.href,
		data: artdel,
		cache: false,
		processData: false,
		contentType: false
	}).done(function(response){
		$('#artdel-result').html(response);
		refreshArt();
	}).always(function(response){
		handleResponse(response);
	});
});

function tabCallback(event){
	switchTabs(this);
};

$('#arttab').on('click', tabCallback);

$('#videostab').on('click', tabCallback);

$('#settingstab').on('click', tabCallback);

$('#info-checksort').on('click', function(event){
	bubble = $('#checksort-bubble')[0];
	if(bubble.style.display === 'none'){
		bubble.style.display = 'inline-block';
	}else{
		bubble.style.display = 'none';
	}
});

window.onload = function(){
	//videoload.js onload script
	window.tag = document.createElement('script');
	tag.src = 'https://www.youtube.com/iframe_api';
	window.firsttag = document.getElementsByTagName('script')[0];
	firsttag.parentNode.insertBefore(tag, firsttag);
	default_tab = document.getElementById('arttab');
	switchTabs(default_tab);

	window.iframes = document.getElementsByClassName('ytframe');
	window.videoid = [];
	window.iframeid = [];

	for (x = 0; x < iframes.length; x++){
		videoid[x] = iframes[x].attributes.ytsrc.value;
		iframeid[x] = 'iframe' + x;
		iframes[x]['id'] = iframeid[x];
	}
	//select art tab
	buttonSelect($('#arttab')[0]);
	contentSelect($('#arttab')[0].attributes.contentid);
};
