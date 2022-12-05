function pluralorsingular(singular,val) {
	
	var pluralize={
		'group':'groups',
		'person':'people'
	}
	
	if (val>1){
		return pluralize[singular]
	} else {
		return singular
	}
	
}

function make_languagegroupstable(markers) {
	
	var tablehtml="<table class='lgmaptable'><tr><td>Language Group</td><td>Number of people</td></tr>";
	
	//markerclusters contain lots of different kinds of "markers" -- to get at our geojson ones, we have to filter
	//there's likely a smarter way to do this
	
	var lg_ids = new Array;
	
	var tablerowdata=new Array;
	Object.keys(markers).forEach(marker_id=>{
		if (markers[marker_id])	{	
			if (markers[marker_id].feature){
				var markerprops=markers[marker_id].feature.properties;
				tablerowdata.push({
					"lg":markerprops.name,
					"value":markerprops.size
				})
				lg_ids.push(markerprops.point_id)
			}
		}
	})
	
	
	
	tablerowdata.sort((a,b)=>a.value-b.value);
	tablerowdata.reverse()
	
	displaylimit=5;
	//special handlers for Yoruba and Igbo (ffs)
	
	var dialects=[
		{'id':1160515,'name':'Yoruba'},
		{'id':1260677,'name':'Igbo'}
	];
	
	var cluster_dialects=new Array;
	
	var dialect_case=false;
	dialects.forEach(d=>{if(lg_ids.includes(d.id)){dialect_case=true;cluster_dialects.push(d);displaylimit-=1}});
	
	tablerowdata.slice(0,displaylimit).forEach(r=>{tablehtml+="<tr><td>"+r.lg+"</td><td>"+r.value.toString()+"</td></tr>"});
	if (displaylimit<tablerowdata.length) {
		if (dialect_case) {
			var excluded_other_count={'languages':0,'people':0};
			
			cluster_dialects.forEach(dialect=>{
			
				var excluded_dialect_count={'languages':0,'people':0};
			
				tablerowdata.slice(displaylimit,tablerowdata.length-1).forEach(r=>{
					if (r.lg.includes(dialect.name)) {
						excluded_dialect_count['languages']+=1
						excluded_dialect_count['people']+=r.value
					} else {
						excluded_other_count['languages']+=1
						excluded_other_count['people']+=r.value
					}
				})
			
				tablehtml += "<tr><td>"+excluded_dialect_count.languages.toString()+" more "+dialect.name+" dialects</td><td>"+excluded_dialect_count.people.toString()+"</td></tr>"	
			})
			
			if (excluded_other_count.languages>0) {
				tablehtml += "<tr><td>"+excluded_other_count.languages.toString()+" other language "+pluralorsingular('group',excluded_other_count.languages)+"</td><td>"+excluded_other_count.people.toString()+"</td></tr>"	
			}
			
		} else {
			var excluded_lg_count=tablerowdata.length-displaylimit;
			var excluded_people_count=0
			tablerowdata.slice(displaylimit,tablerowdata.length-1).forEach(r=>{excluded_people_count+=r.value})
			tablehtml += "<tr><td>"+excluded_lg_count.toString()+" other language groups</td><td>"+excluded_people_count.toString()+"</td></tr>"	
		}
	}
	
	tablehtml+="</table>"
	
	return tablehtml
	
}

function makeNodePopUp(node_classes,node_title) {
	var popupsubheads=[];
	//a node can have multiple classes (mostly this is for sierra leone)
	Object.entries(node_classes).forEach(([k,v]) => popupsubheads.push(formatNodePopUpListItem (k,v)));
	if (!popupsubheads.includes(false)){
		var popupcontent=popupsubheads.join(' and ') + " in " + node_title;
	} else {
		var count=node_classes['origin']['count'];
		var popupcontent=[count,personorpeople(count),"with",node_title,"origins."].join(" ")
	}
	return(popupcontent);
};