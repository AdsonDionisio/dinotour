import sqlite3
import os

db_path = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE site ADD COLUMN image_vr_filename VARCHAR(255)")
    print("Column VR added successfully")
except Exception as e:
    print(f"Error: {e}")
conn.commit()
conn.close()
