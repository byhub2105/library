from flask import Flask,render_template,url_for,redirect,request
from werkzeug.utils import secure_filename
import sqlite3,os
app = Flask(__name__)
def db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    if not os.path.exists('books.db'):
        conn = db_connection()
        conn.execute('''
CREATE TABLE IF NOT EXISTS books(
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    description TEXT,
                    year INTEGER
                    )
''')
        conn.commit()
        conn.close()
init_db()
# 
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/library', methods=['GET','POST'])
def books():
    conn = db_connection()
    if request.method == 'POST':
        book = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        year = request.form.get('year')
        if book:
            conn.execute('INSERT INTO books(title,author,description,year) VALUES (?,?,?,?)',(book,author,description,year))
            conn.commit()
            conn.close()
            return redirect(url_for('books'))
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('library.html',books = books)

@app.route('/author')
def author():
    return render_template('author.html')

@app.route('/delete/<int:id>')
def delete_book(id):
    conn = db_connection()
    conn.execute('DELETE FROM books WHERE id=?',(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('books'))
@app.route('/book/<id>')
def desc(id):
    conn = db_connection()
    book_detail =conn.execute('SELECT * FROM books WHERE id=?',(id,)).fetchone()
    conn.close()
    return render_template('book.html', book = book_detail)
if __name__ == '__main__':
    app.run(debug=True)