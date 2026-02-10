import time

#------------------------------------------------------------------------------------------------------------------------#
#   SDWAN - PULL WAN IP(S)                                                                                               #
#------------------------------------------------------------------------------------------------------------------------#
# Using Paramiko SSH connection to pull WAN IP address from Extreme SD-WAN device
#
#   @param  conn            Interactive shell from Paramiko SSH connection

def pull_sdwan_wan_addr(conn):
    
    print('Grabbing Router1 WAN IP...')
    conn.send("router 1\n")
    time.sleep(1)
    # Clear the buffer on the screen
    junked = conn.recv(1000)
    conn.send("ifconfig rt1p2\n")
    time.sleep(1)
    wan1_output = conn.recv(1000)
    conn.send('exit\n')
    output = conn.recv(1000)
    
    print('Grabbing Router2 WAN IP...')
    conn.send("router 2\n")
    time.sleep(1)
    # Clear the buffer on the screen
    junked = conn.recv(1000)
    conn.send("ifconfig rt2p2\n")
    time.sleep(1)
    wan2_output = conn.recv(1000)
    
    pub1=None
    pub2=None

    pub1_raw = str(wan1_output).split('\\n')
    for a in pub1_raw:
        if 'inet ' in a:
            pub1 = a.split('inet ',1)[1]
            pub1 = pub1.split(' ',1)[0]
            #print(f'WAN1: {pub1}')
            break

    pub2_raw = str(wan2_output).split('\\n')
    for b in pub2_raw:
        if 'inet ' in b:
            pub2 = b.split('inet ',1)[1]
            pub2 = pub2.split(' ',1)[0]
            #print(f'WAN2: {pub2}')
            break

    return pub1,pub2