from flask import Flask, request, render_template
from backend import *

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["APPLICATION_ROOT"] = "/"

@app.route('/', methods=["GET", "POST"])
async def main():
    if request.method == "POST":
        # The code here determines what happens after submitting the "form", in our case, the filters
        # Get supply chain data
        supplyChain = get_supply_chain()
        events = get_events()

        # # Initialize variables
        id_counter = 0
        lat = 0
        long = 0
        markers = ''
        for index, row in events.iterrows():
            # Create unique ID for each marker
            idd = 'event' + str(id_counter)
            id_counter += 1
            lat += row['location_lat']
            long += row['location_long']
            # Create the marker and its pop-up for each event
            markers += "var {idd} = L.marker([{latitude}, {longitude}]);\
                        {idd}.addTo(map).bindPopup('Event Name: {name}<br>Event Scale: {scale}');".format(idd=idd, latitude=row['location_lat'],\
                                                                                     longitude=row['location_long'], \
                                                                                         name = row['name'], \
                                                                                             scale = row['scale'])
        
        # # Render the page with the map
        return render_template('supplyMap.html', markers=markers, lat=lat/id_counter, lon=long/id_counter)
        # 
    else:
        # Render the input form
        return render_template('welcome.html')