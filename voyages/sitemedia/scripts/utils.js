/* Legacy function for the map */

var IE = navigator.userAgent.indexOf("MSIE 7.0") != -1 || navigator.userAgent.indexOf("MSIE 6.0") != -1 || navigator.userAgent.indexOf("MSIE 5.5") != -1;
var GK = navigator.userAgent.indexOf("Gecko") != -1;

function debug(text) {
	var el = document.getElementById("debug");
	if (el)
		el.innerHTML += text + " ";
}

function Animation(element, steps, duration, callWhenDone, functionArg) {
	this.element = element;
	this.steps = steps;
	this.delay = Math.round(duration / steps);
	this.callWhenDone = callWhenDone;
	this.functionArg = functionArg;
}

Animation.prototype.setPositions = function(x1, y1, x2, y2) {
	this.setAnimatePosition(true);
	this.setStartPosition(x1, y1);
	this.setEndPosition(x2, y2);
}

Animation.prototype.setAnimatePosition = function(value) {
	this.animatePos = value;
}

Animation.prototype.setStartPosition = function(x, y) {
	this.x1 = x;
	this.y1 = y;
}

Animation.prototype.setEndPosition = function(x, y) {
	this.x2 = x;
	this.y2 = y;
}

Animation.prototype.setSizes = function(w1, h1, w2, h2) {
	this.setAnimateSize(true);
	this.setStartSize(w1, h1);
	this.setEndSize(w2, h2);
}

Animation.prototype.setAnimateSize = function(value) {
	this.animateSize = value;
}

Animation.prototype.setStartSize = function(w, h) {
	this.w1 = w;
	this.h1 = h;
}

Animation.prototype.setEndSize = function(w, h) {
	this.w2 = w;
	this.h2 = h;
}

Animation.prototype.setOpacities = function(o1, o2) {
	this.setAnimateOpacity(true);
	this.setStartOpacity(o1);
	this.setEndOpacity(o2);
}

Animation.prototype.setAnimateOpacity = function(value) {
	this.animateOpacity = value;
}

Animation.prototype.setStartOpacity = function(o) {
	this.o1 = o;
}

Animation.prototype.setEndOpacity = function(o) {
	this.o2 = o;
}

Animation.prototype.start = function() {
	this.pos = 0;
	this.move();
}

Animation.prototype.move = function() {

	var t = this.pos / this.steps;
	if (this.animatePos) {
		this.element.style.left = Math.round(this.x1 + t * (this.x2 - this.x1)) + "px";
		this.element.style.top = Math.round(this.y1 + t * (this.y2 - this.y1)) + "px";
	}
	if (this.animateSize) {
		this.element.style.width = Math.round(this.w1 + t * (this.w2 - this.w1)) + "px";
		this.element.style.height = Math.round(this.h1 + t * (this.h2 - this.h1)) + "px";
	}
	if (this.animateOpacity) {
		this.element.style.opacity = this.o1 + t * (this.o2 - this.o1);
	}

	if (this.pos < this.steps) {
		this.pos++;
		Timer.delayedCall(this, "move", this.delay);
	} else {
		if (this.callWhenDone)
			this.callWhenDone(this.functionArg);
	}

}
var EventUtils = {

	getRelativePosX : function(e) {
		return e.x ? e.x : e.layerX;
	},

	getRelativePosX : function(e) {
		return e.y ? e.y : e.layerY;
	}
}

