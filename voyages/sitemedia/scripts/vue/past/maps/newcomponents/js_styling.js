function personorpeople(count){
	if (count===1) {
		var result="person"
	} else {
		var result="people"
	}
	return result
};

function nodelogvaluescale_fn(points,min,max) {
	var valueMin = d3.min(points.features, function (p) {
		return p.properties.size;
	  });
	  var valueMax = d3.max(points.features, function (p) {
		return p.properties.size;
	  });
	return d3.scaleLog().domain([valueMin, valueMax]).range([min, max]);
}


function routeslogvaluescale_fn(routes,min,max) {
	var mapRouteValueMin = d3.min(routes, function (r) {
		return r.weight;
	});
	var mapRouteValueMax = d3.max(routes, function (r) {
		return r.weight;
	});
  return d3.scaleLog().domain([mapRouteValueMin, mapRouteValueMax]).range([min,max]);
}



function legColorPicker(leg_type,alpha=1) {
	if (leg_type == 'final_destination') {
		var thiscolor=d3.color("rgba(246,193,60,"+alpha+")");
	} else if (leg_type == 'origin') {
		var thiscolor=d3.color("rgba(96,192,171,"+alpha+")");
	} else {
		var thiscolor=d3.color("rgba(215,153,250,"+alpha+")");		
	};
	return thiscolor;
};
	
//Node color rules:
//Priority given to embarkations & disembarkations, and their combination
//So my only color "scale" is red<-->blue
//Only nodes that have no embark or disembark get colored as yellow (final destination) or green (origin)
function nodeColorPicker(nodeclasses) {
	if ('embarkation' in nodeclasses || 'disembarkation' in nodeclasses) {
		if ('embarkation' in nodeclasses && 'disembarkation' in nodeclasses) {
			var embark=nodeclasses.embarkation.count;
			var disembark=nodeclasses.disembarkation.count;
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
	} else if ('post-disembarkation' in nodeclasses) {
		var thiscolor=d3.rgb(246,193,60);
	} else if ('origin' in nodeclasses) {
		var thiscolor=d3.rgb(96,192,171);
	};
	return thiscolor
}

function formatNodePopUpListItem(k,v) {
	var nodeclass_labels={
		'embarkation':'embarked',
		'disembarkation':'disembarked',
		'post-disembarkation':'ended up',
		'origin':'originated'
	};
	
	var label = nodeclass_labels[k];
	var count = v.count;
	var key = v.key;
	var formattedstring=[count.toString(),personorpeople(count),label].join(' ')
	if (k!='origin') {
		var text='<a href="#" onclick="linkfilter(' + key.toString() + ',\'' + k + '\'); return false;">' + formattedstring + '</a>'
	} else {
		var text = false
	};
	return text;
};