var map = L.map('map').setView([39.255485, -76.711392], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var lat;
var lng;
var newMarker;

map.on('click', function(e){
        
        // add the new pin to the 
        /*var popup = L.popup();
        popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
        var mp = new L.Marker([e.latlng.lat, e.latlng.lng]).addTo(map);
        */
        newMarker = new L.Marker([e.latlng.lat, e.latlng.lng]).addTo(map);
        lat = e.latlng.lat;
        lng = e.latlng.lng;
        console.log(e);

  });



// Get the button
//addPin = document.form1.Add_Pin;
function addPinToMap(){

    console.log("Trying to add pin to Database");

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

    console.log(pinID, name, typeStr, type, addr, date, desc, lat, lng);

    var msg = name + ", " + typeStr + " on " + date + "\n" + desc;
    newMarker.bindPopup(msg).openPopup();
    /*
    set(ref(db,'pins/'+ pinID),{
        pin_name: name.value,
        type: type,
        cleaned_up: typeStr,
        Date: date.value,
        Description: desc.value
    })
    .then(()=>{
        alert("Pin added to database");
    })
    .catch((error)=>{
        alert("Error adding Pin to database");
    });
    */

    // Add event to add data to database on sumbitt
    pinSubmit = document.getElementById("submitNewPin");

    // Call the python script to add the pin to the map.
    // addPinToMyMaps



    addMarker(pinID, name, typeStr, type, addr, date, desc);
    //alert("Finished adding pin to Database");
}

function editPinOnMap(){
    
}

function addMarker(pinID, name, typeStr, type, addr, date, desc){

    
}