$(document).ready(function() {

    const input = document.getElementById("address");
    const autocomplete = new google.maps.places.Autocomplete(input);

    var url_string = window.location.href
    var url = new URL(url_string);
    var address = url.searchParams.get("address");
    var num_stations = url.searchParams.get("num_stations");
    var num_bikes = url.searchParams.get("num_bikes");
    var facing_direction = url.searchParams.get("facing_direction");
    var refresh_freq = url.searchParams.get("refresh_freq");

		function loadData(){
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

        //$.getJSON("divvy.py", function(json) {
          $.getJSON("/divvy.py?address=" + address + '&num_stations=' + num_stations + '&num_bikes=' + num_bikes, function(json) {

                bikes = json

                div = $("#divvy-undocked-bikes")
                div.empty()
                div.html("<table>");
                div.append('<tr><th>Minutes</th><th>Meters</th><th>Blocks</th><th>Approx Address</th></tr>');

                for(i=0; i < bikes.length; i++) {
                  bike = bikes[i];
                  partial_address = bike.address.split(",")[0];
                  div.append('<tr><td>' + parseInt(bike['seconds']/60) + '</td><td>' + parseInt(bike['meters']) + '</td><td>' + bike['distance_blocks'] + '</td><td>' + partial_address + '</td></tr>');
                }
                div.append('</table>');
          });
   }

   loadData(); // This will run on page load
   setInterval(function(){
     loadData() // this will run after every N minutes
   }, refresh_freq * 60000);

   function loadClock() {
     var today = new Date();
     var h = today.getHours();
     var m = today.getMinutes();
     var s = today.getSeconds();
     if (h == 0) {hs = "12"; as = "a.m.";}
     if (h > 0 && h < 12) {hs = h; as = "a.m.";}
     if (h == 12) {hs = "12"; as = "p.m.";}
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