var ElementUtils = {

	show : function() {
		for (var i = 0; i < arguments.length; i++) {
			var el = document.getElementById(arguments[i]);
			if (el)
				el.style.display = "";
		}
	},

	hide : function() {
		for (var i = 0; i < arguments.length; i++) {
			var el = document.getElementById(arguments[i]);
			if (el)
				el.style.display = "none";
		}
	},

	getEventMouseX : function(event) {
		return event.clientX + Math.max(document.body.scrollLeft, document.documentElement.scrollLeft);
	},

	getEventMouseY : function(event) {
		return event.clientY + Math.max(document.body.scrollTop, document.documentElement.scrollTop);
	},

	getEventMouseElementX : function(event, el) {
		return ElementUtils.getEventMouseX(event) - ElementUtils.getPosLeft(el);
	},

	getEventMouseElementY : function(event, el) {
		return ElementUtils.getEventMouseY(event) - ElementUtils.getPosTop(el);
	},

	getOffsetWidth : function(el) {
		return el.offsetWidth;
	},

	getOffsetHeight : function(el) {
		return el.offsetHeight;
	},

	getRealPageHeight : function() {
		if (IE) {
			return window.document.documentElement.offsetHeight;
		} else {
			return window.innerHeight;
		}
	},

	getRealPageWidth : function() {
		if (IE) {
			return window.document.documentElement.offsetWidth;
		} else {
			return window.innerWidth;
		}
	},

	getOffsetLeft : function(el, rel) {
		var curleft = 0;
		while (el.offsetParent && el != rel) {
			curleft += el.offsetLeft
			el = el.offsetParent;
		}
		return curleft;
	},

	getOffsetTop : function(el, rel) {
		var curtop = 0;
		while (el.offsetParent && el != rel) {
			curtop += el.offsetTop
			el = el.offsetParent;
		}
		return curtop;
	},

	getPosLeft : function(el) {
		var curleft = 0;
		while (el.offsetParent) {
			curleft += el.offsetLeft
			el = el.offsetParent;
		}
		return curleft;

	},

	getPosTop : function(el) {

		var curtop = 0;
		while (el.offsetParent) {
			curtop += el.offsetTop
			el = el.offsetParent;
		}
		return curtop;

	},

	deleteAllChildren : function(el) {
		while (el.hasChildNodes())
		el.removeChild(el.firstChild);
	},

	getPageWidth : function() {
		if (self.pageXOffset)// all except IE
		{
			return self.innerWidth;
		} else if (document.documentElement && document.documentElement.clientWidth)// IE6 Strict
		{
			return document.documentElement.clientWidth;
		} else if (document.body)// all other IE
		{
			return document.body.clientWidth;
		}
	},

	getPageHeight : function() {
		if (self.pageYOffset)// all except IE
		{
			return self.innerHeight;
		} else if (document.documentElement && document.documentElement.clientHeight)// IE6 Strict
		{
			return document.documentElement.clientHeight;
		} else if (document.body)// all other IE
		{
			return document.body.clientHeight;
		}
	},

	getPageScrollLeft : function() {
		if (document.documentElement != null) {
			return document.documentElement.scrollLeft;
		} else {
			return document.body.scrollLeft;
		}
	},

	getPageScrollTop : function() {
		if (document.documentElement != null) {
			return document.documentElement.scrollTop;
		} else {
			return document.body.scrollTop;
		}
	},

	addOption : function(sel, value, text) {
		var opt = document.createElement("option");
		opt.value = value;
		opt.appendChild(document.createTextNode(text));
		sel.appendChild(opt);
	},

	removeAllOptions : function(sel) {
		while (sel.length > 0)
		sel.remove(0);
	}
}

/////////////////////////////////////////////////////////
// EventAttacher
// Note: Handling events of the window object is treated
// separately because Opera in 'this' variable passes
// document instead of window.
/////////////////////////////////////////////////////////

var EventAttacher = {
	map : new Array(),

	attach : function(element, eventType, object, handler, args) {

		/*
		 if (element == null)
		 {
		 if (window.addEventListener)
		 {
		 window.addEventListener(eventType, EventAttacher.globalWindowHandler, false);
		 }
		 else
		 {
		 window.attachEvent("on" + eventType, EventAttacher.globalWindowHandler);
		 }
		 }
		 else
		 {
		 if (element.addEventListener)
		 {
		 element.addEventListener(eventType, EventAttacher.globalHandler, false);
		 }
		 else if (element.attachEvent)
		 {
		 element.attachEvent("on" + eventType, EventAttacher.globalHandler);
		 }
		 }
		 */
		if (element == null) {
			window["on" + eventType] = EventAttacher.globalWindowHandler;
		} else {
			element["on" + eventType] = EventAttacher.globalHandler;
		}

		var reg = new Object();
		EventAttacher.map.push(reg);

		reg.element = element;
		reg.object = object;
		reg.eventType = eventType;
		reg.handler = handler;
		reg.args = args;

	},

	attachById : function(elementId, eventType, object, handler, args) {
		var element = document.getElementById(elementId);
		if (element != null) {
			this.attach(element, eventType, object, handler, args);
		}
	},

	attachOnWindowEvent : function(eventType, object, handler, args) {
		this.attach(null, eventType, object, handler, args);
	},

	detachOnWindowEvent : function(eventType, object, handler) {
		detach(null, eventType, object, handler);
	},

	detach : function(element, eventType, object, handler) {
		var noOnTheSameType = 0;
		for (var i = 0; i < EventAttacher.map.length; i++) {
			var reg = EventAttacher.map[i];
			if (reg.element == element && reg.eventType == eventType) {
				noOnTheSameType++;
				if (reg.object == object && reg.handler == handler) {
					EventAttacher.map.splice(i, 1);
					noOnTheSameType--;
					i--;
					;
				}
			}
		}
		if (noOnTheSameType == 0) {
			if (element == null) {
				/*
				 if (window.detachEvent)
				 {
				 window.detachEvent("on" + eventType, EventAttacher.globalWindowHandler);
				 }
				 else if (window.removeEventListener)
				 {
				 window.removeEventListener(eventType, EventAttacher.globalWindowHandler, false);
				 }
				 */
				window["on" + eventType] = null;
			} else {
				/*
				 if (element.detachEvent)
				 {
				 element.detachEvent("on" + eventType, EventAttacher.globalHandler);
				 }
				 else if (element.removeEventListener)
				 {
				 element.removeEventListener(eventType, EventAttacher.globalHandler, false);
				 }
				 */
				element["on" + eventType] = null;
			}
		}
	},

	detachOnWindowEvent : function(eventType, object, handler) {
		EventAttacher.detach(null, eventType, object, handler);
	},

	detachById : function(elementId, eventType, object, handler) {
		var element = document.getElementById(elementId);
		EventAttacher.detach(element, eventType, object, handler);
	},

	globalWindowHandler : function(event) {
		if (!event)
			event = window.event;
		EventAttacher.dispatch(event, null, event.type);
	},

	globalHandler : function(event) {
		if (!event)
			event = window.event;
		var element = this;
		EventAttacher.dispatch(event, element, event.type);
	},

	dispatch : function(event, element, eventType) {
		for (var i = 0; i < EventAttacher.map.length; i++) {
			var reg = EventAttacher.map[i];
			if (reg.element == element && reg.eventType == eventType) {
				reg.object[reg.handler](event, reg.args);
			}
		}
	}
}

