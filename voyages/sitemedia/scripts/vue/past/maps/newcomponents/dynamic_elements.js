function tablemaker(tablerowdata,displaylimit,tablenameheader,tableheaderrow) {
	
	
	var tablehtml="<center><table class='lgmaptable'><tr><td>"+tableheaderrow[0]+"</td><td>"+tableheaderrow[1]+"</td></tr>"
	
	function maketablerow(name,count){
		return "<tr><td>"+name+"</td><td>"+count.toString()+"</tr>"
	}
	
	var rowcount=1
	
	var totalscount=0
	
	var excluded_clustered_dialect_lg_rows={}
	
	var least_included_value=100000000
	
	Object.keys(clustered_dialects).forEach(c=>{excluded_clustered_dialect_lg_rows[clustered_dialects[c]]={'lgcount':0,'peoplecount':0}})
	
	var excluded_nonclustered_lg_rows={'lgcount':0,'peoplecount':0}
	
	tablerowdata.forEach(r=>{
		
		var languagegroup=r.lg
		var languagegrouppeoplecount=r.value
		
		if (languagegrouppeoplecount<least_included_value) {
			least_included_value=languagegrouppeoplecount
		}
		
		totalscount+=languagegrouppeoplecount
		
		if (rowcount<displaylimit) {
			
			tablehtml+=maketablerow(languagegroup,languagegrouppeoplecount)
		
		} else {
			
			if (Object.keys(clustered_dialects).includes(languagegroup)){
				var lgcluster=clustered_dialects[languagegroup]
				excluded_clustered_dialect_lg_rows[lgcluster].lgcount+=1
				excluded_clustered_dialect_lg_rows[lgcluster].peoplecount+=languagegrouppeoplecount
			} else {
				excluded_nonclustered_lg_rows.lgcount+=1
				excluded_nonclustered_lg_rows.peoplecount+=languagegrouppeoplecount
			}
		}
		
		rowcount+=1
		
	})
	
	Object.keys(excluded_clustered_dialect_lg_rows).forEach(c=>{
		
		var clusterdata=excluded_clustered_dialect_lg_rows[c]
		
		var peoplecount=clusterdata.peoplecount
		
		if (peoplecount>least_included_value) {
			
			var namecell=clusterdata.lgcount.toString() +" more "+c+" "+pluralorsingular('dialect',clusterdata.lgcount)
			
			tablehtml+=maketablerow(namecell,clusterdata.peoplecount)
			
		} else {
			excluded_nonclustered_lg_rows.lgcount+=1
			excluded_nonclustered_lg_rows.peoplecount+=peoplecount
		}
		
	})
	
	if (excluded_nonclustered_lg_rows.peoplecount>0) {
		var formatted_tablenameheader=pluralorsingular(tablenameheader,excluded_nonclustered_lg_rows.lgcount)
		var namecell=excluded_nonclustered_lg_rows.lgcount.toString()+" other "+formatted_tablenameheader
		tablehtml+=maketablerow(namecell,excluded_nonclustered_lg_rows.peoplecount)
	}
	
	tablehtml+=maketablerow("Total",totalscount)
	
	
	tablehtml+="</table></center>"

	return tablehtml
}

function make_origin_and_final_nodes_table(markers,cluster_class) {	
	//markerclusters contain lots of different kinds of "markers" -- to get at our geojson ones, we have to filter
	//there's likely a smarter way to do this
	
	
	if (cluster_class=='origin') {
		var tablenameheader='Language Group'
		
		var tableheaderrow=[
			"Language Group  <span id=\"origins_map_key_pill\" data-toggle=\"tooltip\" class=\"badge badge-pill badge-secondary tooltip-pointer\" title=\"Origins are derived from user contributions.\"> IMP </span>",
			"Number of Liberated Africans with Identified Languages"			
		]
		
	} else if (cluster_class=='final_destination') {
		var tablenameheader='Last Known Location'
		
		var tableheaderrow=[
			"Last Known Location",
			"Number of Liberated Africans"			
		]
		
	}
	
	
	var tablerowdata=new Array;
	Object.keys(markers).forEach(marker_id=>{
		if (markers[marker_id])	{	
			if (markers[marker_id].feature){
				var markerprops=markers[marker_id].feature.properties;
				tablerowdata.push({
					"lg":markerprops.name,
					"value":markerprops.size
				})
			}
		}
	})
	tablerowdata.sort((a,b)=>a.value-b.value);
	tablerowdata.reverse()

	var tablehtml=tablemaker(tablerowdata,5,tablenameheader,tableheaderrow)
	
	return tablehtml
}


