import os
import datetime
import subprocess


def create_backup(db_name, db_user, db_password, backup_dir, host='localhost', port=5432):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Директория {backup_dir} не существует, она была создана.")

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    backup_filename = f"{db_name}_backup_{timestamp}.sql"
    backup_path = os.path.join(backup_dir, backup_filename)

    command = f"PGPASSWORD={db_password} pg_dump -U {db_user} -h {host} -p {port} {db_name} -f {backup_path}"

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Резервная копия базы данных {db_name} успешно создана: {backup_path}")
        return backup_path
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании резервной копии: {e}")
        return None

#backup_file = create_backup('my_database', 'postgres', 'password', '/path/to/backup')