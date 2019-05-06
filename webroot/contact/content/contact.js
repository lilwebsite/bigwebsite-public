//The MIT License (MIT)

//Copyright (c) 2018 Carl Gessau

//Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

//The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

//
//feel free to use this code for anything that needs a custom high resolution font
//for a text box as long as it is adhering to the MIT license. I designed this for
//reuse, so it would work well with custom emojis or additonal special characters
//in any type of self defined text box (probably won't work in an <input>, but in an
//extension of one, like the one I have made here)
//

//regarding the hidden input, this is so mobile is compatible. without it the keyboard would not show up at all.

//
//function description
//
//keypress.add() - will add a keypress to the array keypress.keys. keeps track of all the keys that are to be displayed
//keypress.del() - deletes the most recently added key to keypress.add()
//keypress.setletters() - will add the apropriate html to the targeted container div and assign the elements their ID for each letter respectively (ex: to display A the element will need to be given an ID of #A or for the @ symbol an id of #at. each ID has the apropriate background position setup beforehand)
//keypress.verify() - will check if the hidden input (#prompt) and the keypress.keys array are equal. if not, make them equal
//keypress.duplicate_verify() - in some cases, when the hidden input and document keyboard input both receive input, a duplicate letter is added to the input box. This removes that duplicated letter.
//keypress.genstr() - will generate a string value from the keypress.keys array. Very useful.
//keypress.deletetimeout() - will add a timeout to the delete key being pressed by setting keypress.deleted to true. Prevents multiple delete calls.
//keypress.timeout() - will add a timeout to a key being pressed by setting keypress.detected to true. Stops multiple keys from being added to the input and keypress.keys on a single input.
//

window.debug = new Object();
//set to true if you want debug output
debug.on = false;
debug.print = function(str) {
	(this.on ? console.log('debug --> [' + str + ']') : null);
};

//displays caret
function careton() {
	setTimeout(function() {
		if (document.getElementById('caret') === null) {
			setTimeout(caretoff, 500);
		} else {
			document.getElementById('caret').style.opacity = '1';
		}
		caretoff();
	}, 500);
}

//hides caret
function caretoff() {
	setTimeout(function() {
		if (document.getElementById('caret') === null) {
			setTimeout(careton, 500);
		} else {
			document.getElementById('caret').style.opacity = '0';
		}
		careton();
	}, 500);
}

//resizes text in the box; caret is automatic
onresize = function() {
	letter = document.getElementsByClassName('alphabet')[0];
	if (letter != undefined) {
		dummy = document.getElementById('dummy');
		caretcontainer = document.getElementById('caret-container');
		ccheight = caretcontainer.clientHeight
		letters = document.getElementsByClassName('alphabet');
		if (letter.clientHeight >= ((ccheight / 4) * 3)) {
			for (x = 0; x < letters.length; x++) {
				//a little math to make it size correctly; maybe not the most effcient
				letters[x].style.fontSize = (((ccheight / 4) * 3) / 4) + 'px';
			}
		} else {
			for (x = 0; x < letters.length; x++) {
				letters[x].style.fontSize = '1.5vh';
			}
		}
	}
}

function oninput(that) {
	//if valid is false by the end of this function it will
	//delete the character that was just added to the input
	valid = false;
	//verify just in case on keypress timeout
	if (keypress.detect === true) {
		keypress.duplicate_verify();
		//keypress.verify();
	} else {
		//if a letter was removed, delete it
		keypress.setkeystr();
		if (that.value.length < keypress.keystr.length) {
			//this if statement needs to be here
			//putting it above with && won't work
			if (keypress.verifylength(false) === true) {
				if (keypress.del() === false && that.value.length != 0) {
					if (that.value.length > 0) {}
					valid = true;
				}
			} else if (that.value.length > 1) {
				//since the input is probably meant to be removing a character,
				//even if the input isn't perfect, removing a character should be fine
				that.value = keypress.genstr(true);
				keypress.del();
				keypress.verify();
				valid = true;
			}
		} else if (that.value.length > keypress.keystr.length && keypress.checkletter(that.value[that.value.length - 1]) != false) {
			if (keypress.checkundefined() === true) {
				that.value = keypress.checkundefined(true);
			}
			if (keypress.verifylength() === true) {
				//this only seems to be an issue with firefox mobile
				//but on backspace it'll duplicate the string
				//into the hidden input (#prompt) box
				if (keypress.keystr + keypress.keystr === that.value && that.value.length > 2) {
					that.value = keypress.keystr;
				}
				//if a letter was added use alternate verify
				keypress.verify(true);
				valid = true;
			} else {
				that.value = keypress.genstr();
				keypress.verify();
				valid = true;
			}
		}
	}
	if (valid === true) {
		keypress.setletters();
	} else if (keypress.checkletter(that.value[that.value.length - 1]) === false && that.value.length != 0) {
		that.value = that.value.replace(that.value[that.value.length - 1], '');
	}
	keypress.input_setlength(keypress.keys.length);
}

