import paramiko, os
host = "139.9.6.3"; port = 22; user = "root"; password = "20061214Tony"
local_dir = r"D:\codex\website\origin\Mizuki\dist"
remote_dir = "/opt/1panel/www/sites/www.LpSite.com/index"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port=port, username=user, password=password, timeout=30)
print("SSH connected")
stdin, stdout, stderr = ssh.exec_command(f"rm -rf {remote_dir}/*")
stdout.channel.recv_exit_status()
print("Cleaned remote dir")

sftp = ssh.open_sftp()
uploaded = 0
for root, dirs, files in os.walk(local_dir):
    for d in dirs:
        rel = os.path.relpath(os.path.join(root, d), local_dir)
        rp = os.path.join(remote_dir, rel).replace("\\", "/")
        try: sftp.stat(rp)
        except: sftp.mkdir(rp)
    for f in files:
        lf = os.path.join(root, f)
        rel = os.path.relpath(lf, local_dir)
        rf = os.path.join(remote_dir, rel).replace("\\", "/")
        sftp.put(lf, rf)
        uploaded += 1
sftp.close()
ssh.close()
print(f"Uploaded {uploaded} files OK")