function formatNodePopUpListItem(k,v) {
	var nodeclass_labels={
		'embarkation':'embarked',
		'disembarkation':'disembarked',
		'origin':'originated'
	};
	
	var count = v.count||0;
	var key = v.key||null;
	
	if (k=="post-disembarkation") {
	
		formattedstring=[count.toString(),pluralorsingular("Liberated African",count)].join(' ')
		
	} else {
		var label = nodeclass_labels[k];
		var formattedstring=[count.toString(),pluralorsingular("Liberated African",count),label].join(' ')
		
	}
	
	if (key && k!='origin') {
		var text='<a href="#" onclick="linkfilter(' + key.toString() + ',\'' + k + '\'); return false;">' + formattedstring + '</a>'
	} else {
		var text = false
	};
	return text;
};


function makeNodePopUp(feature,nodesdict,edgesdict) {
// 	var popupsubheads=new Object;
	var node_classes=feature.properties.node_classes;
	var node_title=feature.properties.name;
	//a node can have multiple classes (mostly this is for sierra leone)
// 	Object.entries(node_classes).forEach(([k,v]) => popupsubheads[k]=formatNodePopUpListItem (k,v));
	
	var popupcontent=''
	
	if (node_classes['origin']) {
		var count=node_classes['origin']['count'];
		popupcontent=[count,pluralorsingular("Liberated African",count),"with",node_title,"origins."].join(" ")
	} else {
		if (node_classes['embarkation'] || node_classes ['disembarkation']) {
			var popupsubheads=new Array;
			var emb_disemb_classes=['embarkation','disembarkation']
			emb_disemb_classes.forEach(k=>{
				if (node_classes[k]) {
					popupsubheads.push(formatNodePopUpListItem(k,node_classes[k]))
				}
			})
			popupcontent+=popupsubheads.join(' and ') + " in " + node_title + ". ";
		}
		
		if (node_classes['post-disembarkation']) {
			popupcontent+="This is the final known location for " + formatNodePopUpListItem('post-disembarkation',node_classes['post-disembarkation']) + '.'
			
		}
	
	}
	
	
	
	
// 	if (!popupsubheads.includes(false)){
// 		if (popupsubheads.length>2) {
// 			
// 			popupcontent=popupsubheads.slice(0,-1).join(", ")
// 			popupcontent+=", and " + popupsubheads.slice(-1) + " in " + node_title;
// 			
// 		} else {
// 			var popupcontent=popupsubheads.join(' and ') + " in " + node_title;
// 		}
// 	} else {
// 		if (node_classes['origin']){
// 			var count=node_classes['origin']['count'];
// 			var popupcontent=[count,pluralorsingular("Liberated African",count),"with",node_title,"origins."].join(" ")
// 		} else {
// 			popupcontent=false
// 		}
// 	}
	
	//don't make a table for certain nodes, e.g., "other africa"
	var bad_aggregation_nodes=[60900]
	
	if (Object.keys(node_classes).includes('embarkation') && !bad_aggregation_nodes.includes(feature.properties.point_id)) {

		var tablerowdata=new Array;
		var tablerowdatakeys=new Object;
		var excludedpeoplecount=0;
		feature.properties.hidden_edges.forEach(e_id=>{
			if (edgesdict[e_id]){
				
				var edge=edgesdict[e_id]
				var st=edge.source_target
				var s_id=st[0]
				if (nodesdict[s_id]) {
					var source=nodesdict[s_id]
					var sourcedata=source._layers[Object.keys(source._layers)[0]].feature.properties
					
					if (Object.keys(sourcedata.node_classes).includes('origin')){
					
						var language_group=sourcedata.name
						var weight=edge.weight
					
						if (language_group in Object.keys(tablerowdatakeys)) {
							tablerowdatakeys[language_group]+=weight
						} else {
							tablerowdatakeys[language_group]=weight
						}
						}
						
				}
			}
		})
		
		if (Object.keys(tablerowdatakeys).length>0) {
			Object.keys(tablerowdatakeys).forEach(lg=>{tablerowdata.push({'lg':lg,'value':tablerowdatakeys[lg]})})
			tablerowdata.sort((a,b)=>a.value-b.value);
			tablerowdata.reverse()
			var tableheaderrow=[
				"Language Group  <span id=\"origins_map_key_pill\" data-toggle=\"tooltip\" class=\"badge badge-pill badge-secondary tooltip-pointer\" title=\"Origins are derived from user contributions.\"> IMP </span>",
				"Number of Liberated Africans with Identified Languages"			
			]
			var tablehtml=tablemaker(tablerowdata,5,"Language Group",tableheaderrow)
			popupcontent+="<hr/>" +tablehtml
			

		}
	
	}
	
	$(function () {
		$('[data-toggle="tooltip"]').tooltip()
	})
	
	return(popupcontent);
};