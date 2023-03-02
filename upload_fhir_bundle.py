import json
import os
import requests
import argparse

def send_data_to_fhir(file_name):
    """
    This function will open a file and send the json data to the FHIR server.
    """

    # Make sure the encoding is utf-8
    with open(dirTestPatients+file_name, "r", encoding='utf-8') as bundle_file:
        data = bundle_file.read()

    r = requests.post(url = URL, data = data, headers = headers)

    # Output file name that was processed + the status code
    print(file_name)
    print(r.status_code)

# Setting up argparse
parser = argparse.ArgumentParser(description='Uploads dummy data to a FHIR server.')
parser.add_argument('path', type=str, help='Path to the output directory of Synthea')
parser.add_argument('--url', default="http://localhost:8080/fhir/", help='URL to the FHIR server (default: "http://localhost:8080/fhir/")')
args = parser.parse_args()

# FHIR server endpoint
URL = args.url

# FHIR server json header content
headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

# This path is specific to my setup
dirTestPatients = args.path
# Loop over all files in the output folder in order to upload each json file for each patient.
for dirpath, dirnames, files in os.walk(dirTestPatients):

    # Finding hospital information and creating the bundle first
    for file_name in files:
        if "hospitalInformation" in file_name:
            send_data_to_fhir(file_name)
            break

    # Finding practioners and creating the bundle second
    for file_name in files:
        if "practitionerInformation" in file_name:
            send_data_to_fhir(file_name)
            break

    # Creating the patients
    for file_name in files:
        if ("hospitalInformation" not in file_name) and ("practitionerInformation" not in file_name):
            send_data_to_fhir(file_name)
