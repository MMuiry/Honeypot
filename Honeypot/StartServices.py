import subprocess

#starts services 


#starts ssh if not active
def ssh_start():
    result = subprocess.run(['systemctl', 'is-active', 'ssh'], capture_output=True)

    # Decode the output of the command
    status = result.stdout.decode('utf-8').strip()

    # Check if the server is active
    if status == 'active':
        print('OpenSSH server is running.')
    else:
        print('Starting OpenSSH-Server...')
        subprocess.run(["sudo" ,"systemctl", "start", "ssh"])


#starts telnet if not active
def telnet_start():
    result = subprocess.run(['systemctl', 'is-active', 'xinetd'], capture_output=True)

    try:
        subprocess.check_call(['sudo', '/etc/init.d/xinetd', 'start'])
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

#starts ftp if not active
def ftp_start():
    result = subprocess.run(['systemctl', 'is-active', 'vsftpd'], capture_output=True)

    # Decode the output of the command
    status = result.stdout.decode('utf-8').strip()

    # Check if the server is active
    if status == 'active':
        print('FTP server is running.')
    else:
        print('Starting FTP...')
        subprocess.run(["sudo" ,"systemctl", "start", "vsftpd"])

#starts apache2 if not active

def apache2_start():
    result = subprocess.run(['systemctl', 'is-active', 'apache2'], capture_output=True)

    # Decode the output of the command
    status = result.stdout.decode('utf-8').strip()

    # Check if the server is active
    if status == 'active':
        print('Apache2 server is running.')
    else:
        print('Starting apache2...')
        subprocess.run(["sudo" ,"systemctl", "start", "apache2"])



def run():
    subprocess.run(["sudo", "python3", "StopServices.py"])
    file_path = "chosenservices.txt"
    #depending on what the user choose, it will run the services
    with open(file_path, "r") as file:
        servicesArray = [service.strip() for service in file.readlines()]
    for service in servicesArray:
        if service == "22l":
            ssh_start()

        if service == "21l":
            ftp_start()
        if service == "80l":
            apache2_start()
            #actives low interaction website
            subprocess.run(['sudo', 'a2dissite', 'medHoneypot.conf'])
            subprocess.run(['sudo', 'a2ensite', 'lowHoneypot.conf'])
            subprocess.run(['sudo', 'systemctl', 'reload', 'apache2'])
        if service == "80m":
            apache2_start()
            #actives med interaction website
            subprocess.run(['sudo', 'a2dissite', 'lowHoneypot.conf'])
            subprocess.run(['sudo', 'a2ensite', 'medHoneypot.conf'])
            subprocess.run(['sudo', 'systemctl', 'reload', 'apache2'])
        if service == "23l":
            telnet_start()
run()

