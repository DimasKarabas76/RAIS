import os
import subprocess
import time
import paramiko
from datetime import datetime


def create_backup_ssh(db_name, user, remote_host, backup_dir, ssh_user):
    # Формируем имя файла для резервной копии
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_file = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.dump")

    # Строим команду для выполнения через SSH
    dump_command = f"pg_dump -U {user} -h localhost -F c -b -v {db_name} > {backup_file}"

    # Устанавливаем SSH-соединение
    try:
        # Создаем SSH клиент
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Подключаемся по ключу
        ssh.connect(remote_host, username=ssh_user)

        # Выполняем команду на удаленной машине
        stdin, stdout, stderr = ssh.exec_command(dump_command)

        # Выводим результаты
        print(stdout.read().decode())
        error = stderr.read().decode()
        if error:
            print(f"Error: {error}")

        ssh.close()
    except Exception as e:
        print(f"SSH connection failed: {e}")


def run_periodically(interval, db_name, user, remote_host, backup_dir, ssh_user):
    while True:
        create_backup_ssh(db_name, user, remote_host, backup_dir, ssh_user)
        time.sleep(interval)


if __name__ == "__main__":
    # Параметры для подключения и бэкапа
    db_name = 'auth_db'
    user = 'dima'
    remote_host = '172.25.204.9'
    backup_dir = '/home/dima/pract_RAIS'
    ssh_user = 'postgres'  # Пользователь для SSH

    # Запускаем бэкап каждые 5 минут (600 секунд)
    run_periodically(300, db_name, user, remote_host, backup_dir, ssh_user)