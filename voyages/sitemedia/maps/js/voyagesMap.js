/*!
 *  Test if two (ordered) arrays are equal.
 */
 Array.prototype.arrayEquals = function(b) {
	var a = this;
	if (a.length != b.length) return false;
	var result = true;
	for (var i = 0; result && i < a.length; ++i) {
		result = (a[i] == b[i]);
	}
	return result;
}

/*!
 *  Push an object into the array only if it is not already in the array.
 */
 Array.prototype.pushUnique = function(obj) {
	if (this.indexOf(obj) < 0) {
		this.push(obj);
	}
}

/*!
 *  Remove all instances of an element from the array.
 */
Array.prototype.remove = function(item) {
	for(var i = this.length; i--;) {
		if(this[i] === item) {
			this.splice(i, 1);
		}
	}
}

/*!
 *  How many pixels correspond to 1 degree of latitude.
 */
L.Map.prototype.getPixelToLatScale = function() {
	return (this.getPixelBounds().max.y - this.getPixelBounds().min.y) / (this.getBounds().getNorth() - this.getBounds().getSouth());
}

/*!
 *  A class representing a volume of flow from
 *  LatLng source to LatLng destination.
 */
function Flow(source, destination, volume, netVolume, initial, terminal, path) {
	this.source = source;
	this.destination = destination;
	this.volume = volume;
	this.netVolume = netVolume;
	this.initial = initial || false;
	this.terminal = terminal || false;
	this.path = path || [ source, destination ];
}

/*!
 *  A class that stores global locations together with names
 *  identifying what they are.
 */
function LocationIndex() {
	this.add = function(loc, label) {
		var key = voyagesMap._latLngEncode(loc);
		if (!this.hasOwnProperty(key)) {
			this[key] = [ label ];
		} else {
			this[key].pushUnique(label);
		}
	};

	this.names = function() {
		var result = { };
		for (var key in this) {
			var col = this[key];
			if (col.length == 1) {
				result[key] = "port: " + col[0];
			} else {
				result[key] = "ports: " + Array.prototype.join.call(col, ", ");
			}
		}
		return result;
	};
};

var _mapBoundaries = new L.LatLngBounds(
	new L.LatLng(-59.517932, -111.936579),
	new L.LatLng(63.9, 60.9)
);

// Helpful definitions when using Django templates.
var None = null;
var Nothing = null;

/*!
 *  A singleton that organizes all interactive
 *  features of the Voyages map.
 */
