import os
import time
import subprocess
from datetime import datetime


def create_backup_ssh(db_name, user, remote_host, backup_dir, ssh_user, ssh_password):
    # Формируем имя файла для резервной копии
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_file = f"/var/lib/postgresql/dumps/{db_name}_backup_{timestamp}.dump"  # Создаем дамп в /tmp на удаленном сервере

    # Строим команду для выполнения через SSH
    dump_command = f"pg_dump -U postgres -h localhost -F c -b -v -f {backup_file} {db_name}"

    try:
        # Выполняем команду через SSH
        ssh_command = f"ssh {ssh_user}@{remote_host} '{dump_command}'"

        # Выполнение команды
        process = subprocess.Popen(ssh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Печатаем вывод для отладки
        if stderr:
            print(f"Error: {stderr.decode()}")
        else:
            print(f"Success: {stdout.decode()}")

        # Скачиваем файл на локальный сервер
        local_backup_path = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.dump")
        scp_command = f"scp {ssh_user}@{remote_host}:{backup_file} {local_backup_path}"

        # Выполняем команду scp для скачивания
        process = subprocess.Popen(scp_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Печатаем вывод для отладки
        if stderr:
            print(f"Error downloading file: {stderr.decode()}")
        else:
            print(f"Backup file downloaded to: {local_backup_path}")

    except Exception as e:
        print(f"SSH connection failed: {e}")


def run_periodically(interval, db_name, user, remote_host, backup_dir, ssh_user, ssh_password):
    while True:
        create_backup_ssh(db_name, user, remote_host, backup_dir, ssh_user, ssh_password)
        time.sleep(interval)


if __name__ == "__main__":
    # Параметры для подключения и бэкапа
    db_name = 'auth_db'
    user = 'dima'
    remote_host = '172.25.204.9'
    backup_dir = '/home/dima/pract_RAIS'  # Локальная директория для сохранения дампов
    ssh_user = 'postgres'  # Пользователь для SSH
    ssh_password = '123'  # Пароль для SSH подключения

    # Запуск бэкапов каждые 10 минут (600 секунд)
    run_periodically(10, db_name, user, remote_host, backup_dir, ssh_user, ssh_password)