/////////////////////////////////////////////////////////
// EventQueue
/////////////////////////////////////////////////////////

function EventQueue() {
	this.queue = new Array();
}

EventQueue.prototype.register = function(object, method, arg) {
	var reg = new Object();
	reg.object = object;
	reg.method = method;
	reg.arg = arg;
	this.queue.push(reg);
}

EventQueue.prototype.invoke = function() {
	for (var i = 0; i < this.queue.length; i++) {
		var reg = this.queue[i];
		reg.object[reg.method](reg.arg);
	}
}
/////////////////////////////////////////////////////////
// Timer
/////////////////////////////////////////////////////////

var Timer = {

	map : new Array(),
	nextId : 0,

	delayedFunction : function(fnc, delay, arg) {

		var id = Timer.nextId;
		Timer.nextId++;

		var reg = new Object();
		reg.fnc = fnc;
		reg.arg = arg;
		reg.tid = window.setTimeout("Timer.globalHandler(" + id + ")", delay);

		Timer.map["call_" + id] = reg;

		return id;

	},

	extendFunction : function(id, fnc, delay, arg) {
		Timer.cancelCall(id);
		return Timer.delayedFunction(fnc, delay, arg);
	},

	delayedCall : function(object, method, delay, arg) {

		var id = Timer.nextId;
		Timer.nextId++;

		if (object == null)
			object = window;
		var reg = new Object();
		reg.object = object;
		reg.method = method;
		reg.arg = arg;
		reg.tid = window.setTimeout("Timer.globalHandler(" + id + ")", delay);

		Timer.map["call_" + id] = reg;

		return id;

	},

	extendCall : function(id, object, method, delay, arg) {
		Timer.cancelCall(id);
		return Timer.delayedCall(object, method, delay, arg);
	},

	cancelCall : function(id) {
		var reg = Timer.map["call_" + id];
		if (reg) {
			window.clearTimeout(reg.tid);
			delete Timer.map["call_" + id];
		}
	},

	globalHandler : function(id) {
		var reg = Timer.map["call_" + id];
		if (reg) {
			delete Timer.map["call_" + id];
			if (reg.fnc) {
				reg.fnc(reg.arg);
			} else {
				reg.object[reg.method](reg.arg);
			}
		}
	}
}

/////////////////////////////////////////////////////////
// ObjectUtils
/////////////////////////////////////////////////////////

var ObjectUtils = {

	toString : function(obj) {
		if (!obj) {
			return obj;
		} else {
			var ret = "";
			for (var k in obj)
			ret += k + " = " + obj[k] + "\n";
			return ret;
		}
	},

	printObject : function(obj) {
		alert(this.toString(obj));
	}
}

/////////////////////////////////////////////////////////
// StringUtils
/////////////////////////////////////////////////////////

var StringUtils = {

	splitByLines : function(str) {
		return str.split(/[\n\r]+/);
	},

	removeEmptyStrings : function(strArray) {
		var newArray = new Array();
		for (var i = 0; i < strArray.length; i++) {
			if (strArray[i] != "") {
				newArray.push(strArray[i]);
			}
		}
		return newArray;
	},

	splitByLinesAndRemoveEmpty : function(str) {
		return StringUtils.removeEmptyStrings(StringUtils.splitByLines(str));
	},

	compareArrays : function(a1, a2) {
		if (a1.length != a2.length) {
			return false;
		} else {
			var n = a1.length;
			for (var i = 0; i < n; i++) {
				if (a1[i] != a2[i]) {
					return false;
				}
			}
			return true;
		}
	}
}

//Adds an attributes to an existing element
//Mostly used to add attributes to elements generated with JSF which limits the attributes that can be passed to the tag
function insertAttrib(elem, key, val) {
	elem.setAttribute(key, val);
}