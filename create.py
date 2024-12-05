import os
import time
import paramiko
from datetime import datetime

def create_backup_ssh(db_name, user, remote_host, backup_dir, ssh_user, ssh_password):
    # Формируем имя файла для резервной копии
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_file = f"/var/lib/postgresql/dumps/{db_name}_backup_{timestamp}.dump"  # Создаем дамп в /tmp на удаленном сервере

    # Строим команду для выполнения через SSH
    dump_command = f"pg_dump -U {user} -h localhost -F c -b -v -f {backup_file} {db_name}"


        # Создаем SSH клиент
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Подключаемся по паролю
    ssh.connect(remote_host, username=ssh_user, password=ssh_password)
    time.sleep(5)

        # Выполняем команду на удаленной машине
    ssh.exec_command(dump_command)
    time.sleep(15)


        # Скачиваем файл на локальный сервер, если нужно
    sftp = ssh.open_sftp()
    local_backup_path = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.dump")
    sftp.get(backup_file, local_backup_path)
    print(f"Backup file downloaded to: {local_backup_path}")

        # Закрываем соединения
    sftp.close()
    ssh.close()


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