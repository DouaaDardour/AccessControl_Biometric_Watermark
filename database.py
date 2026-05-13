import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('../database.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT,
            photo_path TEXT,
            autorise BOOLEAN DEFAULT 1
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_id INTEGER,
            action TEXT NOT NULL,
            watermark TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de données initialisée avec succès !")


def add_user(nom, prenom, email, photo_path, autorise=True):
    conn = sqlite3.connect('../database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (nom, prenom, email, photo_path, autorise) VALUES (?,?,?,?,?)",
              (nom, prenom, email, photo_path, autorise))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    print(f"✅ Utilisateur ajouté : {prenom} {nom} (ID: {user_id})")
    return user_id


def add_log(user_id, action, watermark):
    conn = sqlite3.connect('../database.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO logs (timestamp, user_id, action, watermark) VALUES (?,?,?,?)",
              (timestamp, user_id, action, watermark))
    conn.commit()
    conn.close()


# ====================== TEST ======================
if __name__ == "__main__":
    init_db()
    print("Base de données prête !")