from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Chemin vers la base de données SQLite
DB_PATH = 'inventory.db'

# Fonction pour créer la table dans la base de données
def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      nom TEXT,
                      grade TEXT,
                      machine TEXT,
                      reseau TEXT,
                      adresse_mac TEXT,
                      num_bureau TEXT,
                      etage TEXT
                      )''')
    conn.commit()
    conn.close()

# Fonction pour insérer une entrée dans la base de données
def insert_entry(nom, grade, machine, reseau, adresse_mac, num_bureau, etage):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO inventory (nom, grade, machine, reseau, adresse_mac, num_bureau, etage)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (nom, grade, machine, reseau, adresse_mac, num_bureau, etage))
    conn.commit()
    conn.close()

# Route pour afficher le formulaire de saisie
@app.route('/')
def index():
    return render_template('index.html')

# Route pour traiter les données du formulaire
@app.route('/add', methods=['POST'])
def add_entry():
    nom = request.form['nom']
    grade = request.form['grade']
    machine = request.form['machine']
    reseau = request.form['reseau']
    adresse_mac = request.form['adresse_mac']
    num_bureau = request.form['num_bureau']
    etage = request.form['etage']
    insert_entry(nom, grade, machine, reseau, adresse_mac, num_bureau, etage)
    return redirect(url_for('index'))

# Route pour afficher toutes les entrées de l'inventaire
@app.route('/inventory')
def inventory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM inventory''')
    entries = cursor.fetchall()
    conn.close()
    return render_template('inventory.html', entries=entries)

if __name__ == '__main__':
    create_table()
    app.run(host='10.8.1.248', port=5000, debug=True)
