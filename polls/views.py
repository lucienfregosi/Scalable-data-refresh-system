from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.core.urlresolvers import reverse
import requests
import sys
import json

from .forms import NameForm

def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # Program is starting after form submitting
            # Get the input parameters
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            accuracy = form.cleaned_data['accuracy']

            # Return Variable
            finalResearchResult = ""

            # Construct the key wich will used later
            resarchKey = str(latitude) + "|" + str(longitude) + "|" + str(accuracy)


            # We need to determine if the request is send for the firt time or not
            # If it's not the firt time, we are going to get the search result in the cache
            # Data are stored in the followed format : {<latitude>|<longitude>|<accuracy>,<result in json format}

            if cache.get(resarchKey) is not None:
                print("Not the research first time")
                # Get to the result wich be returned
                finalResearchResult = cache.get(resarchKey)

            else:
                print("New research")
                # New reseach so the result is not in the cache. Starting foursquare requesting et get a result

                # Initialize the constant to request Foursquare API
                clientId = "0G0PZPQFBYMJ0EQYSWE4YOUU5ZAJMQSLXONNHR2E5CYHJP3M"
                clientSecret = "YBCATWHKEWJBF3NKLZOS3JRNCFFL3QFF20VKIDM4BW2F4GGH"
                apiDateVersion = "20161214"

                # Build the URL
                foursquareRequestUrl = "https://api.foursquare.com/v2/venues/search?ll=" + str(latitude) + "," + str(longitude) + "&client_id=" + str(clientId) + "&client_secret=" + clientSecret + "&v=" + apiDateVersion

                #print(foursquareRequestUrl);

                # Get the response in JSON format
                response = requests.get(foursquareRequestUrl)
                apiJsonResponse = response.json()

                #print(apiJsonResponse)

                # Test the query is well executed
                try:
                    apiJsonResponse["response"]["venues"]
                except:
                    print("Foursquare API query error")
                    # Set a no result research in the cache
                    cache.set(resarchKey,json.dumps("No result"), 2592000)
                    finalResearchResult = "No result"

                else:
                    # 4. Test if the number of result is > 0
                    if len(apiJsonResponse["response"]["venues"]) != 0:
                        print("Setting result in the cache")
                        # Setting the result in the cache with the research key composed by
                        cache.set(resarchKey,json.dumps(apiJsonResponse["response"]["venues"]), 2592000)

                        finalResearchResult = json.dumps(apiJsonResponse["response"]["venues"])
                    else:
                        # Cas d'erreur à traiter
                        print("0 results, change the input parameters")
                        cache.set(resarchKey,json.dumps("No result"), 2592000)
                        finalResearchResult = "No result"

            # End of the treatment, we have to return the json result in a web page
            # Going to redirect with the result of the research (in cache or foursquare) for parameter
            return render(request, 'success.html', {'result': finalResearchResult})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'request.html', {'form': form})
