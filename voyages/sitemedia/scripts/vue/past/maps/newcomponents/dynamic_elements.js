function tablemaker(tablerowdata,displaylimit) {
	var tablehtml="<center><table class='lgmaptable'><tr><td>Language Group</td><td>Number of Liberated Africans</td></tr>";	
		
	function maketablerow(name,count){
		return "<tr><td>"+name+"</td><td>"+count.toString()+"</tr>"
	}
	
	var rowcount=1
	
	var excluded_clustered_dialect_lg_rows={}
	
	Object.keys(clustered_dialects).forEach(c=>{excluded_clustered_dialect_lg_rows[clustered_dialects[c]]={'lgcount':0,'peoplecount':0}})
	
	var excluded_nonclustered_lg_rows={'lgcount':0,'peoplecount':0}
	
	tablerowdata.forEach(r=>{
		
		var languagegroup=r.lg
		var languagegrouppeoplecount=r.value
		
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
		
		if (clusterdata.peoplecount>0) {
			
			var namecell=clusterdata.lgcount.toString() +" more "+c+" "+pluralorsingular('dialect',clusterdata.lgcount)
			
			tablehtml+=maketablerow(namecell,clusterdata.peoplecount)
			
			
		}
		
	})
	
	
	
	if (excluded_nonclustered_lg_rows.lgcount>0) {
		var namecell=excluded_nonclustered_lg_rows.lgcount.toString()+" other language "+pluralorsingular('group',excluded_nonclustered_lg_rows.lgcount)
		tablehtml+=maketablerow(namecell,excluded_nonclustered_lg_rows.peoplecount)
	}
	
	
	tablehtml+="</table></center>"
	return tablehtml
}

function make_origin_nodes_languagegroupstable(markers) {	
	//markerclusters contain lots of different kinds of "markers" -- to get at our geojson ones, we have to filter
	//there's likely a smarter way to do this
	
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
	var tablehtml=tablemaker(tablerowdata,5)
	
	return tablehtml
}





function makeNodePopUp(feature,nodesdict,edgesdict) {
	var popupsubheads=[];
	var node_classes=feature.properties.node_classes;
	var node_title=feature.properties.name;
	//a node can have multiple classes (mostly this is for sierra leone)
	Object.entries(node_classes).forEach(([k,v]) => popupsubheads.push(formatNodePopUpListItem (k,v)));
	if (!popupsubheads.includes(false)){
		var popupcontent=popupsubheads.join(' and ') + " in " + node_title;
	} else {
		if (node_classes['origin']){
			var count=node_classes['origin']['count'];
			var popupcontent=[count,pluralorsingular("Liberated African",count),"with",node_title,"origins."].join(" ")
		} else {
			popupcontent=false
		}
	}
	
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
			var tablehtml=tablemaker(tablerowdata,5)
			popupcontent+="<hr/>" +tablehtml
		}
	
	
	}
	return(popupcontent);
};