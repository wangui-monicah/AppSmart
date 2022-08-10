import requests
import json
import bs4
from bs4 import BeautifulSoup

url_list = ['https://tinyurl.com/4wtuzewn', 'https://tinyurl.com/5n62rvue', 'https://tinyurl.com/s6vzafdu','https://tinyurl.com/ant8teu2','https://tinyurl.com/4f8akvw9']

headers = {
    'User-Agent' : 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

def airtable_upload(table, upload_data, typecast = False, api_key = None, base_id = None, record_id = None):
    """Sends dictionary data to Airtable to add or update a record in a given table. 
        Returns new or updated record in dictionary format.
    
    Keyword arguments:
    • table: set to table name
        ◦ see: https://support.airtable.com/hc/en-us/articles/360021333094#table
    • upload_data: a dictionary of fields and corresponding values to upload in format {field : value}
        ◦ example: {"Fruit" : "Apple", "Quantity" : 20}
    • typecast: if set to true, Airtable will attempt "best-effort automatic data conversion from string values"
        • see: "Create Records" or "Update Records" in API Documentation, available at https://airtable.com/api for specific base
    • api_key: retrievable at https://airtable.com/account
        ◦ looks like "key●●●●●●●●●●●●●●"
    • base_id: retrievable at https://airtable.com/api for specific base
        ◦ looks like "app●●●●●●●●●●●●●●"
    • record_id: when included function will update specified record will be rather than creating a new record
        ◦ looks like "rec●●●●●●●●●●●●●●"
        """
    
    # Authorization Credentials
    if api_key == None:
        print("Enter Airtable API key. \n  *Find under Airtable Account Overview: https://airtable.com/account")
        api_key = input()
    headers = {"Authorization" : "Bearer {}".format(api_key),
              'Content-Type': 'application/json'}
    validate_airtable_kwargs(api_key, "API key", "key")

    # Locate Base
    if base_id == None:
        print("Enter Airtable Base ID. \n  *Find under Airtable API Documentation: https://airtable.com/api for specific base]")
        base_id = input()
    url = 'https://api.airtable.com/v0/{}/'.format(base_id)
    path = url + table
    validate_airtable_kwargs(base_id, "Base ID", "app")
    
    # Validate Record ID
    if record_id != None:
        validate_airtable_kwargs(record_id, "Record ID", "rec")
    
    # Validate upload_data
    if type(upload_data) != dict:
        print("❌ Error: `upload_data` is not a dictonary.")
        return

    # Create New Record
    if record_id == None:
        upload_dict = {"records": [{"fields" : upload_data}], "typecast" : typecast}
        upload_json = json.dumps(upload_dict)
        response = requests.post(path, data=upload_json, headers=headers)
        airtable_response = response.json()

    # Update Record
    if record_id != None:
        path = "{}/{}".format(path, record_id)
        upload_dict = {"fields" : upload_data, "typecast" : True}
        upload_json = json.dumps(upload_dict)
        response = requests.patch(path, data=upload_json, headers=headers)
        airtable_response = response.json()
    
    # Identify Errors
    if 'error' in airtable_response:
        identify_errors(airtable_response)
        
    return airtable_response

# Troubleshooting Functions
def validate_airtable_kwargs(kwarg, kwarg_name, prefix, char_length=17, print_messages=True):
    """Designed for use with airtable_download() and airtable_upload() functions.
        Checks `api_key`, `base_id` and `record_id` arguments to see if they conform to the expected Airtable API format.
        """
    valid_status = True
    if len(kwarg) != char_length:
        if print_messages is True:
            print("⚠️ Caution: {} not standard length. Make sure API key is {} characters long.".format(kwarg_name, char_length))
        valid_status = False
    if kwarg.startswith(prefix) is False:
        if print_messages is True:
            print("⚠️ Caution: {} doesn't start with `{}`.".format(kwarg_name, prefix))
        valid_status = False
    return valid_status


def identify_errors(airtable_response):
    """Designed for use with airtable_download() and airtable_upload() functions.
        Prints error responses from the Airtable API in an easy-to-read format.
        """
    if 'error' in airtable_response:
        try:
            print('❌ {} error: "{}"'.format(airtable_response['error']['type'], airtable_response['error']['message']))
        except:
            print("❌ Error: {}".format(airtable_response['error']))
    return

api_key = "keyVDH1Gwtqdojtxo"
base_id = "appoguJpf3CsaChkv"
headers = {"Authorization": "Bearer " + api_key}

table_name = "Application"

upload_data = {}

i = 0
while i<len(url_list):
    url = url_list[i]
    r = requests.get(url,{'headers':headers})
    soup = bs4.BeautifulSoup(r.text,{'html.parser'})
    job_title = soup.find_all('div', {'class': 'cached-bot-header-skeletonstyle__CachedBotJobViewHeaderContainer-sc-rp06gd-0 hptUYw'})[0].find_all('h1')[-1].text #job description
    company_name = soup.find_all('div', {'class': 'cached-bot-header-skeletonstyle__CachedBotJobViewHeaderContainer-sc-rp06gd-0 hptUYw'})[0].find_all('h2')[-1].text #-- Company name
    info = [job_title, company_name, url]
    #print(info)
    info_set = {}
    info_set["positionName"] = info[0]
    info_set["company"] = info[1]
    info_set["URL"] = info[2]
    upload_data = info_set
    airtable_upload(table_name, upload_data, False, api_key, base_id)
    #print(info_set)
    #i = i+1
    
    #Step 2
    upload_dict = {"records" : [{"fields" : info_set}], 
               "typecast" : False}
    print(upload_dict)
    # Step 3
    upload_json = json.dumps(upload_dict)
    # Step 4
    response = requests.post("https://api.airtable.com/v0/appoguJpf3CsaChkv/Application", data=upload_json, headers=headers)
    print(response)
    i=i+1;
