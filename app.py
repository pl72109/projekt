import sqlite3
from flask import Flask, render_template, request, url_for, redirect, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twoj_sekretny_klucz_123'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Маршрут для отображения списка книг
@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)

# Маршрут для просмотра деталей конкретной книги
@app.route('/book/<int:book_id>')
def book_details(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    if book is None:
        return "Książka nie została znaleziona!", 404
    return render_template('details.html', book=book)

# Маршрут для добавления новой книги
@app.route('/add', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']

        if not title or not author or not description:
            flash('Wszystkie pola są wymagane!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO books (title, author, description) VALUES (?, ?, ?)',
                         (title, author, description))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
