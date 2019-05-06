document.getElementById('showhide').addEventListener('click', function(){
	if(this.innerHTML === '[+] show license'){
		this.innerHTML = '[-] hide license';
		document.getElementsByClassName('license')[0].id = 'txtdisplay';
		window.scrollTo(0, 999999)
	} else {
		this.innerHTML = '[+] show license';
		document.getElementsByClassName('license')[0].id = 'txthide';
	}
}, false);
