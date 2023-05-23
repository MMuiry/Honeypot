import subprocess

#Gets data on ssh service
result = subprocess.run(['systemctl', 'is-active', 'ssh'], capture_output=True)


# Decode result to only get service status
status = result.stdout.decode('utf-8').strip()

# Check if the server is active
if status == 'active':
    print('Stopping OpenSSH-Server...')
    subprocess.run(["sudo" ,"systemctl", "stop", "ssh"])



#Telnet
result = subprocess.run(['systemctl', 'is-active', 'xinetd'], capture_output=True)

# Decode the output of the command
status = result.stdout.decode('utf-8').strip()

# Check if the server is active
if status == 'active':
    print('Stopping Telnet...')
    subprocess.run(["sudo" ,"systemctl", "stop", "xinetd"])



result = subprocess.run(['systemctl', 'is-active', 'vsftpd'], capture_output=True)

# Decode the output of the command
status = result.stdout.decode('utf-8').strip()

# Check if the server is active
if status == 'active':
    print('Stopping FTP...')
    subprocess.run(["sudo" ,"systemctl", "stop", "vsftpd"])



result = subprocess.run(['systemctl', 'is-active', 'apache2'], capture_output=True)

# Decode the output of the command
status = result.stdout.decode('utf-8').strip()

# Check if the server is active
if status == 'active':
    print('Stopping Apache2-Server...')
    subprocess.run(["sudo" ,"systemctl", "stop", "apache2"])

