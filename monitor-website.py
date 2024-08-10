import time
import paramiko
import requests
import smtplib
import os
import paramiko
import linode_api4
import time
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
LINODE_TOKEN = os.environ.get('token_for_linode_machine')


def notify(email_msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE IS DOWN!!! \n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)

def restart_container():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('ip_of_server', username='root', key_filename='key/file/.ssh/id_rsa')
    stdin, stdout, stderr = ssh.exec_command('docker start container_id')
    print(stdout.readlines())
    ssh.close()

def monitor_app():
    try:
        response = requests.get('ip-of-linode-with-port')
        if response.status_code == 200:
            print("app is running, status = UP!")
        else:
            print("app is not running, status = DOWN!")
            msg = f"application returned {response.status_code} "
            # send Email to a person
            notify(msg)

            #restart the app
            restart_container()
            print('Applicaton restarted')
    except Exception as ex:
        print(f'Connection error: {ex}')
        msg="app is not even available"
        notify(msg)

        #restart linode server
        print("Rebooting the server......")
        client = linode_api4.LinodeClient(LINODE_TOKEN)
        nginx_server = client.load(linode_api4.Instance, 213213123)
        nginx_server.reboot()

        #restart the app

        while True:
            nginx_server = client.load(linode_api4.Instance, 213213123)
            if nginx_server.status == 'running':
                time.sleep(15)
                restart_container()
                break

schedule.every(20).minutes.do(monitor_app)

while True:
    schedule.run_pending()
