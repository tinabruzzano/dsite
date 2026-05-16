# dsite/management/migrations.py


from dsite.db import Model
from pathlib import Path
import subprocess


def makemigrations(project_name):
    print(f"[DSite] makemigrations per {project_name}")
    migration = "migration.tar.gz"
    fileofmig = Path(migration)
    MIG_ROOT = Path(__file__)
    subprocess.run(f"tar -czfd {fileofmig} *")
    subprocess.rub("mkdir project_migrations")
    subprocess.run(f"cp {fileofmig} project_migrations/")
    
    

def migrate(project_name):
    print(f"[DSite] migrate per {project_name}")
    print("[DSite] (placeholder) database sincronizzato")
