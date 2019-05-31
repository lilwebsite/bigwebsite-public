function signinswitch(){
	document.getElementById('dimcontainer').className = 'dimcontainer-vis';
	document.getElementById('signedin').className = 'signedin-vis';
}

function signoutswitch(){
	document.getElementById('dimcontainer').className = 'dimcontainer-vis';
	document.getElementById('signedout').className = 'signedout-vis';
}

function hideall(superh = false){
	superhide = function(){
		//document.getElementById('dimcontainer').removeClass('superhide');
		//document.getElementById('signedin').removeClass('superhide');
		//document.getElementById('signedout').removeClass('superhide');
		document.getElementById('dimcontainer').className = 'dimcontainer-nonvis';
		document.getElementById('signedin').className = 'signedin-nonvis';
		document.getElementById('signedout').className = 'signedout-nonvis';
	};
	if(superh === true){
		//document.getElementById('dimcontainer').removeClass('dimcontainer-nonvis');
		//document.getElementById('signedin').removeClass('signedin-nonvis');
		//document.getElementById('signedout').removeClass('signedout-nonvis');
		document.getElementById('dimcontainer').className = 'superhide';
		document.getElementById('signedin').className = 'superhide';
		document.getElementById('signedout').className = 'superhide';
		setTimeout(function(){superhide();}, 800);
	} else {
		document.getElementById('dimcontainer').className = 'dimcontainer-nonvis';
		document.getElementById('signedin').className = 'signedin-nonvis';
		document.getElementById('signedout').className = 'signedout-nonvis';
	}
}

function ontimeout(){
	state = window.buttonstate;
	if(state.overrides.list.length > 1 && state.overrides.list != undefined){
		state.overrides.popoverride();
	} else {
		if(state.overrides.list != undefined){
			state.overrides.popoverride();
		}
		hideall();
		state.clicks = 0;
		state.completed = true;
	}
	if (state.completed === false){
		if (state.overrides.list.length === 1 || state.overrides.list === undefined){
			setTimeout(function(){
				hideall();
			}, 1000);
		}
		if (state.overrides.list === undefined){
			console.log('undefined');
		} else if(state.overrides.list.length === 1){
			console.log('1');
		}
		//normally, if I added state.clicks = 0; here it would
		//reset the click count depending on how fast you click
		//the button, but if I remove it the button breaks with
		//a little bit of a random effect, which I think works
		//better for this implementation.
		state.completed = true;
	}
}

function buttonpress() {
	state = window.buttonstate;
	if(state.broken === false) {
		button = document.getElementById('signinbutton');
		state.last = button.attributes[1].value;
		if(button.attributes[1].value === 'content/button/signin.png') {
			button.attributes[1].value = 'content/button/signout.png';
			hideall();
			signinswitch();
			state.overrides.pushoverride();
			if (state.completed === true){
				state.completed = false;
				setTimeout(function(){ontimeout()}, 2000);
			}
		} else {
			button.attributes[1].value = 'content/button/signin.png';
			hideall();
			signoutswitch();
			state.overrides.pushoverride();
			if(state.completed === true) {
				state.completed = false;
				setTimeout(function(){ontimeout()}, 2000);
			}
		}
		if(state.clicks >= 3) {
			if(state.completed === false){
				setTimeout(function(){hideall()}, 2000);
			}
			if (button.attributes[1].value === 'content/button/signin.png') {
				if (state.last === 'content/button/signout.png') {
					setTimeout(function(){
						state.broken = true;
						button.attributes[0].value = 'signinbroken';
						button.attributes[1].value = 'content/button/signinbroken.png';
					}, 500);
				} else {
					state.broken = true;
					button.attributes[0].value = 'signinbroken';
					button.attributes[1].value = 'content/button/signinbroken.png';
				}
			}
			buttonbroke = new FormData();
			buttonbroke.append('buttonbroke', '0');
			$.ajax({
				type: 'POST',
				url: window.location.href,
				data: buttonbroke,
				cache: false,
				processData: false,
				contentType: false
			});
		}
	}
}

window.addEventListener("DOMContentLoaded", function() {
	window.buttonstate = new Object();
	buttonstate.broken = false;
	buttonstate.completed = true;
	buttonstate.clicks = 0;
	buttonstate.last = null;
	buttonstate.overrides = new Object();
	buttonstate.overrides.list = [];
	buttonstate.overrides.pushoverride = function(){this.list.push(0); return null}
	buttonstate.overrides.popoverride = function(){this.list.splice(0, 1); return null}
	hideall(true);
	document.getElementById('signinbutton').addEventListener('click', function() {
		buttonstate.clicks += 1;
		buttonpress(buttonstate);
	}, false);
}, false);