window.keypress = new Object();
//keeps an array of currently entered text
keypress.keys = [];
//the html to overwrite in the #caret-container
keypress.caret = '<img src="contact/content/caret.png" id="caret" draggable="false" />';
keypress.letter = '<div class="alphabet"></div>';
keypress.emailregex = /[A-Z0-9.%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi;
keypress.keystr = '';
//detect will prevent multiple letters being 'pressed'; the script 
//checks for if its getting input from the hidden #prompt box or
//the document's keydown listener
keypress.detect = false;
keypress.detectfalse = function() {
	keypress.detect = false;
};

//timeout for the detect 'flag'
keypress.timeout = function() {
	keypress.detect = true;
	setTimeout(function() {
		keypress.detectfalse();
	}, 10);
};

//same as keypress.detect except for deleting (doesn't really work? ff mobile)
keypress.deleted = false;
keypress.deletedfalse = function() {
	keypress.deleted = false;
};

keypress.deletetimeout = function() {
	keypress.deleted = true;
	setTimeout(function() {
		keypress.deletedfalse();
	}, 10);
};

//generates a string from an array for the
//keypress.keystr variable
keypress.genstr = function(remove = false) {
	str = '';
	if (remove === false) {
		for (x = 0; x < keypress.keys.length; x++) {
			str += keypress.keys[x];
		}
		return str;
	} else {
		for (x = 0; x < keypress.keys.length - 1; x++) {
			str += keypress.keys[x];
		}
		return str;
	}
};

//sets the key str for getting the length
keypress.setkeystr = function() { keypress.keystr = this.genstr(); }

//checks if the letter in the hidden input (#prompt) box exists
keypress.checkletter = function(letter) {
	regex = /([abcdefghijklmnopqrstuvwxyz@.-0123456789])/gi;
	regresult = regex.exec(letter);
	if (regresult != undefined) {
		return regresult[0];
	}
	return false;
};

//basically:
//case (character pressed): break
//on break return true; on default return false
keypress.checkkey = function(key) {
	switch (key.key.toLowerCase()) {
		case 'a': break;case 'b': break;case 'c': break;case 'd': break;case 'e': break;case 'f': break;case 'g': break;case 'h': break;case 'i': break;case 'j': break;case 'k': break;case 'l': break;case 'm': break;case 'n': break;case 'o': break;case 'p': break;case 'q': break;case 'r': break;case 's': break;case 't': break;case 'u': break;case 'v': break;case 'w': break;case 'x': break;case 'y': break;case 'z': break;case '@': break;case '.': break;case '-': break;case '0': break;case '1': break;case '2': break;case '3': break;case '4': break;case '5': break;case '6': break;case '7': break;case '8': break;case '9': break;
		default:
			if (key.keyCode === 8) {
				keypress.del();
				keypress.verify();
				keypress.setletters();
				return false;
				break;
			}
			return false;
			break;
	}
	return true;
};

keypress.checkundefined = function(overwrite = false) {
	found = document.getElementById('prompt').value.indexOf('undefined');
	textin = document.getElementById('prompt');
	if (found != -1) {
		if (overwrite === false) {
			return true;
		} else {
			value = textin.value.replace(/undefined/g, '');
			return value
		}
	}
	return false;
};

//the function verifylength() is responsible for
//verifying the current length of the hidden
//input box. on firefox mobile it is prone to
//adding duplicate text. if a key input has 
//been detected it will check if the length
//is over one key. if it is greater, something
//is wrong and it has to nullify the str in
//the input box
keypress.input_lastlen = 0;
keypress.input_nullify = false;
keypress.verifylength = function(adding = true) {
	if (adding === true) {
		if (this.input_lastlen === document.getElementById('prompt').value.length - 1) {
			this.input_nullify = false;
			return true;
		}
		this.input_nullify = true;
		return false;
	} else {
		if (this.input_lastlen === document.getElementById('prompt').value.length + 1) {
			this.input_nullify = false;
			return true;
		}
		this.input_nullify = true;
		return false;
	}
};

keypress.input_setlength = function(length) {
	this.input_lastlen = length;
};

//checks that the input box and the keys array are equal
//if not, it fixes them
keypress.verify = function(txt = false) {
	//txt is just an alias, the real purpose is
	//to specify if the call is coming from
	//the input box or the keyboard
	textin = document.getElementById('prompt');
	if (txt === false && this.input_nullify === false) {
		//gotta get the actual length as string instead of an array or 
		//it won't work (ex: ['at', 'at'].length != 'atat'.length)
		this.setkeystr();
		if (this.keystr != textin.value) {
			if (this.keystr.length > textin.value.length) {
				textin.value = this.keystr;
			} else if (this.keystr.length < textin.value.length) {
				if (keypress.checkundefined() === true) {
					textin.value = keypress.checkundefined(true);
				}
				if (this.keystr.length < textin.value.length) {
					for (x = 0; x < textin.value.length; x++) {
						if (x === 0) {
							this.keys = [];
						}
						this.keys.push(textin.value[x]);
					}
				}
			}
			this.setletters();
		}
	} else if (this.input_nullify === false) {
		regexresult = this.checkletter(textin.value[textin.value.length - 1]);
		if (regexresult != false) {
			switch (regexresult) {
				case '@':
					regexresult = 'at';
					break;
				case '.':
					regexresult = 'dot';
					break;
				case '-':
					regexresult = 'dash';
					break;
			}
			this.add(regexresult.toLowerCase());
			this.verify();
		} else {
			//I forget why I added this
			//probably important though
			for (x = 0; x < this.keys.length; x++) {
				if (x === 0) {
					textin.value = this.keys[x];
				} else {
					textin.value += this.keys[x];
				}
			}
		}
		this.setletters();
	} else {
		if (keypress.checkundefined() === true) {
			textin.value = keypress.checkundefined(true);
		}
		if (this.genstr() === textin.value) {
			this.nullify = false;
		}
	}
};

//this only executes when the hidden input needs
//to check for duplicate characters
keypress.duplicate_verify = function() {
	this.setkeystr();
	textin = document.getElementById('prompt');
	if (this.keystr.length < textin.value.length) {
		textin.value = this.keystr;
	}
};

//add a keypress and verify that the hidden input is equal
keypress.add = function(key) {
	this.keys.push(key);
	this.verify();
};

//delete a keypress and verify
keypress.del = function() {
	if (this.deleted === false) {
		if (this.keys.length > 0) {
			this.keys.splice(this.keys.length - 1, 1);
			document.getElementById('prompt').value = this.genstr();
		} else {
			document.getElementById('prompt').value = '';
		}
		this.verify();
		this.setletters();
		this.deletetimeout();
		return true;
	}
	return false;
};

//how many characters the text box can hold
//used by keypress.setletters() and keypress.insert()
keypress.textbox_width = 13;

//insert the apropriate html
keypress.insert = function() {
	htmlinsert = '';
	setup = function(x) {
		if (x === 0 && keypress.keys.length > 0) {
			htmlinsert = keypress.letter;
		} else if (x === keypress.keys.length) {
			htmlinsert += keypress.caret;
		} else {
			htmlinsert += keypress.letter;
		}
	};
	if (this.keys.length <= this.textbox_width) {
		for (x = 0; x < this.keys.length + 1; x++) {
			setup(x);
		}
	} else {
		for (x = 0; x < this.keys.length + 1; x++) {
			if (x > (this.keys.length - this.textbox_width - 1)) {
				setup(x);
			}
		}
	}
	document.getElementById('caret-container').innerHTML = htmlinsert;
};

//touch up the html insert; also this is what should be 
//called over the keypress.insert function
keypress.setletters = function() {
	this.insert();
	letters = document.getElementsByClassName('alphabet');
	setup = function(x, z) {
		switch (keypress.keys[z]) {
			case '@':
				letters[x].id = 'at';
				break;
			case '.':
				letters[x].id = 'dot';
				break;
			case '-':
				letters[x].id = 'dash';
				break;
			case '0':
				letters[x].id = 'zero';
				break;
			case '1':
				letters[x].id = 'one';
				break;
			case '2':
				letters[x].id = 'two';
				break;
			case '3':
				letters[x].id = 'three';
				break;
			case '4':
				letters[x].id = 'four';
				break;
			case '5':
				letters[x].id = 'five';
				break;
			case '6':
				letters[x].id = 'six';
				break;
			case '7':
				letters[x].id = 'seven';
				break;
			case '8':
				letters[x].id = 'eight';
				break;
			case '9':
				letters[x].id = 'nine';
				break;
			default:
				letters[x].id = keypress.keys[z];
		}
	};
	z = letters.length - 1;
	for (x = letters.length - 1; x > -1; x--) {
		if ((x + this.keys.length) >= (this.keys.length - letters.length)) {
			if (this.keys.length <= this.textbox_width) {
				setup(x, z);
			} else {
				setup(x, ((this.keys.length - letters.length) + z));
			}
			z--;
		}
	}
};

keypress.clear = function() {
	this.keys = [];
	document.getElementById('prompt').value = '';
	this.verify();
	this.setletters();
}

//execution begins around here
window.onload = function() {
	//ring the doorbell
	var doorbell = new Object();
	doorbell.completed = false;
	doorbell.ele = document.getElementById('doorbell');
	doorbell.audio = document.getElementById('audio');
	doorbell.ele.addEventListener('click', function() {
		if (doorbell.completed === false) {
			doorbell.audio.pause();
			doorbell.audio.currentTime = 0;
			doorbell.ele.src = 'contact/content/doorbellpressed.png';
			doorbell.audio.play();
			doorbell.completed = true;
			emailtext = new FormData();
			emailtext.append('email', keypress.genstr());
			if (keypress.genstr().search(keypress.emailregex) != -1) {
				$.ajax({
					type: 'POST',
					url: window.location.href,
					data: emailtext,
					cache: false,
					processData: false,
					contentType: false
				}).done(function(response) {
					keypress.clear();
				});
			}
			setTimeout(function() {
				doorbell.ele.src = 'contact/content/doorbell.png';
				doorbell.completed = false;
			}, 125);
		}
	});

	//this will flicker the caret on and off
	caretoff();

	//just a lil logic for making sure the text stays in the box on mobile
	//refer to onresize()
	onresize();
	new ResizeSensor(document.getElementById('enterinfo'), onresize);

	//typing logic
	//
	//focus hidden text field so the script can detect input for mobile
	document.getElementById('caret-container').addEventListener('click', function() {
		document.getElementById('prompt').focus();
	});


	//if a key is pressed, will check if that key is ok and then add it 
	// () is only called here
	document.addEventListener('keydown', function(key) {
		if (keypress.checkkey(key) != false && keypress.detect === false) {
			keypress.add(key.key.toLowerCase());
			keypress.setletters();
			keypress.timeout();
		}
	});

	//prevent navigation back with backspace
	$(document).on('keydown', function(key) {
		debug.print('keypress');
		capture = $(key.target || key.srcElement);
		((key.keyCode == 8 && !capture.is('input')) ? key.preventDefault() : null);
	});

	//listen to the prompt
	document.getElementById('prompt').addEventListener('input', function() {
		oninput(this);
	});

	//reset prompt on page load
	(document.getElementById('prompt').value != '' ? document.getElementById('prompt').value = '' : null);
};
