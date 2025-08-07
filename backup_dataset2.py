import os
import shutil

# Paths
project_root = "/home/nvidia07/cat-breed-detector"
data_dir = os.path.join(project_root, "data")
backup_dir = os.path.join(project_root, "data_backup2")

# Remove old backup if it exists
if os.path.exists(backup_dir):
    shutil.rmtree(backup_dir)
    print(f"🗑️ Removed existing backup at: {backup_dir}")

# Create new backup
try:
    shutil.copytree(data_dir, backup_dir)
    print(f"✅ Full dataset backup created at: {backup_dir}")
except Exception as e:
    print(f"❌ Backup failed: {e}")