var contents = [$('#videocontainer')[0], $('#artcontainer')[0], $('#settingscontainer')[0]];

function refreshVideos(){
	$.ajax({
		type: 'GET',
		url: window.location.href + '/videolist'
	}).done(function(response2){
		$('#videodelete').html(response2);
		window.location.href = window.location.pathname + window.location.search + window.location.hash;
	});
}

function refreshArt(){
	$.ajax({
		type: 'GET',
		url: window.location.href + '/artlist'
	}).done(function(response2){
		$('#artdelete').html(response2);
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

$('#formytadd').on('submit', function(event){
	event.preventDefault();
	videoadd = new FormData($(this)[0]);
	videoadd.append('video-submit', 'videourl');
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
	});
});

$('#formartadd').on('submit', function(event){
	event.preventDefault();
	artadd = new FormData($(this)[0]);
	artadd.append('art-submit', 'artimg');
	regex = /[.](jpeg|jpg|png|gif|bmp|webp|pdf)/gi;
	file = $(this)[0][0];
	if(file != undefined){
		result = regex.exec(file.files[0].name);
		if(result != undefined){
			artadd.append('filename', result[0]);
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
			});
		} else {
			$('#artadd-result').html('<p stle="color: red">invalid file format</p>');
		}
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
	});
});

$('#arttab').on('click', function(event){
	buttonSelect(this);
	contentSelect(this.attributes.contentid);
});

$('#videostab').on('click', function(event){
	buttonSelect(this);
	contentSelect(this.attributes.contentid);
});

$('#settingstab').on('click', function(event){
	buttonSelect(this);
	contentSelect(this.attributes.contentid);
});

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
