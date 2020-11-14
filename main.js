    $(document).ready(function() {

		function loadData(){

    var url_string = window.location.href
    var url = new URL(url_string);
    var loc = url.searchParams.get("location");

        $.getJSON("https://gbfs.divvybikes.com/gbfs/en/station_status.json", function(json) {
              $( ".divvy-station" ).each(function( ) {
                $(this).html('<div class="divvy-status">No Data</div>');
              });

              stations = json.data.stations;

              for(i=0; i < stations.length; i++) {
                a = stations[i];
                stationd = $('#divvy-station-' + a.station_id);
                stationd.empty();
                stationd.html('<div class="divvy-status"><div class="divvy-header">Classic Bikes</div><div class="divvy-data">' + (a.num_bikes_available - a.num_ebikes_available) + '</div></div><div class="divvy-status"><div class="divvy-header">E-Bikes</div><div class="divvy-data">' + a.num_ebikes_available + '</div></div><div class="divvy-status"><div class="divvy-header">Empty Docks</div><div class="divvy-data">' + a.num_docks_available + "</div></div>");
              }
        });

        $.getJSON("/arrivals.py", function(json) {

              $( ".stop" ).each(function( ) {
                $(this).html('<div class="arrival">No Departures</div>');
              });

              for(i=0; i < json.length; i++) {
                a = json[i];
                //if a.stop == '8062400' { a.stop = '10567';} //same stop
                if (a.stop == '8173082' || a.stop == '8058068') {a.stop = '8062460';} //same stop 57+SI
                //if (a.stop == '8062060') {a.stop = '8062400';} //same stop 55+LP
                if (a.stop == '8062060' && window.location.pathname != '/moomers') {a.stop = '8062516';} //same stop 55+LP
                //if (a.stop == '8062516' && window.location.pathname != '/moomers') {a.stop = '7179';} //same stop 55+LP

                stopd = $('#stop-' + a.stop);
                if(stopd.html() == '<div class="arrival">No Departures</div>') {
                  stopd.empty();
                }

                if ((a.stop == '1518' && a.route == '171') || (a.stop == '1654' && a.route == '55')) { continue; } // remove buses near end of line that people are unlikely to want to board
                if (a.mins == "0") { a.mins = "now"; }
                else if (a.mins == "-1") {a.mins = "?? min";}
                else { a.mins = a.mins + " min";}
                stopd.append('<div class="arrival '+ a.agency +'">' + 
                '<div class="route ' + (a.route.length > 4 ? 'rlong' : '') + '">' + a.route + '</div>' +
                '<div class="dest ' + (a.dest.length > 20 ? 'long' : '') + '">' + a.dest + '</div>' + 
                '<div class="time">' + a.mins + '</div>'+
                '<div class="clear">&nbsp;</div>' + 
                '</div>');
              }
        });
   }

   loadData(); // This will run on page load
   setInterval(function(){
     loadData() // this will run after every 30 seconds
   }, 30000);

   function loadClock() {
     var today = new Date();
     var h = today.getHours();
     var m = today.getMinutes();
     var s = today.getSeconds();
     if (h == 0) {hs = "12"; as = "a.m.";}
     if (h > 0 && h < 12) {hs = h; as = "a.m.";}
     if (h == 12) {as = "p.m.";}
     if (h > 12) {hs = h - 12; as = "p.m.";}
     m = (m < 10 ? "0" + m : m)
     s = (s < 10 ? "0" + s : s)
     $('#clock').html(hs + ":" + m + " " + as);
     //$('#clock').html(hs + ":" + m + ":" + s + " " + as);
   }

   loadClock(); // This will run on page load
   setInterval(function(){
     loadClock() // this will run every N seconds
   }, 1000);

}); 
