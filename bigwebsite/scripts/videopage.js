window.limit = undefined;
window.query_type = '1'; //video query
window.when_videos_load = function(){
	window.videoid = [];
	window.iframeid = [];
	initPage();
	return true;
};

get_videos = function(){
	videos = document.getElementsByClassName('container');
	videoquery = new FormData();
	videoquery.append('query', (limit).toString());
	videoquery.append('type', query_type)
	$.ajax({
		type: 'POST',
		url: window.location.href + '/query',
		data: videoquery,
		cache: false,
		processData: false,
		contentType: false
	}).done(function(response){
		x = num = last = 0;
		max = response[0];
		currently_loading = undefined;
		set_loading = undefined;
		load_single = function(){
			x++;
			last = num;
			if(!videos[num] || num >= max){return when_videos_load();}
			resp = response[x];
			video = videos[num];
			check_type = function(t){
				if(t){
					if(resp[resp.type] == t.value)
					{return true;}
				}
				return false;
			}
			type = 'video'
			if(check_type(type)){
				video.innerHTML = resp.border + resp.ytframe + resp.thumbnail;
				currently_loading = video;
			}
			if(currently_loading && num <= max){
				num++;
				currently_loading = undefined;
				return video.children[2].onload = function(){
					return load_single();
				}
			}
			return;
		};
		load_single();
	});
}

window.onload = function(){
	getlimit = new FormData();
	getlimit.append('getlimit', 'dummy');
	getlimit.append('type', query_type)
	$.ajax({
		type: 'POST',
		url: window.location.href + '/query',
		data: getlimit,
		cache: false,
		processData: false,
		contentType: false
	}).done(function(response){
		limit = response[0]
		get_videos();
	});
}
