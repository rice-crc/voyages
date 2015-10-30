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

	if (source == null) {
		console.log('source should not be null!');
	}
	if (destination == null) {
		console.log('destination should not be null!');
	}
}

/*!
 *  A class that stores global locations together with names
 *  identifying what they are.
 */
function LocationIndex() {
	this.locationType = PORT_LABEL;

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
				result[key] = col[0];
			} else {
				result[key] = '<ul><li>' + Array.prototype.join.call(col, "</li><li>") + '</li></ul>';
			}
		}
		return result;
	};
};

/*!
 *  A point in the global with a name.
 *  @param name - the name of the point.
 *  @param latLng - global position.
 *  @param nodeType - a string identifying the type of the node (e.g. port, region, broad region).
 */
function NamedPoint(name, latLng, nodeType, id) {
	this.name = name;
	this.latLng = latLng;
	this.nodeType = nodeType;
	this.id = id || 0;
}

/*!
 *  A port with parent region and grandparent broad region.
 *  @param namedPoint - the point corresponding to the port
 *  @param region - a NamedPoint corresponding to the region
 *                  this port belongs to.
 *  @param broad - a NamedPoint corresponding to the broad
 *                 region this port belongs to.
 */
function Port(namedPoint, region, broad) {
	namedPoint.nodeType = 'port';
	if (region) region.nodeType = 'region';
	if (broad) broad.nodeType = 'broadregion';
	this.namedPoint = namedPoint;
	this.region = region;
	this.broad = broad;

	/*!
	 *  Retrieves the NamedPoint at the given zoom level.
	 */
	this.getNamedPoint = function(level) {
		var result = null;
		if (level == 0) {
			result = this.broad;
		} else if (level == 1) {
			result = this.region;
		}
		return result || this.namedPoint;
	}
}

var _mapBoundaries = new L.LatLngBounds(
	new L.LatLng(-59.517932, -111.936579),
	new L.LatLng(63.9, 60.9)
);

// Helpful definitions when using Django templates.
var None = null;
var Nothing = null;

var PORT_LABEL = { singular: gettext('port'), plural: gettext('ports') };
var REGION_LABEL = { singular: gettext('region'), plural: gettext('regions') };
var BROAD_REGION_LABEL = { singular: gettext('broad region'), plural: gettext('broad regions') };

/*!
 *  A singleton that organizes all interactive
 *  features of the Voyages map.
 */
