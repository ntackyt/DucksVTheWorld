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
    }
    else{
        addOpen = addOption = false;
    }
  }

  function editSelect(){

  }


// Get the button
//addPin = document.form1.Add_Pin;
function clearMarker(){

    // Clear out the marker
    newMarker = null;

    console.log("Trying to add pin to Database");
    /*
    // Input the pin data into the database
    //const db = getDatabase();

    // Get References to add to the database
    var dateCurr = new Date();
    var pinID = dateCurr.getSeconds();
    var name = document.getElementById("pinName").value;
    var typeSelect = document.getElementById("pinType");
    var type = typeSelect.options[typeSelect.selectedIndex].value;
    var typeStr = typeSelect.options[typeSelect.selectedIndex].text;
    var addr = document.getElementById("pinAddress").value;
    var date = document.getElementById("pinDate").value;
    var desc = document.getElementById("pinDesc").value;
    var lat_entry = document.getElementById("latCoord");
    var lng_entry = document.getElementById("lngCoord");
    
    console.log(pinID, name, typeStr, type, addr, date, desc, lat_entry.value, lng_entry.value);

    

    var msg = name + ", " + typeStr + " on " + date + "\n" + desc;
    newMarker.bindPopup(msg).openPopup();

    // Send the pin to the server.
    // For CSRF protection
   const csrftoken = getCookie('csrftoken');
    // POST data to Django server using AJAX
    $.ajax({
        type: "POST",
        url: "/map/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            "pin_name": name,
            "pin_type_str": typeStr,
            "pin_type_bool": type,
            "pin_addr": addr,
            "pin_date": date,
            "pin_desc": desc,
            "pin_lat": lat,
            "pin_lng": lon
        },
        success: function (response) {
            if (response.success == true) {
                alert("data successfully posted")
            } else {
                alert("data not successfully posted")
            }
        },
        error: function (error) {
            console.log("Error: ", error);
        }
    });
    */
    //alert("Finished adding pin to Database");
}

//function editPinOnMap(){   }