#!/usr/bin/env python3

from ctf_gameserver import checkerlib
import logging
import http.client
import socket
import paramiko
import hashlib
import requests

PORT_WEB = 5000
PORT_API = 5001

def ssh_connect():
    def decorator(func):
        def wrapper(*args, **kwargs):
            # SSH connection setup
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            rsa_key = paramiko.RSAKey.from_private_key_file(f'/keys/team{args[0].team}-sshkey')
            client.connect(args[0].ip, username = 'root', pkey=rsa_key)

            # Call the decorated function with the client parameter
            args[0].client = client
            result = func(*args, **kwargs)

            # SSH connection cleanup
            client.close()
            return result
        return wrapper
    return decorator

class MyChecker(checkerlib.BaseChecker):

    def __init__(self, ip, team):
        checkerlib.BaseChecker.__init__(self, ip, team)
        self._baseurl = f'http://[{self.ip}]:{PORT_WEB}'
        logging.info(f"URL: {self._baseurl}")

    @ssh_connect()
    def place_flag(self, tick):
        flag = checkerlib.get_flag(tick)
        logging.info(f'flag to place: {flag}')
        creds = self._add_new_flag(self.client, flag)
        if not creds:
            return checkerlib.CheckResult.FAULTY
        logging.info('created')
        checkerlib.store_state(str(tick), creds)
        checkerlib.set_flagid(str(tick))
        return checkerlib.CheckResult.OK

    def check_service(self):
        # check if ports are open
        if not self._check_port_web(self.ip, PORT_WEB) or not self._check_port_web(self.ip, PORT_API):
            return checkerlib.CheckResult.DOWN
                
        file_path_web = '/app/templates/login.html'
        # check if index.html from toritoken_web has been changed by comparing its hash with the hash of the original file
        if not self._check_web_integrity(file_path_web):
            return checkerlib.CheckResult.FAULTY   
        
        file_path_web_app = '/app/app.py'
        if not self._check_web_app_login_integrity():
            return checkerlib.CheckResult.FAULTY   


        file_path_api = '/app/app.py'
        if not self._check_api_integrity(file_path_api):
            return checkerlib.CheckResult.FAULTY       
              
        return checkerlib.CheckResult.OK
    
    def check_flag(self, tick):
        if not self.check_service():
            return checkerlib.CheckResult.DOWN
        flag = checkerlib.get_flag(tick)
        #creds = checkerlib.load_state("flag_" + str(tick))
        # if not creds:
        #     logging.error(f"Cannot find creds for tick {tick}")
        #     return checkerlib.CheckResult.FLAG_NOT_FOUND
        flag_present = self._check_flag_present(flag)
        if not flag_present:
            return checkerlib.CheckResult.FLAG_NOT_FOUND
        return checkerlib.CheckResult.OK
        
    
    @ssh_connect()
    def _check_web_integrity(self, path):
        ssh_session = self.client
        command = f"docker exec toritoken_web_1 sh -c 'cat {path}'"
        stdin, stdout, stderr = ssh_session.exec_command(command)
        if stderr.channel.recv_exit_status() != 0:
            return False
        
        output = stdout.read().decode().strip()
        hashed = hashlib.md5(output.encode()).hexdigest()
        return hashlib.md5(output.encode()).hexdigest() == '80f61ba6afba238f04fa6906e650e1c8' # 
    
    # funtzio honek web app-ean loginak funtzionatzen duela konprobatzeko, erabiltzaile legitimo batek login egin ahal izatea
    @ssh_connect()
    def _check_web_app_login_integrity(self):
        ssh_session = self.client
        url = 'http://localhost:5000/login'
        text_to_search = 'Ongi etorri'
        curl_command = "curl -X POST http://localhost:5000/login -H 'Content-type: application/x-www-form-urlencoded' -d 'username=admin&password=password'"
        
        stdin, stdout, stderr = ssh_session.exec_command(curl_command)
        curl_response = stdout.read().decode()
        logging.info(f'curl_response: {curl_response}')
        
        if text_to_search in curl_response:
            return True
        else:
            return False
        
    
    @ssh_connect()
    def _check_api_integrity(self, path):
        ssh_session = self.client
        command = f"docker exec toritoken_api_1 sh -c 'cat {path}'"
        stdin, stdout, stderr = ssh_session.exec_command(command)
        if stderr.channel.recv_exit_status() != 0:
            return False
        
        output = stdout.read().decode().strip()
        hashed = hashlib.md5(output.encode()).hexdigest()
        #logging.info(f'Hashed api py: {hashed}')
        return hashlib.md5(output.encode()).hexdigest() == '7bab2b1068b42fa1b8598de77180e3eb' # 
    
      
    # Private Funcs - Return False if error
    def _add_new_flag(self, ssh_session, flag):
        # Execute the file creation command in the container
        command = f"docker exec toritoken_api_1 sh -c 'echo {flag} >> /tmp/flag.txt'"
        stdin, stdout, stderr = ssh_session.exec_command(command)

        # Check if the command executed successfully
        if stderr.channel.recv_exit_status() != 0:
            return False
        
        # Return the result
        return {'flag': flag}

    @ssh_connect()
    def _check_flag_present(self, flag):
        ssh_session = self.client
        command = f"docker exec toritoken_api_1 sh -c 'grep {flag} /tmp/flag.txt'"
        stdin, stdout, stderr = ssh_session.exec_command(command)
        if stderr.channel.recv_exit_status() != 0:
            return False

        output = stdout.read().decode().strip()
        return flag == output

    def _check_port_web(self, ip, port):
        try:
            conn = http.client.HTTPConnection(ip, port, timeout=5)
            conn.request("GET", "/")
            response = conn.getresponse()
            return response.status == 200
        except (http.client.HTTPException, socket.error) as e:
            print(f"Exception: {e}")
            return False
        finally:
            if conn:
                conn.close()

        
  
if __name__ == '__main__':
    checkerlib.run_check(MyChecker)




