function tablemaker(tablerowdata,displaylimit,tablenameheader,tableheaderrow,linknames=false) {
	
	
	var tablehtml="<center><table class='lgmaptable'><tr><td>"+tableheaderrow[0]+"</td><td>"+tableheaderrow[1]+"</td></tr>"
	
	function maketablerow(name,count){
		return "<tr><td>"+name+"</td><td>"+count.toString()+"</tr>"
	}
	
	function makelinkedtablerow(name,count,key,tag){
		return "<tr><td><a href=\"#\" onclick=\"linkfilter(" + key.toString() + ',\''+tag+'\'); return false;\">'+name+"</a></td><td>"+count.toString()+"</tr>"
		
		
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
			
			if (linknames) {
				tablehtml+=makelinkedtablerow(languagegroup,languagegrouppeoplecount,r.key,r.tag)
			} else {
				tablehtml+=maketablerow(languagegroup,languagegrouppeoplecount)
			}
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
		var linknames=true
		var tableheaderrow=[
			"Language Group  <span id=\"origins_map_key_pill\" data-toggle=\"tooltip\" class=\"badge badge-pill badge-secondary tooltip-pointer\" title=\"Origins are derived from user contributions.\"> IMP </span>",
			"Number of Liberated Africans with Identified Languages"			
		]
		
	} else if (cluster_class=='final_destination') {
		var tablenameheader='Last Known Location'
		var linknames=false
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
				
				var thistablerow={
					"lg":markerprops.name,
					"value":markerprops.size
				}
				if (cluster_class=='origin') {
					thistablerow.key=markerprops.point_id-1000000
					thistablerow.tag='origin'
				}
				
				
				
				tablerowdata.push(thistablerow)
			}
		}
	})
	tablerowdata.sort((a,b)=>a.value-b.value);
	tablerowdata.reverse()

	var tablehtml=tablemaker(tablerowdata,5,tablenameheader,tableheaderrow,linknames)
	
	return tablehtml
}


function formatNodePopUpListItem(k,v) {
	var nodeclass_labels={
		'embarkation':'embarked',
		'disembarkation':'disembarked'
	};
	
	var count = v.count||0;
	var key = v.key||null;
	
	if (k=="post-disembarkation") {
	
		formattedstring=[count.toString(),pluralorsingular("Liberated African",count)].join(' ')
		
	} else {
		var label = nodeclass_labels[k];
		var formattedstring=[count.toString(),pluralorsingular("Liberated African",count),label].join(' ')
		
	}
	
	var text='<a href="#" onclick="linkfilter(' + key.toString() + ',\'' + k + '\'); return false;">' + formattedstring + '</a>'
	
	return text;
};


function makeNodePopUp(feature,nodesdict,edgesdict) {
// 	var popupsubheads=new Object;
	var node_classes=feature.properties.node_classes;
	var node_title=feature.properties.name;
	//a node can have multiple classes (mostly this is for sierra leone)
	
	var bad_aggregation_nodes=[]
	var tablehtml = new String;
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
			tablehtml=tablemaker(tablerowdata,5,"Language Group",tableheaderrow)
		}
		var total_enslaved_with_identified_languages=0
		tablerowdata.forEach(r=>{total_enslaved_with_identified_languages+=r.value})
	}
	

	
	var headerhtml=new String;
	
	if (node_classes['origin']) {
		var thisnode=node_classes['origin'];
		headerhtml='<a href="#" onclick="linkfilter('  + thisnode.key.toString()  + ',\'origin\'); return false;">'  + thisnode.count.toString()  + ' '  + pluralorsingular("Liberated African",thisnode.count)  +' with ' + node_title + ' origins.' + '</a>';
	} else {
		
		var headerhtmlslots=new Array;
	
		if (node_classes['embarkation']) {
			headerhtmlslots.push(formatNodePopUpListItem('embarkation',node_classes['embarkation']) + " in " + node_title + ", of whom " + total_enslaved_with_identified_languages.toString()+ " have an identified language group")
		}
		
		if (node_classes['disembarkation']) {
			var dis_string=formatNodePopUpListItem('embarkation',node_classes['disembarkation'])
			if (!node_classes['embarkation']) {
				dis_string+=" in " + node_title	
			} else {
				dis_string+=" here"
			}
			headerhtmlslots.push(dis_string)
		}
		
		if (node_classes['post-disembarkation']) {
			//if only post-disembark
			if (Object.keys(node_classes).length==1) {
				headerhtmlslots.push(node_title + " is the final known location for " + formatNodePopUpListItem('post-disembarkation',node_classes['post-disembarkation']))
			} else{
				headerhtmlslots.push("This is the final known location for " + formatNodePopUpListItem('post-disembarkation',node_classes['post-disembarkation']))
			}
		}
		
		if (headerhtmlslots.length==1) {
			headerhtml=headerhtmlslots[0]+'.'
		} else if (headerhtmlslots.length>1) {
			headerhtml=headerhtmlslots.join('. ')
		}
	
	}
	
	
	var popupelements=new Array;
	
	[headerhtml,tablehtml].forEach(element=>{
		if (element.length!=0) {
			popupelements.push(element)
		}
	})
	
	var popupcontent=popupelements.join('<hr/>')
	
	$(function () {
		$('[data-toggle="tooltip"]').tooltip()
	})
	
	return(popupcontent);
};