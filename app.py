from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Adiciona a configuração de CORS ao aplicativo

@app.route('/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, bookUrl, imageUrl, author FROM books')
    books = cursor.fetchall()
    conn.close()
    return jsonify(books)

if __name__ == '__main__':
    app.run(debug=True)
