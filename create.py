import os
import time
import paramiko
from datetime import datetime

def create_backup_ssh(db_name, user, remote_host, backup_dir, ssh_user, ssh_password):
    # Формируем имя файла для резервной копии
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Строим команду для выполнения через SSH
    dump_command = f"pg_dump -U {user} -h localhost -F c -b -v {db_name} > {backup_file}"

    try:
        # Создаем SSH клиент
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Подключаемся по паролю
        ssh.connect(remote_host, username=ssh_user, password=ssh_password)

        sftp = ssh.open_sftp()
        local_backup_path = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.dump")
        sftp.get(backup_file, local_backup_path)
        print(f"Backup file downloaded to: {local_backup_path}")

        # Удаляем файл на удаленном сервере
        sftp.remove(backup_file)

        # Закрываем соединения
        sftp.close()
        ssh.close()

    except Exception as e:
        print(f"SSH connection failed: {e}")

def run_periodically(interval, db_name, user, remote_host, backup_dir, ssh_user, ssh_password):
    while True:
        create_backup_ssh(db_name, user, remote_host, backup_dir, ssh_user, ssh_password)
        time.sleep(interval)

if __name__ == "__main__":
    db_name = 'auth_db'
    user = 'dima'
    remote_host = '172.25.204.9'
    backup_dir = '/home/dima/pract_RAIS'
    ssh_user = 'postgres'
    ssh_password = '123'

    run_periodically(300, db_name, user, remote_host, backup_dir, ssh_user, ssh_password)