window.onload = function(){
	window.highrez = new Object();
	highrez.state = false;
	images = document.getElementsByClassName('art');
	
	hidehirez = function(){
		highrez.element.attributes.src.value = '';
		document.getElementById('dimcontainer').className = 'dim-nonvis';
		highrez.element.className = 'highrez-nonvis';
		highrez.state = false;
	};
	
	for(x = 0; x < images.length; x++){
		images[x].addEventListener('click', function(x){
			highrez.element = document.getElementById('highrez'); 
			if(highrez.state === false){
				highrez.element.attributes.src.value = this.parentElement.attributes.fullrez.value;
				document.getElementById('dimcontainer').className = 'dim-vis';
				highrez.element.className = 'highrez-vis';
				highrez.state = true;
			}
		}, false);
	}
	
	/*document.getElementById('backbutton').addEventListener('click', function(){
		if(highrez.state === false){
			window.location = 'http://bigwebsite.cool/';
		} else {
			hidehirez();
		}
	}, false);*/
	
	document.getElementById('dimcontainer').addEventListener('click', function(){ hidehirez(); }, false);
	
	//document.getElementById('highrez').addEventListener('click', function(){
		//window.location = window.location+'?img='+highrez.element.attributes.src.value;
	//}, false)
}
