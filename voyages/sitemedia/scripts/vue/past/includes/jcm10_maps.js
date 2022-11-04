
	
	function personorpeople(count){
		if (count===1) {
			var result="person"
		} else {
			var result="people"
		}
		return result
	};
	
	function drawUpdateRoutes(map, routes) {
// 	  console.log(routes);
	  var valueMin = d3.min(routes, function (r) {
		return r.weight;
	  });
	  var valueMax = d3.max(routes, function (r) {
		return r.weight;
	  });
	  
	  var valueScale = d3.scaleLog().domain([valueMin, valueMax]).range([1, 10]);
	  
	  function makePopUp(r) {
	  	var weightline = r.weight + " " + personorpeople(r.weight);
	  	return weightline;
	  };
	  
	  routes.map((route) => {
		var commands = [];
		commands.push("M", route.geometry[0][0]);
		commands.push("C", route.geometry[1][0], route.geometry[1][1], route.geometry[0][1]);
// 		console.log(commands);
		L.curve(commands, { color: "rgb(96,192,171)", weight: valueScale(route.weight) })
		  .bindPopup(makePopUp(route),{'maxHeight':'300'})
		  .addTo(map);
	  });
	}
	
// borrowed from https://codepen.io/haakseth/pen/KQbjdO
	function drawUpdateCount(map,results_count) {
		var results_count_div = L.control({ position: "topleft" });
		results_count_div.onAdd = function(map) {
			var div = L.DomUtil.create("div", "legend");
			div.innerHTML += '<p class="legendp"><a href="#results">'+results_count.toString()+' '+personorpeople(results_count)+' selected.<br/>← Read their names</a></p>';
			return div
		};
		results_count_div.addTo(map);
	};
	
	function drawLegend(map) {
		var legend_div = L.control({ position: "bottomleft" });
		legend_div.onAdd = function(map) {
			var div = L.DomUtil.create("div", "legend");
			div.innerHTML= '<table class=legendtable>\
				<tr>\
					<td><div class="circle" style="background-color:rgb(167,224,169);"></div><td>\
					<td>Origins</td>\
				</tr>\
				<tr>\
					<td><div class="circle" style="background-color:rgb(255,0,0);"></div><td>\
					<td>Embarkations</td>\
				</tr>\
				<tr>\
					<td><div class="circle" style="background-color:rgb(163,0,255);"></div><td>\
					<td>Embark & Disembark</td>\
				</tr>\
				<tr>\
					<td><div class="circle" style="background-color:rgb(0,0,255);"></div><td>\
					<td>Disembarkations</td>\
				</tr>\
				<tr>\
					<td><div class="circle" style="background-color:rgb(246,193,60);"></div><td>\
					<td>Post-Disembark Locations</td>\
				</tr>\
				</table>'
			return div
		};
		legend_div.addTo(map);
	};

	function drawUpdatePoints(map, points) {
// 	  console.log(points);
		function onEachFeature(feature, layer) {
			// does this feature have a property named popupContent?
			if (feature.properties && feature.properties.popupcontent) {
				layer.bindPopup(feature.properties.popupcontent);
			}
		};
		
		function colorPicker(nodeclasses) {
			if ('post-disembarkation' in nodeclasses) {
				var thiscolor=d3.rgb(246,193,60);
			} else if ('origin' in nodeclasses) {
				var thiscolor= d3.rgb(167,227,153);
			} else {
				if ('embarkation' in nodeclasses && 'disembarkation' in nodeclasses) {
					var embark=nodeclasses['embarkation'];
					var disembark=nodeclasses['disembarkation'];
					var embarkratio=embark/(embark+disembark)
					var disembarkratio=disembark/(embark+disembark)
					var thiscolor=d3.rgb(embarkratio*255,0,disembarkratio*255);
					return thiscolor
				} else {
					if ('embarkation' in nodeclasses) {
						var thiscolor=d3.rgb(255,0,0);
					} else if ('disembarkation' in nodeclasses) {
						var thiscolor=d3.rgb(0,0,255);
					}
				}
			}
			return thiscolor
		}
		
		//scale the nodes sizes logarithmically 
		
		var valueMin = d3.min(points.features, function (p) {
			return p.properties.size;
		  });
		  var valueMax = d3.max(points.features, function (p) {
			return p.properties.size;
		  });
	
		var valueScale = d3.scaleLog().domain([valueMin, valueMax]).range([1, 20]);  
		
		//while we're at it, let's make the map zoom & pan to fit our collection of points
		  
		  var latmin = d3.min(points.features, function (p) {
		  	return p.geometry.coordinates[1];
		  });
		  
		  var latmax = d3.max(points.features, function (p) {
		  	return p.geometry.coordinates[1]
		  });
		  
		  var longmin = d3.min(points.features, function (p) {
		  	return p.geometry.coordinates[0]
		  });
		  
		  var longmax = d3.max(points.features, function (p) {
		  	return p.geometry.coordinates[0]
		  });
		
		var minmax_group = new L.featureGroup([L.marker([latmin,longmin]),L.marker([latmax,longmax])]);
		map.fitBounds(minmax_group.getBounds());
		
	  
		L.geoJSON(points.features, {
			pointToLayer: function (feature, latlng) {
				return L.circleMarker(latlng, {
					radius: valueScale(feature.properties.size),
					fillColor: colorPicker(feature.properties.node_classes),
					color: "#000",
					weight: 1,
					opacity: 1,
					fillOpacity: 0.6
				});
				
			},
			onEachFeature: onEachFeature

		}).addTo(map);
	  
	};