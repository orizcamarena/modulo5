from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('diccionario.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS palabra (
                palabra text,
                significado text
                )""")
conn.commit()
conn.close()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_palabra', methods=['GET', 'POST'])
def add_palabra():
    if request.method == 'POST':
        palabra = request.form['palabra']
        significado = request.form['significado']
        conn = sqlite3.connect('diccionario.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO palabra (palabra, significado) VALUES (?, ?)", (palabra, significado))
        conn.commit()
        conn.close()
        return 'La palabra fue agregada correctamente..'
    else:
        return render_template('add_palabra.html')


@app.route('/todPalabra')
def todPalabra():
    conn = sqlite3.connect('diccionario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM palabra")
    palabra = cursor.fetchall()
    conn.close()
    return render_template('todPalabras.html', palabra=palabra)


@app.route('/buscarPalabra', methods=['GET', 'POST'])
def buscarPalabra():
    if request.method == 'POST':
        buscarPalabra = request.form['buscarPalabra']
        conn = sqlite3.connect('diccionario.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM palabra WHERE palabra=?", (buscarPalabra,))
        palabra = cursor.fetchall()
        conn.close()
        return render_template('buscarPalabra.html', palabra=palabra)
    else:
        return render_template('buscarPalabra_form.html')


@app.route('/delete_palabra/<palabra>', methods=['POST'])
def delete_palabra(palabra):
    conn = sqlite3.connect('diccionario.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM palabra WHERE palabra=?", (palabra,))
    conn.commit()
    conn.close()
    return redirect(url_for('todPalabras'))


if __name__ == '__main__':
    app.run(debug=True)
