import paramiko,sys,os,datetime,socket
from getpass import getpass
from netmiko import Netmiko
from netmiko.exceptions import NetmikoTimeoutException,NetmikoAuthenticationException

#------------------------------------------------------------------------------------------------------------------------#
#   LOGIN PROMPT - USER/PASS                                                                                             #
#------------------------------------------------------------------------------------------------------------------------#
# Gets user credentials for use later in script
# Example:
#   print("\nPlease enter Router Credentials")
#   rtr_user, rtr_pass = login_cred()

def login_cred():
    print('-'*32)
    user = input("Username: ")
    key = getpass()
    print('*'*32)
    return(user, key)

#------------------------------------------------------------------------------------------------------------------------#
#  LOGIN PROMPT - USER/PASS/ENABLE                                                                                       #
#------------------------------------------------------------------------------------------------------------------------#
# Gets user credentials for use later in script
# Example:
#   print("\nPlease enter Router Credentials")
#   rtr_user, rtr_pass, rtr_enable = login_cred_enable()

def login_cred_enable():
    print('-'*32)
    user = input('Username: ')
    key = getpass()
    sys.stdout.write('Enable ')
    secret = getpass()
    print('*'*32)
    return(user, key, secret)

#------------------------------------------------------------------------------------------------------------------------#
#   SSH CONNECTION - SINGLE (PARAMIKO)                                                                                   #
#------------------------------------------------------------------------------------------------------------------------#
# Connect to the device, and print out auth or timeout errors
#
#   @param  ipaddr          IP address of the device    (e.g., '172.16.103.2')
#   @param  hostname        Hostname of the device      (e.g., 'gfs-bb-rtr')
#   @param  login_user      Username for login (usually obtained through function login_cred)
#   @param  login_pass      Password for login (usually obtained through function login_cred)

def sshConnect(ipaddr,hostname,login_user,login_pass):
    try:
        # Create an SSH client
        print(f'Attempting connection to {hostname} ...')
        client = paramiko.SSHClient()

        # Automatically add the remote host key (use with caution in production)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote host
        client.connect(ipaddr, port=22, username=login_user, password=login_pass)
        print(f"Connected to {hostname}. Opening shell ...")
        
        # Invoke an interactive shell session
        shell = client.invoke_shell()
        print("Interactive shell opened.")

        '''
        pub1,pub2 = pull_wan_addr(shell)

        # Close the connection
        print(f'Disconntecting from {hostname} ...')
        client.close()
        print(f'Connection closed.\n{"*"*48}')
        return(pub1,pub2)
        '''
        return(shell)

    except paramiko.ssh_exception.AuthenticationException:
        print(f"Authentication failed. Please check your username and password.\n{'*'*48}")
        #pub1 = 'Error'
        #pub2 = 'Error'
        #return(pub1,pub2)
        return

    except paramiko.ssh_exception.SSHException as e:
        print(f"SSH error: {e}\n{'*'*48}")
        #pub1 = 'Error'
        #pub2 = 'Error'
        #return(pub1,pub2)
        return

    except Exception as e:
        print(f"An error occurred: {e}\n{'*'*48}")
        #pub1 = 'Error'
        #pub2 = 'Error'
        #return(pub1,pub2)
        return

''' WORKING COPY
def sshConnect(ipaddr,hostname,cred_user,cred_pass):
    try:
        # Create an SSH client
        print(f'Attempting connection to {hostname} ...')
        client = paramiko.SSHClient()
        
        # Automatically add the remote host key (use with caution in production)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote host
        client.connect(ipaddr, port=22, username=cred_user, password=cred_pass)
        print(f"Connected to {hostname}. Opening shell ...")
        
        # Invoke an interactive shell session
        shell = client.invoke_shell()
        print("Interactive shell opened.")

        pub1,pub2 = pull_wan_addr(shell)

        # Close the connection
        print(f'Disconntecting from {hostname} ...')
        client.close()
        print(f'Connection closed.\n{"*"*48}')
        return(pub1,pub2)

    except paramiko.ssh_exception.AuthenticationException:
        print(f"Authentication failed. Please check your username and password.\n{'*'*48}")
        pub1 = 'Error'
        pub2 = 'Error'
        return(pub1,pub2)

    except paramiko.ssh_exception.SSHException as e:
        print(f"SSH error: {e}\n{'*'*48}")
        pub1 = 'Error'
        pub2 = 'Error'
        return(pub1,pub2)

    except Exception as e:
        print(f"An error occurred: {e}\n{'*'*48}")
        pub1 = 'Error'
        pub2 = 'Error'
        return(pub1,pub2)
'''

#------------------------------------------------------------------------------------------------------------------------#
#   SSH CONNECTION - SINGLE (NETMIKO)                                                                                    #
#------------------------------------------------------------------------------------------------------------------------#
# Connect to the device, and print out auth or timeout errors
#
#   @param  device_name     Hostname of the device      (e.g., 'gfs-bb-rtr')
#   @param  device_ip       IP address of the device    (e.g., '172.16.103.2')
#   @param  device_os       OS (netmiko) of the device  (e.g., cisco_ios, checkpoint_gaia_ssh)
#   @param  login_user      Username for login (usually obtained through function login_cred)
#   @param  login_pass      Password for login (usually obtained through function login_cred)
#   @param  login_secret    Enable password (usually obtained through function login_cred_enable)

def sshConnectNetDev(device_name, device_ip, device_os, login_user, login_pass, login_secret=''):
    
    if not os.path.exists('session_logs'):
        os.makedirs('session_logs')
    
    log_start = datetime.datetime.now()
    logTime = log_start.strftime("%Y%m%d_%H%M%S")

    device_settings =  {
            'host': device_ip,
            'username': login_user,
            'password': login_pass,
            'device_type': device_os,
            'secret': login_secret,
            'global_delay_factor': 3,
            #'banner_timeout': 30,
            'session_log': 'session_logs/{}_session_{}.log'.format(device_name,logTime)
        }
    
    # Function attempts to establish a SSH connection to device passed in parameters
    try:
        print("\nAttempting connection to {} ({}).".format(device_name, device_ip))
        net_connect = Netmiko(**device_settings)
    except NetmikoTimeoutException:
        print(f"Timeout error: {device_name} ({device_ip})")
        return(None)
    except NetmikoAuthenticationException:
        print(f"Authentication error: {device_name} ({device_ip})")
        return(None)
    except socket.gaierror as e:
        print(f"Name or service not known: {e}")
        return(None)
    except EOFError as e:
        print(f"Connection closed unexpectedly: {e}")
        return(None)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return(None)
    '''
    except:
        # If device cannot be reached, an error message will printed to the terminal and no
        # SSH connection will be returned to the variable set for this function
        print("--> ERROR: Connection to {} ({}) timed-out.\n".format(device_name, device_ip))
    '''
        # Here is where you can optionally write to output that the connection failed
        # Example:
        #     txt_output.write("{}: CONNECTION FAILED\n\n".format(device_hostname))
        #return(None)
    
    # Function returns an established SSH connection to the variable
    print("--> Connected to {} ({}).".format(device_name, device_ip))
    return(net_connect)
    # Make sure to disconnect the SSH session when you're done by sending net_connect.disconnect()


