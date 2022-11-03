/*
 * Leaflet.curve v1.0.0 - a plugin for Leaflet mapping library for adding Text to curve path.
 * Leaflet.curve is forked from https://github.com/elfalem/Leaflet.curve
 * (c) gautamGS 2019-2020
 */
/*
 * note that SVG (x, y) corresponds to (long, lat)
 */

L.Curve = L.Path.extend({
	options: {
	},
	
	initialize: function(path, options){
		L.setOptions(this, options);
		this._setPath(path);
	},
	
	getPath: function(){
		return this._coords;
	},
	
	setPath: function(path){
		this._setPath(path);
		return this.redrawText();
	},
	
	getBounds: function() {
		return this._bounds;
	},

	_setPath: function(path){
		this._coords = path;
		this._bounds = this._computeBounds();
	},
	
	_computeBounds: function(){
		var bound = new L.LatLngBounds();
		var lastPoint;
		var lastCommand;
		for(var i = 0; i < this._coords.length; i++){
			coord = this._coords[i];
			if(typeof coord == 'string' || coord instanceof String){
				lastCommand = coord;
			}else if(lastCommand == 'H'){
				bound.extend([lastPoint.lat,coord[0]]);
				lastPoint = new L.latLng(lastPoint.lat,coord[0]);
			}else if(lastCommand == 'V'){
				bound.extend([coord[0], lastPoint.lng]);
				lastPoint = new L.latLng(coord[0], lastPoint.lng);
			}else if(lastCommand == 'C'){
				var controlPoint1 = new L.latLng(coord[0], coord[1]);
				coord = this._coords[++i];
				var controlPoint2 = new L.latLng(coord[0], coord[1]);
				coord = this._coords[++i];
				var endPoint = new L.latLng(coord[0], coord[1]);

				bound.extend(controlPoint1);
				bound.extend(controlPoint2);
				bound.extend(endPoint);

				endPoint.controlPoint1 = controlPoint1;
				endPoint.controlPoint2 = controlPoint2;
				lastPoint = endPoint;
			}else if(lastCommand == 'S'){
				var controlPoint2 = new L.latLng(coord[0], coord[1]);
				coord = this._coords[++i];
				var endPoint = new L.latLng(coord[0], coord[1]);

				var controlPoint1 = lastPoint;
				if(lastPoint.controlPoint2){
					var diffLat = lastPoint.lat - lastPoint.controlPoint2.lat;
					var diffLng = lastPoint.lng - lastPoint.controlPoint2.lng;
					controlPoint1 = new L.latLng(lastPoint.lat + diffLat, lastPoint.lng + diffLng);
				}

				bound.extend(controlPoint1);
				bound.extend(controlPoint2);
				bound.extend(endPoint);

				endPoint.controlPoint1 = controlPoint1;
				endPoint.controlPoint2 = controlPoint2;
				lastPoint = endPoint;
			}else if(lastCommand == 'Q'){
				var controlPoint = new L.latLng(coord[0], coord[1]);
				coord = this._coords[++i];
				var endPoint = new L.latLng(coord[0], coord[1]);

				bound.extend(controlPoint);
				bound.extend(endPoint);

				endPoint.controlPoint = controlPoint;
				lastPoint = endPoint;
			}else if(lastCommand == 'T'){
				var endPoint = new L.latLng(coord[0], coord[1]);

				var controlPoint = lastPoint;
				if(lastPoint.controlPoint){
					var diffLat = lastPoint.lat - lastPoint.controlPoint.lat;
					var diffLng = lastPoint.lng - lastPoint.controlPoint.lng;
					controlPoint = new L.latLng(lastPoint.lat + diffLat, lastPoint.lng + diffLng);
				}

				bound.extend(controlPoint);
				bound.extend(endPoint);

				endPoint.controlPoint = controlPoint;
				lastPoint = endPoint;
			}else{
				bound.extend(coord);
				lastPoint = new L.latLng(coord[0], coord[1]);
			}
		}
		return bound;
	},
	
	//TODO: use a centroid algorithm instead
	getCenter: function () {
		return this._bounds.getCenter();
	},
	
	_update: function(){
		if (!this._map) { return; }
		
		this._updatePath();
	},
	
	_updatePath: function() {
		this._renderer._updatecurve(this);
		this._redrawText();
	},

	_redrawText: function () {
		
		var text = this._text,
		    options = this._textOptions;
		if (text) 
		{
		    this.setText(null).setText(text, options);
		}
		
    	},

	setText: function(text, options)
	{
		
		this._text = text;
		this._textOptions = options;
		if (!L.Browser.svg || typeof this._map === 'undefined') {
			return this;
		  }
		
		var defaults = 
		    {
            		fillColor: 'green',
            		attributes: {},
            		below: false,
			offset: 20,
			orientation :180,
			center : true
		   };
		options = L.Util.extend(defaults, options);
		
		if (!text) 
		{
            		if (this._textNode && this._textNode.parentNode)
			{ 
				this._map._renderer._container.removeChild(this._textNode);
                
               			 /* delete the node, so it will not be removed a 2nd time if the layer is later removed from the map */
                		delete this._textNode;
            		}
            		return this;
		}
		
		//replace texts Non breakable spaces
		text = text.replace(/ /g, '\u00A0');  // Non breakable spaces
		
		var id = 'curvepathdef-' + L.Util.stamp(this);
		var svg = this._map._renderer._container;
		this._path.setAttribute('id', id);

		 /* Put it along the path using textPath */
		 var textNode = L.SVG.create('text'),
		 textPath = L.SVG.create('textPath');


		var dy = options.offset ;
		
		textPath.setAttributeNS("http://www.w3.org/1999/xlink", "xlink:href", '#'+id);
		textNode.setAttribute('dy', dy);
		
		textPath.appendChild(document.createTextNode(text));
        	textNode.appendChild(textPath);
		this._textNode = textNode;
		
		if (options.below) 
		{
            		svg.insertBefore(textNode, svg.firstChild);
       		 }
        	else 
		{
            		svg.appendChild(textNode);
		}
		
		 /* Center text according to the path's bounding box */
		if (options.center) 
		{
           		var textLength = textNode.getComputedTextLength();
			var pathLength = this._path.getTotalLength();
			/* Set the position for the left side of the textNode */
            		textNode.setAttribute('dx', ((pathLength / 2) - (textLength / 2)));
        	}

		/* Change label rotation (if required) */
        	if (options.orientation)
		{
            		var rotateAngle = 0;
            		switch (options.orientation)
			{
				case 'flip':
                    				rotateAngle = 180;
                    				break;
                		case 'perpendicular':
                   				 rotateAngle = 90;
                    				break;
                		default:
                    			rotateAngle = options.orientation;
            		}

            		var rotatecenterX = (textNode.getBBox().x + textNode.getBBox().width / 2);
			var rotatecenterY = (textNode.getBBox().y + textNode.getBBox().height / 2);
			
			textNode.setAttribute('transform','rotate(' + rotateAngle + ' '  + rotatecenterX + ' ' + rotatecenterY + ')');
		}

		/*---return the modified element back */
		return this;
	},
	_project: function() {
		var coord, lastCoord, curCommand, curPoint;

		this._points = [];
		
		for(var i = 0; i < this._coords.length; i++){
			coord = this._coords[i];
			if(typeof coord == 'string' || coord instanceof String){
				this._points.push(coord);
				curCommand = coord;
			}else {
				switch(coord.length){
					case 2:
						curPoint = this._map.latLngToLayerPoint(coord);
						lastCoord = coord;
					break;
					case 1:
						if(curCommand == 'H'){
							curPoint = this._map.latLngToLayerPoint([lastCoord[0], coord[0]]);
							lastCoord = [lastCoord[0], coord[0]];
						}else{
							curPoint = this._map.latLngToLayerPoint([coord[0], lastCoord[1]]);
							lastCoord = [coord[0], lastCoord[1]];
						}
					break;
				}
				this._points.push(curPoint);
			}
		}
	}	
});

L.curve = function (path, options){
	return new L.Curve(path, options);
};

L.SVG.include({
	_updatecurve: function(layer){
		this._setPath(layer, this._curvePointsToPath(layer._points));
		
    	},
 	_curvePointsToPath: function(points){
		var point, curCommand, str = '';
		for(var i = 0; i < points.length; i++){
			point = points[i];
			if(typeof point == 'string' || point instanceof String){
				curCommand = point;
				str += curCommand;
			}else{
				switch(curCommand){
					case 'H':
						str += point.x + ' ';
						break;
					case 'V':
						str += point.y + ' ';
						break;
					default:
						str += point.x + ',' + point.y + ' ';
						break;
				}
			}
		}
		return str || 'M0 0';
	}
});
