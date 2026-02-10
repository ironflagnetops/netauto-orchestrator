import time
from utils import write_json_out,sshConnect,nb_grab_devices_by_role

#---------------#
#   FUNCTIONS   #
#---------------#



#------------------#
#   SCRIPT START   #
#------------------#
# User enters SD-WAN SSH credentials
print("\nPlease enter SD-WAN Credentials")
sdw_user, sdw_pass = login_cred()
print()

error_sites = {}

dev_lib = nb_grab_devices_by_role('sd-wan')

for dev in dev_lib:
    #print(dev)
    if 'ERROR' not in dev['mgmt_ip']:
        wan1,wan2 = sshConnect(dev['mgmt_ip'],dev['name'])
        dev['wan1'] = wan1
        dev['wan2'] = wan2

write_json_out(dev_lib,'nb_pub')