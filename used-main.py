import requests
import json
import openpyxl
import time


api_key = ''

def collectPhoneNumbers1(domain,city,fileName):
    endpoint_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

    # Set the search parameters
    query = f"{domain} in {city}"
    fields = 'formatted_address,name'

    # Send the first request to the Google Places API
    params = {
        'query': query,
        'fields': fields,
        'key': api_key
    }
    response = requests.get(endpoint_url, params)
    results = json.loads(response.text)['results']

    # Keep making requests until we have at least 100 results
    while len(results) < 100:
        # Check if there are more results to retrieve
        next_page_token = json.loads(response.text).get('next_page_token')
        if next_page_token is None:
            break

        # Wait for a few seconds to give the server time to generate the next page token
        time.sleep(2)

        # Send the next request to the Google Places API with the page token
        params['pagetoken'] = next_page_token
        response = requests.get(endpoint_url, params)
        results += json.loads(response.text)['results']

    # Create a new Excel workbook and sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["Phone Number", "Name", "Address", "City"])

    # Loop through the results and add them to the Excel sheet
    for result in results:
        name = result.get('name', '')
        address = result.get('formatted_address', '')
        city = result.get('formatted_address', '').split(',')[-1].strip()
        place_id = result.get('place_id', '')

        # Send a request to the Details endpoint to get the phone number
        details_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number&key={api_key}'
        details_response = requests.get(details_url)
        details_result = json.loads(details_response.text)['result']
        number = details_result.get('formatted_phone_number', '')

        sheet.append([number, name, address, city])

    # Save the Excel file to the desktop
    #desktop path : C:\Users\One-x-shield\Desktop\test.xlsx
    workbook.save(fr"C:\Users\One-x-shield\Desktop\{fileName}.xlsx")

collectPhoneNumbers1("casino","newyork","LA")