var voyagesMap = {
	// "Private" members
	_bounds: _mapBoundaries,
	_graphics: [ ],
	_icon: null,
	_map: L.map('map', {
		attributionControl: false,
		maxBounds: _mapBoundaries,
	}).setView([6, -20], 3),
	_mapLayer: null,
	_maxPathWidth: 80,
	_networkLayers: [ ],
	_pathColor: 'SandyBrown',
	_pathOpacity: 1.0,
	_routeNodes: [ ],

	// Public methods.

	/*!
	 *	Wrap the corresponding addLayer method of
	 * _map and allows us to keep track of which
	 *  layers have been added to the map.
	 */
	addLayer: function(layer) {
		this._map.addLayer(layer);
		this._graphics.push(layer);
		return layer;
	},

	/*!
	 *  Clear all graphics on top of map.
	 */
	clear: function() {
		this.clearNetwork();
		for (var i = 0; i < this._graphics.length; ++i) {
			this._map.removeLayer(this._graphics[i]);
		}
		this._graphics = [ ];
	},

	/*!
	 *  Clear all graphics related to the network flow.
	 */
	clearNetwork: function() {
		for (var i = 0; i < this._networkLayers.length; ++i) {
			var layer = this._networkLayers[i];
			this._map.removeLayer(layer);
			var index = this._graphics.indexOf(layer);
			if (index >= 0) {
				this._graphics.splice(index, 1);
			}
		}
		this._networkLayers = [ ];
	},

	/*!
	 *  Redraw the current network. In case the route nodes
	 *  have been updated, the paths may change accordingly.
	 */
	draw: function() {
		// This function must be set by the method setNetworkFlow.
	},

	/*!
	 *  Gets the map boundaries.
	 */
	getBounds: function() { return this._bounds; },

	/*!
	 *  Gets the maximum width of a path denoting flow in this
	 *  map. All flow path widths are scaled down so that the
	 *  maximum width is attained by the path segment with
	 *  largest flow.
	 */
	getMaxPathWidth: function() { return this._maxPathWidth; },

	/*!
	 *  Gets the opacity for flow paths.
	 */
	getPathOpacity: function() { return this._pathOpacity; },

	/*!
	 * Initialize the map.
	 * @param {String} baseMapId - the id of the map being loaded
	 * @param {Array} routeNodes - an array of LatLng's that are
	 *        used to route network flows.
	 * @param {L.Icon} markerIcon - the icon that will be shown
	 *        for every port in the network.
	 */
	init: function(baseMapId, mapTilePrefix, routeNodes, markerIcon) {
		this.clear();
		this.loadBaseMap(baseMapId, mapTilePrefix);
		this._icon = markerIcon || L.icon({ iconUrl: mapTilePrefix + 'js/images/marker-icon-redcircle.png', iconAnchor: [6, 6] });;
		this._routeNodes = routeNodes;
		return this;
	},

	/*!
	 * Load a base map tiling using mapId as identifier.
	 * @param mapId - the id of the map being loaded
	 */
	loadBaseMap: function(mapId, prefix) {
	    prefix = prefix || '';
		if (this._mapLayer) this._map.removeLayer(this._mapLayer);
        var options = {
            minZoom: 2,
            maxZoom: 7,
            opacity: 1.0,
            id: mapId,
            tms: false,
            noWrap: true,
            bounds: this._bounds,
        };
		this._mapLayer = L.tileLayer(prefix + 'img/map_{id}/{z}/{x}/{y}.png', options);
		this._map.addLayer(this._mapLayer);
		return this._mapLayer;
	},

	/*!
	 *	Wrap the corresponding addLayer method of
	 * _map and allows us to keep track of which
	 *  layers have been added to the map.
	 */
	removeLayer: function(layer) {
		this._map.removeLayer(layer);
		this._graphics.remove(layer);
		return layer;
	},
	
	/*!
	 * Parse the given JSON string and invoke
	 * setNetworkFlow with the parsed elements.
	 * @param {String} json - the JSON data describing the
	 *        collection of ports and flows between them.
	 */
	setJsonNetworkFlow: function(json) {
		this.clearNetwork();
		try {
			var data = JSON.parse(json);
			var ports = { };
			var flows = [ ];
			for (var key in data.ports) {
				var coord = data.ports[key];
				ports[key] = new L.LatLng(coord[0], coord[1]);
			}
			for (var i = 0; i < data.flows.length; ++i) {
				var flow = data.flows[i];
				flows.push(new Flow(ports[flow[0]], ports[flow[1]], flow[2], flow[3]));
			};
			this.setNetworkFlow(ports, flows);
		} catch (err) {
			console.log(err);
		}
		return this;
	},

    /*!
     *  Sets the maximum path width (see getMaxPathWidth for details).
     */
	setMaxPathWidth: function(maxWidth) {
	    this._maxPathWidth = maxWidth;
	    return this;
	},

	/*! Compute the global network flow and route paths
	 * that correspond to these flows that will be displayed
	 * on top of the map.
	 * @param {Object} ports - an object indexing all ports where
	 *        flows are being reported. E.g. ports['name of port'] = L.LatLng(...);
	 * @param {Array} flows - a collection of flows connecting points in ports.
	 */
	setNetworkFlow: function(ports, flows) {
		this.clearNetwork();
		var clusters = new L.markerClusterGroup({
			chunkedLoading: true,
			removeOutsideVisibleBounds: false
		});
		var markers = { };
		var names = { };
		for (var name in ports) {
			var marker = new L.Marker(ports[name], { icon: this._icon, title: 'Port ' + name });
			var key = this._latLngEncode(ports[name]);
			markers[key] = marker;
			names[key] = name;
			clusters.addLayer(marker);
		}
		var self = this;
		var cache = { };
		var generateClusterFlow = function() {
			self.clearNetwork();
			self.addLayer(clusters);
			self._networkLayers.push(clusters);
			var zoom = self._map.getZoom();
		    if (!cache[zoom]) {
		        // Since this is potentially costly, we cache the
		        // cluster flow according to zoom levels for reuse.
                var locations = new LocationIndex();
                var clusterFlow = [ ];
                for (var i = 0; i < flows.length; ++i) {
                    var flow = flows[i];
                    var sourceKey = self._latLngEncode(flow.source);
                    var destinationKey = self._latLngEncode(flow.destination);
                    var source = clusters.getVisibleParent(markers[sourceKey]);
                    var destination = clusters.getVisibleParent(markers[destinationKey]);
                    source = source ? source.getLatLng() : flow.source;
                    destination = destination ? destination.getLatLng() : flow.destination;
                    locations.add(source, names[sourceKey]);
                    locations.add(destination, names[destinationKey]);
                    clusterFlow.push(new Flow(source, destination, flow.volume, flow.netVolume));
                }
                var network = self._totalNetworkFlow(clusterFlow);
                cache[zoom] = function() { self._internalDraw(network, locations.names()); };
			}
			cache[zoom]();
		};
		this.draw = generateClusterFlow;
		this.draw();
		clusters.on('animationend', this.draw);
		return this;
	},

	/*!
	 *  Sets the opacity of flow paths.
	 */
	setPathOpacity: function(opacity) {
		if (opacity < 0 || opacity > 1) opacity = 1.0;
		this._pathOpacity = opacity;
		this.draw();
		return this;
	},

	// Private Methods.

	/*!	Curve calc function for canvas 2.3.1
	 *	Epistemex (c) 2013-2014
	 *	License: MIT
	 *
	 * Calculates an array containing points representing a cardinal spline through given point array.
	 * Points must be arranged as: [x1, y1, x2, y2, ..., xn, yn].
	 *
	 * The points for the cardinal spline are returned as a new array.
	 *
	 * @param {Array} points - point array
	 * @param {Number} [tension=0.5] - tension. Typically between [0.0, 1.0] but can be exceeded
	 * @param {Number} [numOfSeg=20] - number of segments between two points (line resolution)
	 * @param {Boolean} [close=false] - Close the ends making the line continuous
	 * @returns {Float32Array} New array with the calculated points that was added to the path
	 */
	_getCurvePoints: function(points, tension, numOfSeg, close) {
		'use strict';

		// options or defaults
		tension = (typeof tension === 'number') ? tension : 0.5;
		numOfSeg = numOfSeg ? numOfSeg : 25;

		var pts,									// for cloning point array
			i = 1,
			l = points.length,
			rPos = 0,
			rLen = (l-2) * numOfSeg + 2 + (close ? 2 * numOfSeg: 0),
			res = new Float32Array(rLen),
			cache = new Float32Array((numOfSeg + 2) * 4),
			cachePtr = 4;

		pts = points.slice(0);

		if (close) {
			pts.unshift(points[l - 1]);				// insert end point as first point
			pts.unshift(points[l - 2]);
			pts.push(points[0], points[1]); 		// first point as last point
		}
		else {
			pts.unshift(points[1]);					// copy 1. point and insert at beginning
			pts.unshift(points[0]);
			pts.push(points[l - 2], points[l - 1]);	// duplicate end-points
		}

		// cache inner-loop calculations as they are based on t alone
		cache[0] = 1;								// 1,0,0,0

		for (; i < numOfSeg; i++) {

			var st = i / numOfSeg,
				st2 = st * st,
				st3 = st2 * st,
				st23 = st3 * 2,
				st32 = st2 * 3;

			cache[cachePtr++] =	st23 - st32 + 1;	// c1
			cache[cachePtr++] =	st32 - st23;		// c2
			cache[cachePtr++] =	st3 - 2 * st2 + st;	// c3
			cache[cachePtr++] =	st3 - st2;			// c4
		}

		cache[++cachePtr] = 1;						// 0,1,0,0

		// calc. points
		parse(pts, cache, l);

		if (close) {
			//l = points.length;
			pts = [];
			pts.push(points[l - 4], points[l - 3], points[l - 2], points[l - 1]); // second last and last
			pts.push(points[0], points[1], points[2], points[3]); // first and second
			parse(pts, cache, 4);
		}

		function parse(pts, cache, l) {

			for (var i = 2, t; i < l; i += 2) {

				var pt1 = pts[i],
					pt2 = pts[i+1],
					pt3 = pts[i+2],
					pt4 = pts[i+3],

					t1x = (pt3 - pts[i-2]) * tension,
					t1y = (pt4 - pts[i-1]) * tension,
					t2x = (pts[i+4] - pt1) * tension,
					t2y = (pts[i+5] - pt2) * tension;

				for (t = 0; t < numOfSeg; t++) {

					var c = t << 2, //t * 4;

						c1 = cache[c],
						c2 = cache[c+1],
						c3 = cache[c+2],
						c4 = cache[c+3];

					res[rPos++] = c1 * pt1 + c2 * pt3 + c3 * t1x + c4 * t2x;
					res[rPos++] = c1 * pt2 + c2 * pt4 + c3 * t1y + c4 * t2y;
				}
			}
		}

		// add last point
		l = close ? 0 : points.length - 2;
		res[rPos++] = points[l];
		res[rPos] = points[l+1];

		return res;
	},

	/*! Determines how close two points in _routeNodes
	 * have to be in order to be consider adjacent.
	 */
	_implicitNeighborhoodRange: function() {
		return Math.min(11, Math.max(6, 60 / this._map.getPixelToLatScale())) * 100000;
	},

	_internalDraw: function(network, locations) {
		var pathOpacity = this._pathOpacity || 1.0;
		var pathColor = this._pathColor;
		var result = [ ];
		var maxVolume = 0;
		for (var i = 0; i < network.length; ++i) {
			var vol = network[i].volume;
			if (vol > maxVolume) {
				maxVolume = vol;
			}
		}
		var maxWidth = Math.min(this._maxPathWidth, this._map.getPixelToLatScale() * 2.5);
		var widthScale = maxVolume > maxWidth ? (maxWidth / maxVolume) : 1.0;
		var polyLineBuilder = function(path, lWeight) {
			return L.polyline(path, {
				weight: lWeight,
				opacity: pathOpacity,
				color: pathColor
			});
		};
		for (var i = 0; i < network.length; ++i) {
			var flow = network[i];
			var path = this._smoothPolyline(flow.path);
			var lWeight = 3.0 + flow.volume * widthScale;
			var line = polyLineBuilder(path, lWeight);
			var popup = null;
			var sourceName = locations[this._latLngEncode(flow.path[0])];
			var destinationName = locations[this._latLngEncode(flow.path[flow.path.length - 1])];
			var numbersInfo = 'Embarked: ' + flow.volume + '. Disembarked: ' + flow.netVolume + '.';
			if (flow.initial) {
				popup = 'Source ' + sourceName + '<br>Outbound traffic. ' + numbersInfo;
			}
			if (flow.terminal) {
				// Trim polyline and apply arrow symbol to a virtual 
				// poly line reaching the final point. This whole
				// trick is necessary because some paths will be drawn
				// with thick lines that ruin the arrow head tip.
				var arrowSize = Math.min(maxWidth * 3, 4 * lWeight);
				var finalPoint = path[path.length - 1];
				path = this._trimPolyline(path, arrowSize - lWeight / 2);
				line = polyLineBuilder(path, lWeight);
				var virtualPath = path.slice(0);
				virtualPath.splice(-1);
				virtualPath.push(finalPoint);
				var virtualLine = L.polyline(virtualPath, {
					opacity: 0.0,
				});
				var arrowSymbol = L.Symbol.arrowHead({
				    polygon: true,
					pixelSize: arrowSize,
					headAngle: 60,
					pathOptions: {
						stroke: false,
						weight: 2,
						fillOpacity: pathOpacity,
						color: pathColor
					}
				});
				var arrowHead = this.addLayer(L.polylineDecorator(virtualLine));
				this._networkLayers.push(arrowHead);
				arrowHead.setPatterns([
					{ offset: '100%', repeat: 0, symbol: arrowSymbol}
				]);
				popup = 'Destination ' + destinationName + '<br>Inbound traffic. ' + numbersInfo;
			}
			if (flow.terminal || flow.initial) {
				line.on('mouseover', function() {
					this.setStyle({ weight: Math.min(maxWidth * 1.3, 2 * this.originalWeight) });
				});
				line.on('mouseout', function() {
					this.setStyle({ weight: this.originalWeight });
				});
			}
			if (flow.initial && flow.terminal) {
				popup = 'Traffic from ' + sourceName + ' to ' + destinationName + '. ' + numbersInfo;
			}
			if (popup) {
				line.bindPopup(popup);
			}
			line.originalWeight = lWeight;
			this.addLayer(line);
			this._networkLayers.push(line);
		}
	},

	_latLngEncode: function(latLng) {
		return latLng.lat + "_" + latLng.lng;
	},

	/*! An implementation of the A* algorithm for path search.
	 * @param {LatLng} start - the starting point
	 * @param {LatLng} end - the end point
	 * @param {Array} routeNodes - array of LatLng nodes which are used for routing
	 * @returns {Array} An array of LatLng points which is a path from start to end.
	 */
	_routeFinder: function(start, end) {
		implicitNeighborhoodRange = this._implicitNeighborhoodRange() || 600000;
		routeNodes = this._routeNodes;
		var heuristicFn = function(a) {
			return a.point.distanceTo(end) + a.pathLength;
		};
		var openSet = [ { "point": start, "pathLength": 0, "parent": null, "isOpen": true } ];
		var availableNodes = [ ];
		for (var i = 0; i < routeNodes.length; ++i) {
			availableNodes.push( { "point": routeNodes[i], "pathLength": null, "parent": null, "isOpen": false } );
		}
		availableNodes.push( { "point": end, "pathLength": null, "parent": null, "isOpen": false } );
		var solution = null;
		while (openSet.length > 0) {
			// Adjacent nodes.
			var current = openSet[0];
			if (current.point == end) {
				solution = current;
				break;
			}
			current.isOpen = false;
			var index = availableNodes.indexOf(current);
			if (index >= 0) {
				availableNodes.splice(index, 1);
			}
			openSet.splice(0, 1);
			availableNodes.sort(function(a, b) {
				return a.point.distanceTo(current.point) - b.point.distanceTo(current.point);
			});
			var expanded = false;
			for (var i = 0; i < availableNodes.length; ++i) {
				var point = availableNodes[i].point;
				var dist = point.distanceTo(current.point);
				// If the node is not an implicit neighbor we penalize its
				// distance. This ensures that long jumps are still available
				// if we need them, but they will be kept as short as possible.
				if (dist > implicitNeighborhoodRange) dist *= 10;
				if (!availableNodes[i].isOpen ||
						availableNodes[i].pathLength > dist + current.pathLength) {
                    // Either the node is not on the open set or
                    // we found a shorter path from the start.
					var node = availableNodes[i];
					node.pathLength = dist + current.pathLength;
					node.parent = current;
					if (!node.isOpen) {
						node.isOpen = true;
						openSet.push(node);
					}
					expanded = true;
				}
			}
			if (!expanded) {
				// Must find a long jump that gets us closer to the goal.;
				for (var i = 0; !expanded && i < availableNodes.length; ++i) {
					var point = availableNodes[i].point;
					var dist = 10 * point.distanceTo(current.point);
					if (!availableNodes[i].isOpen || availableNodes[i].pathLength > dist + current.pathLength) {
						var node = availableNodes[i];
						node.pathLength = dist + current.pathLength;
						node.parent = current;
						if (!node.isOpen) {
							node.isOpen = true;
							openSet.push(node);
						}
						expanded = true;
					}
				}
			}
			openSet.sort(function(a, b) {
				return heuristicFn(a) - heuristicFn(b);
			});
		}
		// Collect coordinates of the optimized path.
		var result = [ ];
		var iterator = solution;
		while (iterator) {
			result.unshift(iterator.point);
			iterator = iterator.parent;
		}
		return result;
	},

	_smoothPolyline: function(points) {
		var coords = [ ];
		for (var i = 0; i < points.length; ++i) {
			coords.push(points[i].lng);
			coords.push(points[i].lat);
		}
		// Interpolate points for a smooth path.
		var smooth = this._getCurvePoints(coords, 0.4, 20, false);
		var result = [ ];
		for (var k = 0; k < smooth.length; k += 2) {
			result.push(new L.LatLng(smooth[k + 1], smooth[k]));
		}
		return result;
	},

	/*! A method that computes the total network flow.
	 *
	 *  Find routes on the map connecting each pair
	 *  of coordinates in globalFlows. Then merge all
	 *  flows in a single network.
	 *
	 * @param {Array} globalFlows - an array of Flow objects
	 * @param {Array} routeNodes - the nodes that can be used
	 * to route paths from the sources to destinations in
	 * globalFlows.
	 * @returns {Array} an array of Flow objects which form
	 * the total network flow.
	 */
	_totalNetworkFlow: function(globalFlows) {
		// Encoding LatLng objects as text.
		// Associative array node coordinates encoded as %lat_%lng
		// mapping to an array of route incidences (route, index of coord
		// in the route path, volume flowing over the route).
		var usedNodes = { };
		for (var i = 0; i < globalFlows.length; ++i) {
			var flow = globalFlows[i];
			var route = this._routeFinder(flow.source, flow.destination);
			for (var j = 0; j < route.length; ++j) {
				var label = this._latLngEncode(route[j]);
				var incidence = { "index": j, "routeIndex": i, "route": route, "volume": flow.volume, "netVolume": flow.netVolume };
				if (!usedNodes.hasOwnProperty(label)) {
					usedNodes[label] = { "incidences": [ incidence ], "links": [ ] };
				} else {
					usedNodes[label].incidences.push(incidence);
				}
			}
		}
		var self = this;
		var linkEnc = function(a, b) {
			return self._latLngEncode(a) + "x" + self._latLngEncode(b);
		}
		var usedLinks = {};
		for (var label in usedNodes) {
			var incidences = usedNodes[label].incidences;
			for (var i = 0; i < incidences.length; ++i) {
				var theIncidence = incidences[i];
				var index = theIncidence.index;
				var route = theIncidence.route;
				if (index < route.length - 1) {
					var linkLabel = linkEnc(route[index], route[index + 1]);
					var initial = (index == 0);
					var terminal = (index == route.length - 2);
					var link = null;
					if (!usedLinks.hasOwnProperty(linkLabel)) {
						link = new Flow(route[index], route[index + 1], theIncidence.volume, theIncidence.netVolume, initial, terminal);
						link.routes = [ theIncidence.routeIndex ];
						usedLinks[linkLabel] = link;
					} else {
						link = usedLinks[linkLabel];
						link.volume += theIncidence.volume;
						link.netVolume += theIncidence.netVolume;
						link.terminal |= terminal;
						link.routes.push(theIncidence.routeIndex);
					}
					var links = usedNodes[label].links;
					links.pushUnique(link);
				}
			}
		}
		for (var label in usedLinks) {
			var link = usedLinks[label];
			link.routes.sort();
		}
		var mergeableLink = function(link) {
			var nextNode = usedNodes[self._latLngEncode(link.destination)];
			for (var i = 0; i < nextNode.links.length; ++i) {
				var candidate = nextNode.links[i];
				if (candidate != link && link.routes.arrayEquals(candidate.routes)) {
					return candidate;
				}
			}
			return null;
		};
		var result = [ ];
		for (var label in usedLinks) {
			var link = usedLinks[label];
			if (link.merged) continue;
			// Merge consecutive links if they carry the same flow.
			var nextNode = usedNodes[this._latLngEncode(link.destination)];
			var merge = [ link.source, link.destination ];
			var nextLink = null;
			link.merged = true;
			while ((nextLink = mergeableLink(link)) != null) {
				link = nextLink;
				link.merged = true;
				merge.push(link.destination);
			}
			if (merge.length > 2) {
				result.push(new Flow(merge[0], merge[merge.length - 1], link.volume, link.netVolume, usedLinks[label].initial, link.terminal, merge));
			} else {
				result.push(link);
			}
		}
		return result;
	},
	
	/*!
	 *  Trim the given polyline so that the new final point
	 *  is at least the given number of pixels away from
	 *  the previous final point.
	 *
	 *  The result is dependent on the current zoom level.
	 *
	 *  @param {Array} latLngs - array of L.LatLng objects defining the polyline.
	 *  @param {Integer} pixels - how many pixels to trim.
	 */
	_trimPolyline: function(latLngs, pixels) {
		var n = latLngs.length;
		var zoom = this._map.getZoom();
		var lastPoint = this._map.project(latLngs[n - 1], zoom);
		var lastInsideRange = n - 1;
		for (var i = n - 2; i >= 0; --i) {
			var point = this._map.project(latLngs[i], zoom);
			if (point.distanceTo(lastPoint) > pixels) break;
			lastInsideRange = i;
		}
		// Edge case: the entire polyline falls within the pixel range.
		if (lastInsideRange == 0) return latLngs;
		var ptA = this._map.project(latLngs[lastInsideRange - 1], zoom);
		var ratio = pixels / ptA.distanceTo(lastPoint);
		var ptB = L.point(
			ptA.x * ratio + lastPoint.x * (1 - ratio),
			ptA.y * ratio + lastPoint.y * (1 - ratio)
		);
		latLngs.splice(lastInsideRange);
		latLngs.push(this._map.unproject(ptB, zoom));
		return latLngs;
	}
};