
let path = location.pathname;
let directories = path.split("/");
let tour_id = directories[(directories.length - 1)];
let online_or_offline = document.getElementById("live_text");
let last_location = document.getElementById("last_location");
let next_location = document.getElementById("next_location");
let bus_id = document.getElementById("bus_id").textContent;
const sheduled = document.getElementById("sheduled");
const sheduled_text = document.getElementById("sheduled-text");
const time_live = document.getElementById("live-time");
const bus_stop = document.getElementById("starting-point-name");
let data_f;
const hours_free = document.getElementById("hours-free");
const minutes_free = document.getElementById("minutes-free");

const url = "https://finnc.herokuapp.com/api/js/";

// GPS and Google Maps functionality removed - simplified for campus project

function dataToSend() {
    let data = {
        'bus_id': bus_id,
        "tour_id": tour_id,
    }
    return data;
}

// Display a simple message in the map area instead of Google Maps
const mapElement = document.getElementById("map");
if (mapElement) {
    mapElement.innerHTML = "<div style='padding: 20px; text-align: center; color: #666;'><p>Bus Location Tracking</p><p>Current Stop: <span id='current-stop-display'>-</span></p></div>";
}

setInterval(async function () {
    let data = dataToSend();
    let responce_data = await fetch(url, {
        method: 'POST', 
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': true,
        },
        body: JSON.stringify(data),
    });
    data_f = await responce_data.json();
    console.log(data_f['connected']);

    if (data_f['connected'] == "false") {
        online_or_offline.textContent = "Offline";
        document.getElementById('live').style.background = '#F70606';
    }
    else if (data_f['connected'] == "true")
    {
        online_or_offline.textContent = "Online";
        document.getElementById('live').style.background = '#52DE20'
    }
    if (data_f["last_location"] != "Not -Yet startted" && data_f["last_location"] != "Unknown") {
        last_location.textContent = data_f["last_location"];
    }
    if (data_f["next_location"] != "Not -Yet startted" && data_f["next_location"] != "Unknown") {
        next_location.textContent = data_f["next_location"];
    }
    if(data_f["started"] == "true")
    {
        sheduled.style.background = '#449CED';
        sheduled_text.textContent = "Started";
    }
    time_live.textContent = data_f["times_ago"];
    
    // Update current stop display (simplified - no GPS)
    const currentStopDisplay = document.getElementById('current-stop-display');
    if (currentStopDisplay && data_f["next_location"] && data_f["next_location"] != "Unknown") {
        currentStopDisplay.textContent = data_f["next_location"];
    }
    
    // Simplified - no distance calculations
    if(data_f["minutes_free"] != undefined && data_f["minutes_free"] != 0)
    {
        minutes_free.textContent = data_f["minutes_free"] + " minutes";
    } else {
        minutes_free.textContent = "N/A";
    }
    if(data_f["hours_free"] != undefined && data_f["hours_free"] != 0)
    {
         hours_free.textContent = data_f["hours_free"] + " hours";
    } else {
        hours_free.textContent = "N/A";
    }
    
}, 10000);
