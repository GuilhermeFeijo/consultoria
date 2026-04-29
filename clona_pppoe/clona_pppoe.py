import secrets
import paramiko

host = secrets.host
port = secrets.port
user = secrets.user
password = secrets.password

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(host, port=port, username=user, password=password)

stdin, stdout, stderr = ssh.exec_command("ppp secret export")

print(stdout.read().decode())
print(stderr.read().decode())

ssh.close()