import googlemaps
import pandas as pd
import os
import time
import requests
import json
import openpyxl

api_key = ''


#this one has the problem that shows only moroccan data
# with website
def collectPhoneNumbers(domain,city,fileName):
    # Set up the Google Maps API client
    gmaps = googlemaps.Client(api_key)
    # Set up the parameters for the search



    # Set up the path for the output file
    output_path = os.path.join(os.path.expanduser("~"), "Desktop", f"{fileName}.csv")

    # Check if the output file already exists
    if os.path.exists(output_path):
        # If it exists, load the existing data into a pandas DataFrame
        existing_data = pd.read_csv(output_path)
    else:
        # If it doesn't exist, create an empty DataFrame
        existing_data = pd.DataFrame(columns=["Phone Number", "Name", "Address", "City", "Website"])

    # Set up the initial query
    query_result = gmaps.places(query=domain, location=city)

    # Keep searching until we've collected 100 results
    while len(existing_data) < 100:
        # Append the new results to the existing DataFrame
        new_data = []
        for result in query_result["results"]:
            place_id = result["place_id"]
            place_details = gmaps.place(place_id,
                                        fields=["name", "formatted_address", "formatted_phone_number", "website"])
            phone_number = place_details["result"].get("formatted_phone_number", "")
            name = place_details["result"]["name"]
            address = place_details["result"]["formatted_address"]
            website = place_details["result"].get("website", "")
            new_data.append((phone_number, name, address, city, website))
        existing_data = pd.concat([existing_data, pd.DataFrame(new_data, columns=existing_data.columns)],
                                  ignore_index=True)

        # Check if there are more results to fetch
        if "next_page_token" in query_result:
            next_page_token = query_result["next_page_token"]
        else:
            break

        # Wait for a few seconds before fetching the next page of results
        time.sleep(2)

        # Fetch the next page of results
        query_result = gmaps.places(query=domain, location=city, page_token=next_page_token)

    # Save the updated DataFrame to a CSV file
    existing_data.to_csv(output_path, index=False)




collectPhoneNumbers("hotels","new york","nyc")
