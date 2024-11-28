import os
import subprocess

def restore_backup(db_name, db_user, db_password, backup_file, host='localhost', port=5432):

    command = f"PGPASSWORD={db_password} psql -U {db_user} -h {host} -p {port} {db_name} < {backup_file}"

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"База данных {db_name} успешно восстановлена из {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при восстановлении базы данных: {e}")


#restore_backup('my_database', 'postgres', 'password', '/path/to/backup/my_database_backup_20231129153000.sql')