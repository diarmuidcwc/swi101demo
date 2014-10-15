%#template for the root swit status
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <script type="text/javascript" src="static/jquery-1.11.1.min.js" charset="utf-8"></script>
        <script type="text/javascript" src="static/jquery.knob.min.js" charset="utf-8"></script>
		<link rel="stylesheet" href="static/pure-release-0.5.0/pure-min.css">
		<link rel="stylesheet" href="static/pure-skin-cwc.css">
		<link rel="stylesheet" href="static/custom.css">
		<script type="text/javascript" src="static/custom.js" charset="utf-8"></script>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>NET/SWI/101</title>
    </head>
	
	
    <body onload="start();">
	
		<div id="content" class="pure-skin-cwc">
			<h1 class="header">NET/SWI/101 Status</h1>
			
			<!-- First "row" in the page is the port status -->
			<div class="pure-menu pure-menu-open pure-menu-horizontal" >
				<h2 class="pure-menu-heading">PTP v2 Boundary 192.168.28.101</h2>
				<ul class="" id="LinkStatus1">
				</ul>
			</div>
			
			<!-- Second row contains the timesetup of the swi -->
			<div class="pure-menu pure-menu-open pure-menu-horizontal" >
				<h2 class="pure-menu-heading">PTP  v2->v1  Bridge    192.168.28.102</h2>
				<ul class="" id="LinkStatus2">
				</ul>
			</div>
			
			
			<!-- Third row contains the Camera control and the traffic generator -->
			<div class="pure-g">
				<div class ="pure-u-1-2" id=cameracontrol>
					<h2> Camera Control</h2>
					<div id="indoor">
						<button id="button" class="camera pure-button  pure-button-primary"  OnClick="selectcamera('indoor')">Show Indoor Camera</button>
					</div>
					<div id="outdoor">
						<button id="button" class="camera pure-button pure-button-primary" OnClick="selectcamera('outdoor')">Show Outdoor Camera</button>
					</div>
				</div>
				
				<div class="pure-u-1-2" id="trafficsliders">
					<h2>Traffic Generator Data Rate (Mbps)</h2>
					<input type="text" value="28" class="dial" data-min="5" data-max="1000" data-fgColor="#66CC66" data-angleOffset=-125 data-angleArc=250>
				</div>

			</div>	
			
			<!-- Fourth row contains the BCU details -->
			<div class="pure-g">
				<div class ="pure-u-1-2" id="bcu1">
					<h2>KAD/BCU/142</h2>
					<h3>192.168.28.1</h3>
					<table class="pure-table pure-table-bordered" id="bcutable1">
						<thead>
							<tr>
							<th>Time Detail</th>
							<th>Setting</th>
							</tr>
						</thead>
						<tbody id="bcutable1">
						<!-- This will be filled out bu the gettimemode javascript function -->
						</tbody>
					</table>
				</div>
				<div class ="pure-u-1-2" id="bcu2">
					<h2>KAD/BCU/145</h2>
					<h3>192.168.28.21</h3>
					<table class="pure-table pure-table-bordered" id="bcutable2">
						<thead>
							<tr>
							<th>Time Detail</th>
							<th>Setting</th>
							</tr>
						</thead>
						<tbody id="bcutable2">
						<!-- This will be filled out bu the gettimemode javascript function -->
						</tbody>
					</table>
				</div>
			</div>
			<p></p>			
			<!-- Fifth row contains the routing grid -->
			<div class="pure-g">
				<div class ="pure-u-1-2" id="routing1">
					<h2>Routing Control SWI#1</h2>
					<table class="pure-table pure-table-bordered" id="routingtable1">
						<thead>
							<tr>
							<th></th>
							<th>P1</th>
							<th>P2</th>
							<th>P3</th>
							<th>P4</th>
							<th>P5</th>
							<th>P6</th>
							<th>P7</th>
							<th>P8</th>
							</tr>
							<tr id="routing1port1" class="disconnected"></tr>
							<tr id="routing1port2" class="disconnected"></tr>
							<tr id="routing1port3" class="disconnected"></tr>
							<tr id="routing1port4" class="disconnected"></tr>
							<tr id="routing1port5" class="disconnected"></tr>
							<tr id="routing1port6" class="disconnected"></tr>
							<tr id="routing1port7" class="disconnected"></tr>
							<tr id="routing1port8" class="disconnected"></tr>
						</thead>
						<tbody id="routingtable1">
						<!-- This will be filled out bu the gettimemode javascript function -->
						</tbody>
					</table>
				</div>
				<div class ="pure-u-1-2" id="routing2">
					<h2>Routing Control SWI#2</h2>
					<table class="pure-table pure-table-bordered" id="routingtable2">
						<thead>
							<tr>
							<th></th>
							<th>P1</th>
							<th>P2</th>
							<th>P3</th>
							<th>P4</th>
							<th>P5</th>
							<th>P6</th>
							<th>P7</th>
							<th>P8</th>
							</tr>
							<tr id="routing2port1" class="disconnected"></tr>
							<tr id="routing2port2" class="disconnected"></tr>
							<tr id="routing2port3" class="disconnected"></tr>
							<tr id="routing2port4" class="disconnected"></tr>
							<tr id="routing2port5" class="disconnected"></tr>
							<tr id="routing2port6" class="disconnected"></tr>
							<tr id="routing2port7" class="disconnected"></tr>
							<tr id="routing2port8" class="disconnected"></tr>
						</thead>
						<tbody id="routingtable2">
						<!-- This will be filled out bu the gettimemode javascript function -->
						</tbody>
					</table>
				</div>
			</div>
			<p>
			<a href="/" onclick="resetrouting()">Reset Routing to Defaults</a>
			</p>
		</div>
		
    </body>
	
	<script>
	function start() {
		loadLinkStatus("192.168.28.101",1);
		loadLinkStatus("192.168.28.102",2);
		getfullrouting("192.168.28.101",1);
		getfullrouting("192.168.28.102",2);
		$( "div#outdoor" ).hide();
		getbcutime("192.168.28.1",1)
		getbcutime("192.168.28.21",2)
	}
	

	</script>
	
</html>

