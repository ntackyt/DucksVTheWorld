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

types = ["Cleaned Up", "Needs Work"]

function loadMap() {
    for (pin in curr_pins){
        // Create Marker
        const popupTxt =  '<h1 style="font-size:20px">' + curr_pins[pin].pin_name + '</h1>'
        marker = new L.Marker([curr_pins[pin].pin_data.pin_lat, curr_pins[pin].pin_data.pin_lng],).addTo(map).bindPopup(popupTxt);  
        
        // Create Post    
        const newPost = document.createElement('div');  
        newPost.classList.add('postDisp');
        newPost.id=pin
        newPost.setAttribute("post_lat", curr_pins[pin].pin_data.pin_lat)
        newPost.setAttribute("post_lng", curr_pins[pin].pin_data.pin_lng)
        var index = parseInt(curr_pins[pin].pin_data.pin_type_bool)
        let pin_type = types[index - 1]
        let postText = `<h1 style="font-size:20px"> ${pin_type}: ${curr_pins[pin].pin_name}</h1>
                        <img src="${curr_pins[pin].user_prof_pic}"><a href="/show_user_profile/${curr_pins[pin].pin_user_id}">${curr_pins[pin].user_first_name} ${curr_pins[pin].user_last_name}</a><br>
                        ${curr_pins[pin].pin_data.pin_date}  @ ${curr_pins[pin].pin_data.pin_addr} <br> 
                        ${curr_pins[pin].pin_data.pin_desc} <br> 
                        <button type="button" onclick="gotoPin(${pin})">See on map</button>`; // Make the button Id the same as the div id to get the attributes - could set buttons attributes?
        newPost.innerHTML = postText;
        document.getElementById('postsScroll').prepend(document.createElement('br'));
        document.getElementById('postsScroll').prepend(newPost);
        
    }
}
loadMap();

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
        points.value = 600;
    }
    else { points.value = 400; }
    console.log(points.value);
}


// Clear the marker var so another can be added
function clearMarker(){
    newMarker = null;
}


function gotoPin(e){
    postDeets = document.getElementById(e).attributes
    map.flyTo(new L.LatLng(postDeets[2].value, postDeets[3].value));
}