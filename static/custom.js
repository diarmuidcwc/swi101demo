//Get the link status via a JSON request
function loadLinkStatus(ipaddress,index){
	// get JSON-formatted data from the server
	$.getJSON( "/linkstatus/"+ipaddress, function( resp ) {
		// create a new list
		var modifiedList = [];
		var link_stat_to_class = {0: "disconnected",100:"hundredmeg",1000:"gigabit"}
		
		$.each( resp, function( key, value ) {
			if (key == "swidown") {
				modifiedList.push("<li class=\"" + link_stat_to_class[0] + "\"><a>Switch Down</a></li>");
			} else{
				modifiedList.push("<li class=\"" + link_stat_to_class[value] + "\"><a>Port "+key+"</a></li>");
			}
			});
		$( "ul#LinkStatus"+index ).html(modifiedList);
	});
	setTimeout( function() { loadLinkStatus(ipaddress,index);},2000)
}

// Switch between the two camera streams.
// Call a get function and toggle the bitton
function selectcamera(cameratype) {
	$.get("/selectcamera/"+cameratype , function (resp) {
		var linkhtml = "";
		switch ( resp ) {
			case "outdoor":
			case "indoor":
				$( "div#indoor" ).toggle();
				$( "div#outdoor" ).toggle();
				break;
			case "default":
				console.log(resp);
			
		}
	});
}
// Get the PTP Time Mode
function gettimemode(ipaddress,index) {
	$.getJSON( "/timeinfo/"+ipaddress, function( resp ) {
		// create a new list
		var tablerows = [];
		$.each( resp, function( key, value ) {
			tablerows.push("<tr> <td>"+key+"</td>  <td>"+value+"</td></tr>");
			});
		$( "tbody#timetable"+index ).html(tablerows);
	});
	setTimeout( function() { gettimemode(ipaddress,index);},2000)
}

function getbcutime(ipaddress,index) {
	$.getJSON( "/bcutimeinfo/"+ipaddress, function( resp ) {
		// create a new list
		var tablerows = [];
		$.each( resp, function( key, value ) {
			tablerows.push("<tr> <td>"+key+"</td>  <td>"+value+"</td></tr>");
			});
		$( "tbody#bcutable"+index ).html(tablerows);
	});
	setTimeout( function() { getbcutime(ipaddress,index);},1000)
}

// Get the PTP Time Mode
function gettrafficgenerators() {
	$.getJSON( "/trafficrate", function( resp ) {
		// create a new list
		var sliders = [];
		$.each( resp, function( key, value ) {
			sliders.push("<div #slider"+key+"><div>");
			});
		$( "div#trafficsliders" ).html(sliders);
	});
}

function settrafficrate(rate) {
	$.get("/trafficrate/1/"+rate , function (resp) {
		console.log(resp);	
	});	
}

function getrouting(ipaddress,port,index) {
	$.getJSON( "/routing/"+ipaddress+"/"+port, function( resp ) {
		// create a new list
		var tablerow = ["<th>P"+port+"</th>"];
		console.log(resp)
		$.each( resp, function( key, value ) {
			if ( value == true ) {
				linkclass = "connected";
			} else {
				linkclass = "disconnected";
			}
			tablerow.push("<td><button class=\""+linkclass+"\" OnClick=\"toggleport('"+ipaddress+"',"+port+","+key+","+index+")\"></button></td>");
			});
		$( "tr#routing"+index+"port"+port ).html(tablerow);
	});
	setTimeout( function() { getrouting(ipaddress,port,index);},10000)
}

function getfullrouting(ipaddress,index) {
	for (i = 1; i < 9; i++) {
		getrouting(ipaddress,i,index);
	}
}

function resetrouting(){
	$.get("/resetrouting" , function (resp) {
		console.log(resp);	
	});	
	
}

function toggleport(ipaddress,srcport,dstport,index) {
	$.getJSON( "/toggleport/"+ipaddress+"/"+srcport+"/"+dstport, function( resp ) {
		// create a new list
		var tablerow = ["<th>P"+srcport+"</th>"];
		console.log(resp)
		$.each( resp, function( key, value ) {
			if ( value == true ) {
				linkclass = "connected";
			} else {
				linkclass = "disconnected";
			}
			tablerow.push("<td><button class=\""+linkclass+"\" OnClick=\"toggleport('"+ipaddress+"',"+srcport+","+key+","+index+")\"></button></td>");
			});
		$( "tr#routing"+index+"port"+srcport ).html(tablerow);
	});
}


$(function() {
    $(".dial").knob( {
		'release' : function (v) {
			settrafficrate(v);
		}
	});
});
  
  