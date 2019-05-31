window.back = document.getElementById('back');
window.next = document.getElementById('next');
window.highrez = new Object();
window.current_pdf = new Object();
window.pdf_regex = /(\d+);(\d+)/gi;
window.loaded_images = 0;
window.limit = undefined;
window.query_type = '0';

window.when_images_load = function(){
	console.log('images loaded');
	imgs = document.getElementsByClassName('art');
	pdfs = document.getElementsByClassName('pdf');
	backbutton = document.getElementById('backlink');

	for(x = 0; x < imgs.length; x++){
		imgs[x].addEventListener('click', function(x){
			if(highrez.state === false){
				highrez.element.attributes.src.value = this.parentElement.attributes.fullrez.value;
				showhirez();
			}
		}, false);
	}

	for(x = 0; x < pdfs.length; x++){
		pdfs[x].attributes.pdf_num = x;
		pdfs[x].addEventListener('click', function(){
			pdf_regex.lastIndex = 0;
			pdf_info = pdf_regex.exec(pdfs[this.attributes.pdf_num].parentElement.attributes.pdfobj.value);
			this.attributes.pdf_image = [];
			this.attributes.pdf_length = parseInt(pdf_info[2]) - 1;
			for(i = 0; i < this.attributes.pdf_length; i++){
				this.attributes.pdf_image[i] = this.attributes.src.value.replace('thumbnail', (i).toString());
			}
			current_pdf.selected = true;
			current_pdf.element = this;
			highrez.element.attributes.src.value = this.attributes.pdf_image[0];
			showhirez('pdf');
		}, false);
	}
	
	document.getElementById('dimcontainer').addEventListener('click', function(){ hidehirez(); }, false);
	highrez.element.addEventListener('click', function(){ hidehirez(); }, false);

	//document.getElementById('highrez').addEventListener('click', function(){
		//window.location = window.location+'?img='+highrez.element.attributes.src.value;
	//}, false)

	document.getElementById('back').addEventListener('click', function(e){ nav_pdf(false) }, false);
	document.getElementById('next').addEventListener('click', function(e){ nav_pdf(true) }, false);
	return true;
};

showhirez = function(type){
	document.getElementById('dimcontainer').className = 'dim-vis';
	highrez.element.className = 'highrez-vis';
	highrez.state = true;
	backbutton.style.display = 'none';
	if(type == 'pdf'){
		next.className = 'control-vis';
	}
};

hidehirez = function(){
	highrez.element.attributes.src.value = '';
	document.getElementById('dimcontainer').className = 'dim-nonvis';
	highrez.element.className = 'highrez-nonvis';
	highrez.state = false;
	backbutton.style.display = '';
	back.className = next.className = 'control-novis';
	current_pdf.selected = false;
	current_pdf.page = 0;
};

nav_pdf = function(dir){
	highrez.element.attributes.src.value = '';
	length = current_pdf.element.attributes.pdf_length;
	image = current_pdf.element.attributes.pdf_image;
	if(dir){
		if(current_pdf.page+1 >= length)
		{return;}
		current_pdf.page++;
	}else{
		if(current_pdf.page-1 < 0)
		{return;}
		current_pdf.page--;
	}
	if(current_pdf.page <= 0){
		back.className = 'control-novis';
	}else{
		back.className = 'control-vis';
	}
	if(current_pdf.page >= length-1){
		next.className = 'control-novis';
	}else{
		next.className = 'control-vis';
	}
	highrez.element.attributes.src.value = image[current_pdf.page];
};

get_images = function(){
	images = document.getElementsByClassName('artobj');
	artquery = new FormData();
	artquery.append('query', (limit).toString());
	artquery.append('type', query_type)
	$.ajax({
		type: 'POST',
		url: window.location.href + '/query',
		data: artquery,
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
			if(!images[num] || num >= max){return when_images_load();}
			resp = response[x];
			image = images[num];
			check_type = function(t){
				if(t){
					if(resp[resp.type] == t.value)
					{return true;}
				}
				return false;
			}
			type = image.attributes.fullrez;
			if(check_type(type)){
				image.innerHTML = `<img class="art" src="${resp.uri}">`;
				currently_loading = image;
			}
			type = image.attributes.pdfobj;
			if(check_type(type)){
				image.innerHTML = `<img class="pdf" src="${resp.uri}">`;
				currently_loading = image;
			}
			if(currently_loading && num <= max){
				num++;
				currently_loading = undefined;
				return image.children[0].onload = function(){
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
		highrez.state = false;
		highrez.element = document.getElementById('highrez');

		current_pdf.selected = false;
		current_pdf.page = 0;
		current_pdf.element = false;

		limit = response[0]

		get_images();
	});
}
