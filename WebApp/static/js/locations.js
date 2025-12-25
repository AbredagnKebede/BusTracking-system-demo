let startingpointdatalist = document.getElementById('startingpointdatalist')
let startingpoint = document.getElementById('startingpoint')
let destinationpointdatalist = document.getElementById('destinationpointdatalist')
let destinationpoint = document.getElementById('destinationpoint')

// GPS functionality removed - users must select from predefined bus stops
document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('startingpoint').disabled = false;
    document.getElementById('destinationpoint').disabled = false;
})

document.getElementById('destinationpoint').addEventListener("change", startigpoint(this.value));

function startigpoint(val)
{
    document.getElementById('destinationpoint').disabled = false;
    console.log(val)
 
}


startingpoint.onfocus = function () {
    startingpointdatalist.style.display = 'block';
    startingpoint.style.borderRadius = "2vw";  
  };
  for (let option of startingpointdatalist.options) {
    option.onclick = function () {
      startingpoint.value = option.value;
      startingpointdatalist.style.display = 'none';
      startingpoint.style.borderRadius = "2vw";
    }
  };
  
  startingpoint.oninput = function() {
    currentFocus = -1;
    var text = startingpoint.value.toUpperCase();
    for (let option of startingpointdatalist.options) {
      if(option.value.toUpperCase().indexOf(text) > -1){
        option.style.display = "block";
    }else{
      option.style.display = "none";
      }
    };
  }
  var currentFocus = -1;
  startingpoint.onkeydown = function(e) {
    if(e.keyCode == 40){
      currentFocus++
     addActive(startingpointdatalist.options);
    }
    else if(e.keyCode == 38){
      currentFocus--
     addActive(startingpointdatalist.options);
    }
    else if(e.keyCode == 13){
      e.preventDefault();
          if (currentFocus > -1) {
            /*and simulate a click on the "active" item:*/
            if (startingpointdatalist.options) startingpointdatalist.options[currentFocus].click();
          }
    }
  }
  
  function addActive(x) {
      if (!x) return false;
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      x[currentFocus].classList.add("active");
    }
    function removeActive(x) {
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("active");
      }
    }

    // -------------------------------------
    destinationpoint.onfocus = function () {
      destinationpointdatalist.style.display = 'block';
      destinationpoint.style.borderRadius = "2vw";  
    };
    for (let option of destinationpointdatalist.options) {
      option.onclick = function () {
        destinationpoint.value = option.value;
        destinationpointdatalist.style.display = 'none';
        destinationpoint.style.borderRadius = "2vw";
      }
    };
    
    destinationpoint.oninput = function() {
      currentFocus = -1;
      var text = destinationpoint.value.toUpperCase();
      for (let option of destinationpointdatalist.options) {
        if(option.value.toUpperCase().indexOf(text) > -1){
          option.style.display = "block";
      }else{
        option.style.display = "none";
        }
      };
    }
    var currentFocus = -1;
    destinationpoint.onkeydown = function(e) {
      if(e.keyCode == 40){
        currentFocus++
       addActive(destinationpointdatalist.options);
      }
      else if(e.keyCode == 38){
        currentFocus--
       addActive(destinationpointdatalist.options);
      }
      else if(e.keyCode == 13){
        e.preventDefault();
            if (currentFocus > -1) {
              /*and simulate a click on the "active" item:*/
              if (destinationpointdatalist.options) destinationpointdatalist.options[currentFocus].click();
            }
      }
    }
    
    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("active");
      }
      function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
          x[i].classList.remove("active");
        }
      }