var voyagesMap = {
	// "Private" members
	__cache: { },
	_arrowOpacity: 1.0,
	_bounds: _mapBoundaries,
	_graphics: [ ],
	_icons: null,
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
		voyagesMap.clearNetwork();
		for (var i = 0; i < this._graphics.length; ++i) {
			voyagesMap._map.removeLayer(this._graphics[i]);
		}
		voyagesMap._graphics = [ ];
		voyagesMap.__cache = { };
		var noOp = function() {};
		voyagesMap.draw = noOp;
		voyagesMap.postDraw = noOp;
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
	 *  Gets the opacity for path arrows.
	 */
	getArrowOpacity: function() { return this._arrowOpacity; },

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
	 * @param {Array} links - an array of links, namely objects having
	 *                        start/end (indices in routeNodes), and length.
	 * @param markerIcons - object indexing {L.Icon} - each nodeType used
	 *                      in this map should have a corresponding icon.
	 */
	init: function(baseMapId, mapTilePrefix, routeNodes, links, markerIcons) {
		voyagesMap.clear();
		voyagesMap.loadBaseMap(baseMapId, mapTilePrefix);
		var filePrefix = mapTilePrefix + 'js/images/marker-icon-';
		voyagesMap._icons = markerIcons || {
    		    'port' : L.icon({ iconUrl: filePrefix + 'port.png', iconAnchor: [6, 6] }),
    		    'region' : L.icon({ iconUrl: filePrefix + 'region.png', iconAnchor: [6, 6] }),
    		    'broadregion' : L.icon({ iconUrl: filePrefix + 'broadregion.png', iconAnchor: [6, 6] }),
            };
		voyagesMap._routeNodes = routeNodes;
		if (!links || links.length == 0) {
			// Generate implicit links.
			links = [ ];
			implicitNeighborhoodRange = this._implicitNeighborhoodRange() || 600000;
			for (var i = 0; i < routeNodes.length; ++i) {
				for (var j = i + 1; j < routeNodes.length; ++j) {
					var dist = routeNodes[i].distanceTo(routeNodes[j]);
					if (dist < implicitNeighborhoodRange) {
						links.push({ start: i, end: j, length: dist });
						links.push({ start: j, end: i, length: dist });
					}
				}
			}
		}
		voyagesMap._processLinks(links);
		voyagesMap._map.off('zoomend', voyagesMap._runDraw);
		voyagesMap._map.on('zoomend', voyagesMap._runDraw);
		return voyagesMap;
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
            maxZoom: 8,
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
	 *  Specify a function that will run every time the network is drawn.
	 *  For instance, when the zoom level changes.
	 */
	postDraw: function() {
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
	 *  Sets the opacity of flow paths.
	 */
	setArrowOpacity: function(opacity) {
		if (opacity < 0 || opacity > 1) opacity = 1.0;
		this._arrowOpacity = opacity;
		this.draw();
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
		var cache = { };
		var locationTypes = [ BROAD_REGION_LABEL, REGION_LABEL, PORT_LABEL ];
		var self = this;
		var generateClusterFlow = function() {
			var zoomLevel = self._map.getZoom();
		    if (!self.__cache[zoomLevel]) {
		        // Since this is potentially costly, we cache the
		        // cluster flow according to detail levels for reuse.
		        var markers = [ ];
		        var uniqueMarkerCodes = { };
				var namedPointToMarker = function(np) {
					var code = self._latLngEncode(np.latLng);
					if (!uniqueMarkerCodes.hasOwnProperty(code)) {
						var marker = new L.Marker(np.latLng, {
							icon: self._icons[np.nodeType],
							title: np.name + ' (' +  gettext('click for details') + ')'
						});
						marker.code = code;
						marker.outFlowEmbarked = 0;
						marker.outFlowDisembarked = 0;
						marker.inFlowEmbarked = 0;
						marker.inFlowDisembarked = 0;
						marker.namedPoint = np;
						marker.name = np.name;
						markers.push(marker);
						uniqueMarkerCodes[code] = marker;
						return marker;
					} else {
						return uniqueMarkerCodes[code];
					}
				};
				var detailLevel = self.zoomToDetailLevel(zoomLevel);
                var locations = new LocationIndex();
                locations.locationType = locationTypes[detailLevel];
                var auxFlowData = [ ];
                for (var i = 0; i < flows.length; ++i) {
                    var flow = flows[i];
                    var sourcePort = ports[flow.source];
                    var destinationPort = ports[flow.destination];
                    var source = sourcePort.getNamedPoint(detailLevel);
                    var destination = destinationPort.getNamedPoint(detailLevel);
                    var markerSource = namedPointToMarker(source);
                    var markerDest = namedPointToMarker(destination);
                    markerSource.name = source.name;
                    markerDest.name = destination.name;
                    locations.add(source.latLng, source.name);
                    locations.add(destination.latLng, destination.name);
                    markerSource.broadRegion = sourcePort.broad;
                    markerDest.broadRegion = destinationPort.broad;
                    // Aggregate marker flows.
                    markerSource.outFlowEmbarked += flow.volume;
                    markerSource.outFlowDisembarked += flow.netVolume;
                    markerDest.inFlowEmbarked += flow.volume;
                    markerDest.inFlowDisembarked += flow.netVolume;
                    auxFlowData.push({ s: markerSource, d: markerDest, f: flow });
                }
                // Helper function that will create a table with node flow data.
                var buildAggregateTable = function(rows, totals, footer) {
                	if (footer) {
                		footer = '<tfoot>' + footer + '</tfoot>'
                	}
                	var inboundHeader = gettext('Africans arriving from Africa');
                	if (totals.broadRegion && (totals.broadRegion.id <= 1 || totals.broadRegion.name == "Africa")) {
                	    inboundHeader = gettext('Africans returning to Africa');
                	}
                	var table = '<div style="overflow-y: auto; overflow-x: hidden; max-height:250px; padding-right:20px;">' +
                	 	'<table class="map_node_aggregate_table">' +
                		'<thead><tr><th rowspan="2">' + locations.locationType.singular.toUpperCase() +
                		'</th><th colspan="2" class="inFlow">' + inboundHeader +
                		'</th><th colspan="2" class="outFlow">' + gettext('Africans carried off') + '</th></tr>' +
                		'<tr><th class="inFlow">' + gettext('Embarked') + '</th><th class="inFlow">' +
                		gettext('Disembarked') + '</th><th class="outFlow">' +
                		gettext('Embarked') + '</th><th class="outFlow">' + gettext('Disembarked') +
                		'</th></tr></thead><tbody><tr>' + rows.join('</tr><tr>') + '</tr></tbody>' + (footer || '') + '</table></div>';
					// See if we should omit inFlow or outFlow columns.
					if (totals.inFlowEmbarked == 0 && totals.inFlowDisembarked == 0) {
						table = table.replace(/inFlow/g, 'zero_value');
					}
					if (totals.outFlowEmbarked == 0 && totals.outFlowDisembarked == 0) {
						table = table.replace(/outFlow/g, 'zero_value');
					}
                	return table;
                }
                var nodeAggregateInfo = function(marker) {
                	return '<td><strong>' + marker.name + '</strong></td><td class="number inFlow">' +
						marker.inFlowEmbarked.toLocaleString() + '</td><td class="number inFlow">' +
						marker.inFlowDisembarked.toLocaleString() + '</td><td class="number outFlow">' +
						marker.outFlowEmbarked.toLocaleString() + '</td><td class="number outFlow">' +
						marker.outFlowDisembarked.toLocaleString() + '</td>';
                };
                var popupOptions = { maxWidth: '640px' };
                for (var code in uniqueMarkerCodes) {
                	var marker = uniqueMarkerCodes[code];
                	marker.bindPopup(buildAggregateTable([ nodeAggregateInfo(marker) ], marker), popupOptions);
                }
                // Create cluster group object and associated popups.
		        var clusterGroup = L.markerClusterGroup({
					iconCreateFunction: function (cluster) {
						var markers = cluster.getAllChildMarkers();
						markers.sort(function(a, b) {
							if (a.name < b.name)
								return -1;
							if (a.name > b.name)
								return 1;
							return 0;
						});
						var title = markers.length + ' ' + locations.locationType.plural + ' (' + gettext('click for details') + ')';
						// Set the popup here.
						var rows = [ ];
						var totals = { name: gettext('Totals'), inFlowEmbarked: 0, inFlowDisembarked: 0, outFlowEmbarked: 0, outFlowDisembarked: 0 };
						for (var i = 0; i < markers.length; ++i) {
							var marker = markers[i];
							rows.push(nodeAggregateInfo(marker));
							totals.broadRegion = marker.broadRegion;
							totals.inFlowEmbarked += marker.inFlowEmbarked;
							totals.inFlowDisembarked += marker.inFlowDisembarked;
							totals.outFlowEmbarked += marker.outFlowEmbarked;
							totals.outFlowDisembarked += marker.outFlowDisembarked;
						}
						cluster.bindPopup(buildAggregateTable(rows, totals, nodeAggregateInfo(totals)), popupOptions);
						return L.divIcon({
							html: '<div title="' + title + '"><span>' + markers.length + '</span></div>',
							className: 'leaflet-marker-icon marker-cluster ' +
								'leaflet-zoom-animated leaflet-clickable cluster-detail' + detailLevel,
							iconSize: L.point(40, 40)
						});
					},
					disableClusteringAtZoom: 8,
					zoomToBoundsOnClick: false,
				});
				// Add all markers in bulk.
				clusterGroup.addLayers(markers);
				// Compute cluster flow and network.
                var extractLatLng = function(p) {
					var pos = clusterGroup.getVisibleParent(p);
					if (pos && pos != p) {
						var clusterPos = pos.getLatLng();
						locations.add(clusterPos, p.name);
						return clusterPos;
					}
                    return p.getLatLng();
                };
				self.addLayer(clusterGroup);
				self._networkLayers.push(clusterGroup);
				var clusterFlow = [ ];
				for (var i = 0; i < auxFlowData.length; ++i) {
					var x = auxFlowData[i];
					var source = extractLatLng(x.s);
					var destination = extractLatLng(x.d);
					if (source.lat == destination.lat && source.lng == destination.lng) continue;
					var flow = new Flow(source, destination, x.f.volume, x.f.netVolume);
					clusterFlow.push(flow);
				}
				var network = self._totalNetworkFlow(clusterFlow);
                voyagesMap.__cache[zoomLevel] = function() {
					voyagesMap.addLayer(clusterGroup);
					voyagesMap._networkLayers.push(clusterGroup);
                    voyagesMap._internalDraw(network, locations.names());
                };
			}
            self.clearNetwork();
            voyagesMap.__cache[zoomLevel]();
		};
		this.draw = generateClusterFlow;
		this._runDraw();
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

	/*!
	 *  Translates a zoom level to a map detail level.
	 *  This is used to determine how to group nodes according
	 *  to their hierarchy.
	 */
	zoomToDetailLevel: function(zoom) {
	    if (zoom <= 3) return 0;
	    if (zoom <= 6) return 1;
	    return 2;
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
	    var arrowOpacity = this._arrowOpacity || 1.0;
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
			var path = flow.path.slice(0);
			path = this._smoothPolyline(path);
			var lWeight = 3.0 + flow.volume * widthScale;
			var line = polyLineBuilder(path, lWeight);
			var popup = null;
			var sourceName = locations[this._latLngEncode(flow.path[0])];
			var destinationName = locations[this._latLngEncode(flow.path[flow.path.length - 1])];
			var numbersInfo = '<br /><strong>' + gettext('Embarked') + ': </strong>' +
			 	flow.volume.toLocaleString() +
			 	'. <strong>' + gettext('Disembarked') + ': </strong>' +
			 	flow.netVolume.toLocaleString() + '.';
			if (flow.initial) {
				popup = '<strong>' + gettext('Place or region of embarkation:') + ' </strong>' +
				 	sourceName + numbersInfo;
			}
			if (flow.terminal) {
				// Trim polyline and apply arrow symbol to a virtual 
				// poly line reaching the final point. This whole
				// trick is necessary because some paths will be drawn
				// with thick lines that ruin the arrow head tip.
				var arrowSize = Math.min(maxWidth * 3, 4 * lWeight);
				var finalPoint = path[path.length - 1];
				var aux = 0;
				while ((aux = this._trimPolyline(path, arrowSize - lWeight / 2) / 2) < arrowSize) {
					arrowSize = aux;
				}
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
						fillOpacity: arrowOpacity,
						color: pathColor
					}
				});
				var arrowHead = this.addLayer(L.polylineDecorator(virtualLine));
				this._networkLayers.push(arrowHead);
				arrowHead.setPatterns([
					{ offset: '100%', repeat: 0, symbol: arrowSymbol}
				]);
				popup = '<strong>' + gettext('Place or region of disembarkation:') + ' </strong>' +
				 destinationName + numbersInfo;
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
				popup = '<strong>' + gettext('Place or region of embarkation:') + ' </strong>' + sourceName +
					' <strong><br />' + gettext('Place or region of disembarkation:') + '</strong> ' +
					destinationName + '.<br />' + numbersInfo;
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

	/*! Process links and create an array _outLinks on each route node
	 *  that can be used to access the links coming out of the node.
	 */
	_processLinks: function(links) {
		for (var i = 0; i < this._routeNodes.length; ++i) {
			this._routeNodes[i]._outLinks = [ ];
		}
		var nodeCount = this._routeNodes.length;
		for (var i = 0; i < links.length; ++i) {
			var link = links[i];
			if (link.start >= nodeCount || link.start < 0 || link.end >= nodeCount || link.end < 0) continue;
			var start = this._routeNodes[link.start];
			var end = this._routeNodes[link.end];
			link.length = start.distanceTo(end);
			start._outLinks.push(link);
		}
	},

	/*! An implementation of the A* algorithm for path search.
	 * @param {LatLng} start - the starting point
	 * @param {LatLng} end - the end point
	 * @param {Array} routeNodes - array of LatLng nodes which are used for routing
	 * @returns {Array} An array of LatLng points which is a path from start to end.
	 */
	_routeFinder: function(start, end) {
		// A penalty factor for making a connection between
		// two nodes that are NOT connected by a link.
		var PENALTY_MULTIPLIER = 100;
		var penalizedDist = function(dist) {
			return dist * dist * PENALTY_MULTIPLIER;
		};
		routeNodes = this._routeNodes;
		var nodes = [ ];
		var addNode = function(point) {
		    var item = {
		    	key: nodes.length,
		    	point: point,
		    	pathLength: null,
		    	parent: null,
		    	isOpen: false,
		    	distanceToEnd: point.distanceTo(end)
			};
			nodes.push(item);
			return item;
		};
		// Clone start and add simulated links to route nodes.
		start = new L.LatLng(start.lat, start.lng);
		start._outLinks = [ ];
		for (var i = 0; i < routeNodes.length; ++i) {
			var node = addNode(routeNodes[i]);
			start._outLinks.push({ start: -1, end: node.key, length: penalizedDist(node.point.distanceTo(start)) });
		}
		// The open set represents all nodes that can be reached from
		// the start position but for which there may be still a shorter
		// path connecting it to the start. Therefore a node may not be
		// open for two reasons: either we still have not found a path
		// from the start point, or we already found the shortest path.
		var openSet = [ ];
		// Helper function to update the open set once new paths are found.
		// Returns true if the new path is shorter than what was previously know (if any).
		var foundPathToNode = function(current, node, dist) {
			var result = !node.isOpen || node.pathLength > dist + current.pathLength;
			if (result) {
				// Either the node is not on the open set or
				// we found a shorter path from the start.
				node.pathLength = dist + current.pathLength;
				node.parent = current;
				if (!node.isOpen) {
					node.isOpen = true;
					openSet.push(node);
				}
			}
			return result;
		}
		var endNode = addNode(end);
		// Create fast access indices.
		var isAvailableIndex = [ ];
		for (var i = 0; i < nodes.length; ++i) {
			isAvailableIndex.push(true);
		}
		// An admissible heuristic is crucial to the correctness of the A* algorithm.
		var heuristicFn = function(a) {
			return a.distanceToEnd + a.pathLength;
		};
		// Pop the open node with smallest heuristic (estimate) for distance to target.
		var popOpen = function() {
			var minIndex = 0;
			for (var i = 1; i < openSet.length; ++i) {
			    if (heuristicFn(openSet[i]) < heuristicFn(openSet[minIndex])) minIndex = i;
			}
			var p = openSet[minIndex];
			openSet.splice(minIndex, 1);
			p.isOpen = false;
			isAvailableIndex[p.key] = false;
			return p;
		};
		var current = addNode(start);
		for (; current != endNode; current = popOpen()) {
			var outLinks = current.point._outLinks || [ ];
			for (var i = 0; i < outLinks.length; ++i) {
				var link = outLinks[i];
				if (isAvailableIndex[link.end]) {
					foundPathToNode(current, nodes[link.end], link.length);
				}
			}
			// Append a penalized direct path to end.
			foundPathToNode(current, endNode, penalizedDist(current.distanceToEnd));
		}
		// Collect coordinates of the optimized path.
		var result = [ ];
		var iterator = current;
		while (iterator) {
			result.unshift(iterator.point);
			iterator = iterator.parent;
		}
		return result;
	},

	_runDraw: function() {
		if (voyagesMap.draw) {
			voyagesMap.draw();
		}
		if (voyagesMap.postDraw) {
			voyagesMap.postDraw();
		}
	},

	_smoothPolyline: function(points) {
		// Helper functions to computes the angle
		// formed by 3 points.
		var self = this;
		var atan = function(x, y) {
			var theta = Math.atan2(x, y);
			return theta < 0 ? 2 * Math.PI + theta : theta;
		};
		var angle = function(p1, p2, p3) {
			var zoom = self._map.getZoom();
			var q1 = self._map.project(p1, zoom);
			var q2 = self._map.project(p2, zoom);
			var q3 = self._map.project(p3, zoom);
			var theta1 = atan(q1.x - q2.x, q1.y - q2.y);
			var theta2 = atan(q3.x - q2.x, q3.y - q2.y);
			return Math.abs(theta1 - theta2);
		};
		var removeSharpEnd = function(i) {
			var result = false;
			var theta = angle(points[i - 1], points[i], points[i + 1]);
			if (theta < Math.PI * 2 / 3) {
				points.splice(i, 1);
				result = true;
			}
			return result;
		};
		if (points.length > 2) {
			removeSharpEnd(1);
		}
		if (points.length > 2) {
			removeSharpEnd(points.length - 2);
		}
		var coords = [ ];
		for (var i = 0; i < points.length; ++i) {
			coords.push(points[i].lng);
			coords.push(points[i].lat);
		}
		// Interpolate points for a smooth path.
		var smooth = this._getCurvePoints(coords, 0.3, 20, false);
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
				var incidence = {
				    "index": j,
				    "routeIndex": i,
				    "route": route,
				    "volume": flow.volume,
				    "netVolume": flow.netVolume
                };
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
						link = new Flow(
						    route[index],
						    route[index + 1],
						    theIncidence.volume,
						    theIncidence.netVolume,
						    initial,
						    terminal);
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
				result.push(
				    new Flow(
                        merge[0],
                        merge[merge.length - 1],
                        link.volume,
                        link.netVolume,
                        usedLinks[label].initial,
                        link.terminal, merge
                    )
                );
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
	 *  @returns {Integer} distance between end-points of polyline in pixels.
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
		if (lastInsideRange == 0) {
			latLngs = [ latLngs[0], latLngs[n - 1]];
			n = 2;
			lastPoint = this._map.project(latLngs[n - 1], zoom);
		} else {
			var ptA = this._map.project(latLngs[lastInsideRange - 1], zoom);
			var ratio = pixels / ptA.distanceTo(lastPoint);
			var ptB = L.point(
				ptA.x * ratio + lastPoint.x * (1 - ratio),
				ptA.y * ratio + lastPoint.y * (1 - ratio)
			);
			latLngs.splice(lastInsideRange);
			latLngs.push(this._map.unproject(ptB, zoom));
		}
		var point = this._map.project(latLngs[0], zoom);
		return point.distanceTo(lastPoint);
	}
};