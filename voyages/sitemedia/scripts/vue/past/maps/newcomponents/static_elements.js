// UPPER-LEFT LEGEND/LINK SHOWING THE TOTAL NUMBER OF PEOPLE IN THE SEARCH RESULT
// borrowed from https://codepen.io/haakseth/pen/KQbjdO
function drawUpdateCount(map,results_count) {
	var results_count_div = L.control({ position: "topleft" });
	results_count_div.onAdd = function(map) {
		var div = L.DomUtil.create("div", "legend");
		div.innerHTML += '<p class="legendp"><a href="#results">'+results_count.toString()+' '+pluralorsingular("Liberated African",results_count)+'.<br/>← Read their names</a></p>';
		return div
	};
	results_count_div.addTo(map);
};

// LOWER LEFT LEGEND SHOWING THE COLOR CODES FOR THE NODES
function drawLegend(map) {
	var legend_div = L.control({ position: "bottomleft" });
	legend_div.onAdd = function(map) {
		var div = L.DomUtil.create("div", "legend");
		div.innerHTML= '<table class=legendtable>\
			<tr>\
				<td><div class="circle" style="background-color:rgb(167,224,169);"></div><td>\
				<td>' + gettext('Origins') + '\
				<span id="origins_map_key_pill" data-toggle="tooltip" class="badge badge-pill badge-secondary tooltip-pointer" title="Origins are derived from user contributions."> IMP </span>\
				</td>\
			</tr>\
			<tr>\
				<td><div class="circle" style="background-color:rgb(255,0,0);"></div><td>\
				<td>'+gettext('Embarkations')+'</td>\
			</tr>\
			<tr>\
				<td><div class="circle" style="background-color:rgb(163,0,255);"></div><td>\
				<td>Embark & Disembark</td>\
			</tr>\
			<tr>\
				<td><div class="circle" style="background-color:rgb(0,0,255);"></div><td>\
				<td>' + gettext('Disembarkations') + '</td>\
			</tr>\
			<tr>\
				<td><div class="circle" style="background-color:rgb(246,193,60);"></div><td>\
				<td>'+gettext('Post-Disembark Locations')+'</td>\
			</tr>\
			</table>\
			'
		return div
	};
	legend_div.addTo(map);
	$(function () {
		$('[data-toggle="tooltip"]').tooltip()
	})
};

function add_control_layers_to_map(featurelayers,map) {
	var layerControl = L.control.layers(null,featurelayers).addTo(map);
	L.control.scale({ position: "bottomright" }).addTo(map);
}