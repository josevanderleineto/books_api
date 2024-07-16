from flask import Flask, jsonify, request
from flask_cors import CORS  # Importe o CORS

import sqlite3

app = Flask(__name__)
CORS(app)  # Permite CORS para todas as rotas da sua aplicação

def init_db():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            bookUrl TEXT NOT NULL,
            imageUrl TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.execute('SELECT COUNT(*) FROM books')
    if cursor.fetchone()[0] == 0:
        books = [
            (1, "As contribuições de ranganathan para a biblioteconomia: reflexões e desafios", 
             "https://firebasestorage.googleapis.com/v0/b/free-reading-9595e.appspot.com/o/Ci%C3%AAncia%20da%20Informa%C3%A7%C3%A3o%2Fas-contribuicoes-de-raganathan.pdf?alt=media&token=15acf98b-5340-49d9-9434-6257d662672f", 
             "https://imgs.search.brave.com/_NMOBioiwCvDoREWVMzwO4Guvk-Yth2h1fw02vN6Pig/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9maWxl/cy5wYXNzZWlkaXJl/dG8uY29tL1RodW1i/bmFpbC9lMzdlYmY0/Zi1kM2FmLTRlNDIt/OWEwZi1lMmIzYzMy/YmEwODcvMjEwLzEu/anBn", 
             "Paulo Coelho"),
            (2, "As contribuições de paul otlet para a biblioteconomia", 
             "https://firebasestorage.googleapis.com/v0/b/free-reading-9595e.appspot.com/o/Ci%C3%AAncia%20da%20Informa%C3%A7%C3%A3o%2Fascontribuicoes-de-poul-outlet.pdf?alt=media&token=f6e23d41-ebd8-4d72-9a7f-dcd5dbdf4043", 
             "https://cip.brapci.inf.br//img/c/00/22/37/76/image.jpg", 
             "Poul Otlet"),
            (3, "Classification decimal dewey - CDD comentada", 
             "https://firebasestorage.googleapis.com/v0/b/free-reading-9595e.appspot.com/o/Ci%C3%AAncia%20da%20Informa%C3%A7%C3%A3o%2Fascontribuicoes-de-poul-outlet.pdf?alt=media&token=f6e23d41-ebd8-4d72-9a7f-dcd5dbdf4043", 
             "https://imgs.search.brave.com/v-o4MUXOi8HKTTR7T8PghCwU_y51MwkIUa9tl4MZ8ds/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL0kv/NDF3eDVtdFdFRkwu/anBn", 
             "Dewey"),
            (4, "Saberes informacionais na América Latina.", 
             "https://firebasestorage.googleapis.com/v0/b/free-reading-9595e.appspot.com/o/Ci%C3%AAncia%20da%20Informa%C3%A7%C3%A3o%2Fsaberes-informacionas.pdf?alt=media&token=48d4e831-5b06-4917-8cc9-e75df770e289", 
             "https://cip.brapci.inf.br//img/c/00/25/44/74/image.png", 
             "Jussara Borges de Lima (org) | Thiago Henrique Bragato Barros (org)"),
            (5, "Dicionario de Bibliotenomia e Arquivologia", 
             "https://firebasestorage.googleapis.com/v0/b/free-reading-9595e.appspot.com/o/Ci%C3%AAncia%20da%20Informa%C3%A7%C3%A3o%2Fdicionario-de-biblitenomia-e-arquivologia.pdf?alt=media&token=57ab4285-080c-4e52-b3e6-db6446316e44", 
             "https://imgs.search.brave.com/cDorxYHEG6jTD-kx8E0E5bfub3xZftBF8kypYx-mjRA/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9iaWJs/aW90ZWNhLmNhZGUu/Z292LmJyL2NnaS1i/aW4va29oYS9vcGFj/LWltYWdlLnBsP3Ro/dW1ibmFpbD0xJmlt/YWdlbnVtYmVyPTc", 
             "Murilo Bastos da Cunha, Cordélia Robalinho de Oliveira Cavalcanti")
        ]
        cursor.executemany('''
            INSERT INTO books (id, title, bookUrl, imageUrl, author)
            VALUES (?, ?, ?, ?, ?)
        ''', books)
        conn.commit()

    conn.close()

@app.route('/books', methods=['GET'])
def get_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    
    books_list = []
    for book in books:
        books_list.append({
            "id": book[0],
            "title": book[1],
            "bookUrl": book[2],
            "imageUrl": book[3],
            "author": book[4]
        })
    return jsonify(books_list)

@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (title, bookUrl, imageUrl, author)
        VALUES (?, ?, ?, ?)
    ''', (new_book['title'], new_book['bookUrl'], new_book['imageUrl'], new_book['author']))
    conn.commit()
    conn.close()
    return jsonify(new_book), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)
