import sqlite3

from flask import Flask, render_template, abort, request, redirect, url_for

# Importar la función get_db_connection desde db.py
from db import get_db_connection

app = Flask(__name__)

# SE DEBE ELIMINAR O COMENTAR ESTA FUNCION PARA EVITAR LLAMADAS RECURSIVAS INFINITAS
# def get_db_connection():
#     # Establece la conexión con la base de datos SQLite.
#     conn = get_db_connection()  # Ahora la función es importada desde db.py
#     conn.row_factory = sqlite3.Row
#     return conn

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html') # Se cambio "index.html" por "home.html" que si existe

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/post', methods=['GET'])
def get_all_post():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()  # Se debe usar "fetchall" en vez de "fetchone" para obtener todos los registros.
    conn.close()
    return render_template('post/posts.html', posts=posts)

@app.route('/post/<int:post_id>', methods=['GET'])
def get_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return render_template('post/post.html', post=post)

@app.route('/post/create', methods=['GET','POST'])
def create_one_post():
    if request.method == 'POST':
        title = request.form['title']
        contend = request.form['content'] # Se cambio "contend" por "content"

        # Validación: Verificar si el título está vacío
        if not title.strip():  # Si el título está vacío o solo tiene espacios
            error_message = "El título es obligatorio."
            return render_template('post/create.html', error_message=error_message)

        # Si el título no está vacío, proceder a guardar en la base de datos
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, contend))  # Se cambio "!" por "?".
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_post'))  # Se cambio "redirect(url_for('/post'))" por "redirect(url_for('get_all_post'))".

    return render_template('post/create.html')

@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def edit_one_post(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_db_connection()
        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_post'))

    elif request.method == 'GET':
        return render_template('post/edit.html', post=post)

@app.route('/post/delete/<post_id>', methods=['POST'])  # Eliminado "str:" en las cadenas esta implícito.
def delete_one_post(post_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))  # Agregada una coma en "(post_id,)" para que sea una tupla.
    conn.commit()
    conn.close()

    return redirect(url_for('get_all_post'))

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')  # Se agrego "host='0.0.0.0'".
