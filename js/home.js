var cardWrapper = document.getElementById('cardWrapper');

data.forEach(function(object) {
    var cardDiv = document.createElement('div');
    cardDiv.className = "card";
    var table = document.createElement('table');
    table.innerHTML = '<tr><td class="thirtyPercentWidth">FC#</td><td>' + object.FC + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Grantor</td><td>' + object.GRANTOR + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Street</td><td>' + object.STREET + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Zip</td><td>' + object.ZIP + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Subdivision</td><td>' + object.SUBDIVISION + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Balance Due</td><td>' + object.BALANCEDUE + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Status</td><td>' + object.STATUS + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Assessor Market Value</td><td>' + object.ASSESSORVALUE + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Style Description</td><td>' + object.STYLEDESC + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Property Description</td><td>' + object.PROPDESC + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Year Built</td><td>' + object.YEARBUILT + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Dwelling Units</td><td>' + object.DWELLINGUNITS + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Total Rooms</td><td>' + object.TOTALROOMS + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Beds</td><td>' + object.BEDS + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Baths</td><td>' + object.BATHS + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Garage Description</td><td>' + object.GARAGEDESC + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Garage Area</td><td>' + object.GARAGEAREA + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Currently Scheduled Sale Date</td><td>' + object.SALEDATE + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Lenders Initial Bid</td><td>' + object.LENDERSINITIALBID + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Deficiency Amount</td><td>' + object.DEFICIENCYAMOUNT + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Total Indebtedness</td><td>' + object.TOTALINDEBTEDNESS + '</td></tr>' +
                '<tr><td class="thirtyPercentWidth">Links</td><td><a href=https://www.zillow.com/homes/'+object.STREET.replaceAll(' ','-')+'_rb target="_blank">Zillow</a></td></tr>';
    cardDiv.appendChild(table);
    var img = document.createElement('img');
    img.setAttribute('src', object.PHOTOPATH);
    cardDiv.appendChild(img);
    cardWrapper.appendChild(cardDiv);
});
