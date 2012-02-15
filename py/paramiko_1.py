import os

from paramiko import SSHClient, SSHConfig

# ssh config file
config = SSHConfig()
ssh_config = os.path.join(os.path.expanduser('~'), '.ssh/config')
print ssh_config
config.parse(file(ssh_config))
o = config.lookup('zA')

# ssh client
pwd1 = 'uhbnmj^&*'
ssh_client = SSHClient()
ssh_client.load_system_host_keys()
ssh_client.connect(o['hostname'], username=o['user'], password=pwd1)

# run a command
print "\nRun a command"
cmd = 'ps aux'
stdin, stdout, stderr = ssh_client.exec_command(cmd)
for i, line in enumerate(stdout):
    line = line.strip()
    print "%d: %s" % (i, line)
    if i >= 9:
        break

# open a remote file
print "\nOpen a remote file"
sftp_client = ssh_client.open_sftp()
sftp_file = sftp_client.open('/var/log/mail.log')
for i, line in enumerate(sftp_file):
    print "%d: %s" % (i, line[:15])
    if i >= 9:
        break
sftp_file.close()
sftp_client.close()

# close ssh client
ssh_client.close()
