import requests,os
from dotenv import load_dotenv

load_dotenv()  # This loads the variables from .env

#------------------------------------------------------------------------------------------------------------------------#
#   ENVIRONMENT VARIABLES                                                                                                #
#------------------------------------------------------------------------------------------------------------------------#
access_token = os.getenv("API_KEY_NETBOX_PROD")
api_url = os.getenv("API_URL_NETBOX_PROD")

#------------------------------------------------------------------------------------------------------------------------#
#   SDWAN - PULL WAN IP(S)                                                                                               #
#------------------------------------------------------------------------------------------------------------------------#
# Using Paramiko SSH connection to pull WAN IP address from Extreme SD-WAN device
#
#   @param  role_slug            Interactive shell from Paramiko SSH connection

def nb_grab_devices_by_role(role_slug):  
    print(f"--> Grabbing 'Devices' Data By Role ... ")
    response = requests.get(f'{api_url}dcim/devices/?limit=1000&role={role_slug}', headers={'Authorization': f'Token {access_token}'})
    json_devices = response.json()['results']

    device_lib = []
    for device in json_devices:
        dev_dict = {}
        dev_dict['name'] = device['name']
        dev_dict['role'] = device['role']['name']
        dev_dict['manufacturer'] = device['device_type']['manufacturer']['name']
        dev_dict['model'] = device['device_type']['model']
        dev_dict['status'] = device['status']['value']
        if device['platform'] is not None:
            dev_dict['platform'] = device['platform']['name']
        else:
            dev_dict['platform'] = 'ERROR: Missing'
        if device['serial'] is not None:
            dev_dict['serial'] = device['serial']
        else:
            dev_dict['serial'] = 'ERROR: Missing'
        if device['primary_ip'] is not None:
            dev_dict['mgmt_ip'] = device['primary_ip']['display'].split('/')[0]
        else:
            dev_dict['mgmt_ip'] = 'ERROR: Missing'
        device_lib.append(dev_dict)
    return device_lib