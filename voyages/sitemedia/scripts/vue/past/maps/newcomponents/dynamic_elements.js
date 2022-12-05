function make_languagegroupstable(markers) {
	
	var tablehtml="<table class='lgmaptable'><tr><td>Language Group</td><td>Number of people</td></tr>";
	
	//markerclusters contain lots of different kinds of "markers" -- to get at our geojson ones, we have to filter
	//there's likely a smarter way to do this
	
	var tablerowdata=new Array;
	Object.keys(markers).forEach(marker=>{
		if (markers[marker])	{	
			if (markers[marker].feature){
				tablerowdata.push({"lg":markers[marker].feature.properties.name,"value":markers[marker].feature.properties.size})
			}
		}
	})
	tablerowdata.sort((a,b)=>a.value-b.value);
	tablerowdata.reverse()
	
	displaylimit=5;
	
	tablerowdata.slice(0,displaylimit).forEach(r=>{tablehtml+="<tr><td>"+r.lg+"</td><td>"+r.value.toString()+"</td></tr>"});
	if (displaylimit<tablerowdata.length) {
		var excluded_lg_count=tablerowdata.length-displaylimit;
		var excluded_people_count=0
		tablerowdata.slice(displaylimit,tablerowdata.length-1).forEach(r=>{excluded_people_count+=r.value})
		tablehtml += "<tr><td>"+excluded_lg_count.toString()+" more language groups</td><td>"+excluded_people_count.toString()+"</td></tr>"	
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