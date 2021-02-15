
function checkAdress(){
    let zipcode = document.getElementById("zipcode").value;
    fetch('/api/address_lookup', {
      method: 'POST',
      headers: {
                'Content-Type': 'application/json',
                },
      body: JSON.stringify({ 'postcode': zipcode}),
    })
    .then(response => response.json())
    .then(data => {
      createAdresslist(data, zipcode);
    })
    .catch((error) => {
      console.error('Error:', error);
    });

}

function createAdresslist(addresses, zipcode) {
    let bigdiv = document.getElementById("booking-form");
    let newdiv = document.createElement("div");
    newdiv.setAttribute("id", "address-select");
    let postcodeElement = document.getElementById("select-postcode")
    bigdiv.replaceChild(newdiv,postcodeElement);
    newdiv.innerHTML = `<div class="form-group">
                            <h1 style="text-align: center"> Select your Address </h1>
                            <select class="form-control" id="address-list">
                            <option>Select Address</option>
                            </select>
                            <button class="btn btn-primary" type="button" style="margin-top: 10px;" onclick="generateDates(${zipcode})">See Available Dates</button>
                         </div>`
    bigdiv.appendChild(newdiv);
    let selectform = document.getElementById("address-list");
    for (let address in addresses){
        let newoption = document.createElement("option");
        newoption.innerText = addresses[address];
        selectform.appendChild(newoption);
    }
}
function generateDates(zipcode){
    let array = [];
    let addressSelect = document.getElementById("address-list");
    let address = addressSelect.options[addressSelect.selectedIndex].value;
    let date = new Date();

    fetch('/api/next_available', {
      method: 'POST',
      headers: {
                'Content-Type': 'application/json',
                },
      body: JSON.stringify({ 'postcode': zipcode , 'address': address , 'date' : date.toISOString().split('T')[0]}),
    })
    .then(response => response.json())
    .then(data => {
        for (let i in data['slots']){
            array.push(data['slots'][i].split('T')[0]);
        }
        $(function datepicker() {
            $('#datepicker').datepicker({
            minDate : "+1d",
            dateFormat: "yy-mm-dd",
            onSelect: function(date) {
                    generateHours(date, zipcode, address);
                },
            beforeShowDay: function(date){
                            var string = jQuery.datepicker.formatDate('yy-mm-dd', date);
                            return [ array.indexOf(string) !==  -1 ]
                            }
            });
        });
    })
    .catch((error) => {
      console.error('Error:', error);
    });
    let bigdiv = document.getElementById("booking-form");
    let selectAddress = document.getElementById("address-select");
    let calendar = document.createElement("div");
    calendar.setAttribute("id","select-date");
    calendar.innerHTML = `<h1 style="text-align:center">Please choose an installation date</h1>
                            <div id="datepicker-center">
                                <div id="datepicker"></div>
                           </div>`
    bigdiv.replaceChild(calendar,selectAddress);

}

function generateHours(date, postcode, address){
    let calendar = document.getElementById("datepicker");
    let existinghours = document.getElementById("hour-list");
    let hourlist = document.createElement("div");
    hourlist.setAttribute("id", "hour-list");
    hourlist.innerHTML = `<div class="form-group">
                            <h1 style="text-align: center"> Select an Hour </h1>
                            <select class="form-control" id="hours-list">
                            <option>Select Hour</option>
                            </select>
                            <button class="btn btn-primary" style="margin-top: 10px;" type="button" onclick="">Select Hour</button>
                         </div>`
    if (calendar.lastElementChild === existinghours){
        calendar.replaceChild(hourlist,existinghours);
    }
    calendar.appendChild(hourlist);
    let hourselect = document.getElementById("hours-list");
    fetch('/api/list_slots', {
      method: 'POST',
      headers: {
                'Content-Type': 'application/json',
                },
      body: JSON.stringify({ 'postcode': postcode, 'address': address, 'date': date}),
    })
    .then(response => response.json())
    .then(data => {
        for (let i in data['hours']){
            let newhour = document.createElement("option");
            newhour.innerText = data['hours'][i].split('T')[1];
            hourselect.appendChild(newhour);
        }
    })
    .catch((error) => {
      console.error('Error:', error);
    });


}

