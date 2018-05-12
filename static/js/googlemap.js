/**
 * Created by amanda on 3/3/2018.
 */

// Initialize google maps
function myMap() {
  var myCenter = new google.maps.LatLng(6.7881,79.8913);
  var mapCanvas = document.getElementById("map");
  var mapOptions = {center: myCenter, zoom: 12};
  var map = new google.maps.Map(mapCanvas, mapOptions);
  var marker = new google.maps.Marker({position:myCenter});
  marker.setMap(map);
}
