function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


var map = L.map('map').setView([39.255485, -76.711392], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

function loadmap() {
    for (pin in curr_pins){
        // Create Marker
        const popupTxt =  '<h1 style="font-size:20px">' + curr_pins[pin].pin_name + '</h1>'
        marker = new L.Marker([curr_pins[pin].pin_data.pin_lat, curr_pins[pin].pin_data.pin_lng],).addTo(map).bindPopup(popupTxt);  
        // Create Post    
        const newPost = document.createElement('div');  
        newPost.classList.add('postDisp');
        const postText = '<h1 style="font-size:20px">'+curr_pins[pin].pin_name + '</h1>\n' +curr_pins[pin].pin_data.pin_desc +'\n';
        newPost.textContent = postText;
        document.getElementById('postsScroll').append(newPost);
        document.getElementById('postsScroll').append(document.createElement('br'));
    }
}
loadmap();


var lat;
var lng;
var newMarker = null;
var addOption = false;
var addOpen = false;

map.on('click', function(e){
        
        // add the new pin to the 
       if(newMarker == null && addOption){
        newMarker = new L.Marker([e.latlng.lat, e.latlng.lng], {draggable:'true',  autoPan: true}).addTo(map);
        var lat_entry = document.getElementById("latCoord");
        var lng_entry = document.getElementById("lngCoord");
        lat_entry.value = e.latlng.lat;
        lng_entry.value = e.latlng.lng;
        console.log(e);
        }
  });

  function addSelected(){

    if(addOpen == false){
        addOpen = true;
        addOption = true; // The add button has been selected.
        document.getElementById('postsScroll').className = "hide";
    }
    else{
        addOpen = addOption = false;
        document.getElementById('postsScroll').className = "scroll";
    }
  }

  function assignPoints(){
    var typeSelect = document.getElementById("pinType");
    var type = typeSelect.options[typeSelect.selectedIndex].value;
    var points = document.getElementById("pinPoints");
    if(type == 1){
        points.value = 6;
    }
    else { points.value = 4; }
    console.log(points.value);
}


// Clear the marker var so another can be added
function clearMarker(){
    newMarker = null;
}
