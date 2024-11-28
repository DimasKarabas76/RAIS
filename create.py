import os
import subprocess
from datetime import datetime

def create_backup(db_name, user, password, backup_dir):
    os.environ['PGPASSWORD'] = password

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_file = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.sql")

    command = f"pg_dump -U {user} -F c -b -v -f {backup_file} {db_name}"
    subprocess.run(command, shell=True, check=True)

    print(f"Backup of database {db_name} created at {backup_file}")

if __name__ == "__main__":
    create_backup('/var/lib/postgresql/16/main/auth_db', 'postgres', 'dima777', '/pract_RAIS')