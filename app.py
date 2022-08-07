from flask import Flask, jsonify, request, Response, json

app = Flask(__name__)

books = [
    {
        'name': 'Green Eggs and Ham',
        'price': 7.99,
        'ISBN': 9811223344
    },
    {
        'name': 'The Cat In The Hat',
        'price': 6.99,
        'ISBN': 9988771133
    }
]


def is_post_request_data_valid(bookObject):
    if ('name' in bookObject and 'price' in bookObject and 'ISBN' in bookObject):
        return True
    else:
        return False


def is_put_request_data_valid(bookObject):
    if ('name' in bookObject and 'price' in bookObject):
        return True
    else:
        return False


def is_patch_request_data_valid(bookObject):
    if 'name' in bookObject and 'price' in bookObject:
        return False
    elif 'name' in bookObject or 'price' in bookObject:
        return True
    else:
        return False


# GET /
@app.route('/')
def welcome_message():
    return 'Welcome to Book Management Python Service!'


# GET /books
@app.route('/books')
def get_books():
    return jsonify({'books': books})


# GET /books/<int:ISBN>
@app.route('/books/<int:ISBN>')
def get_book_by_ISBN(ISBN):
    return_value = {}
    for book in books:
        if book['ISBN'] == ISBN:
            return_value = {
                'name': book['name'],
                'price': book['price']
            }
    return jsonify(return_value)


# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if is_post_request_data_valid(request_data):
        new_book = {
            'name': request_data['name'],
            'price': request_data['price'],
            'ISBN': request_data['ISBN']
        }
        books.insert(0, new_book)
        response = Response('', 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(new_book['ISBN'])
    else:
        invalidBookObjectErrorMessage = {
            'error': 'Invalid book object passed in request',
            'helpString': 'Data passed in should be similar to this {"name": "Green Eggs and Ham","price": 7.99,'
                          '"ISBN": 9811223344} '
        }
        response = Response(json.dumps(
            invalidBookObjectErrorMessage), 400, mimetype='application/json')
    return response


# PUT /books/<int:ISBN>
@app.route('/books/<int:ISBN>', methods=['PUT'])
def update_book(ISBN):
    request_data = request.get_json()
    if is_put_request_data_valid(request_data):
        new_book = {
            'name': request_data['name'],
            'price': request_data['price'],
            'ISBN': ISBN
        }
        i = 0
        for book in books:
            currentISBN = book['ISBN']
            if currentISBN == new_book['ISBN']:
                books[i] = new_book
            i += 1
        response = Response('', 204, mimetype='application/json')
        return response
    else:
        invalidBookObjectErrorMessage = {
            'error': 'Invalid book object passed in request',
            'helpString': 'Data passed in should be similar to this {"name": "Green Eggs and Ham","price": 7.99}'
        }
        response = Response(json.dumps(
            invalidBookObjectErrorMessage), 400, mimetype='application/json')
        return response


# PATCH /books/<int:ISBN>
@app.route('/books/<int:ISBN>', methods=['PATCH'])
def patch_book(ISBN):
    request_data = request.get_json()
    updated_book = {}
    if is_patch_request_data_valid(request_data):
        if 'name' in request_data:
            updated_book['name'] = request_data['name']
        elif 'price' in request_data:
            updated_book['price'] = request_data['price']

        for book in books:
            if book['ISBN'] == ISBN:
                book.update(updated_book)
                break

        response = Response('', 204, mimetype='application/json')
        return response
    else:
        invalidBookObjectErrorMessage = {
            'error': 'Invalid book object passed in request',
            'helpString': 'Data passed in should be similar to this {"name": "Green Eggs Ham"} or {"price": 7.99}'
        }
        response = Response(json.dumps(
            invalidBookObjectErrorMessage), 400, mimetype='application/json')
        return response


# DELETE /books/<int:ISBN>
@app.route('/books/<int:ISBN>', methods=['DELETE'])
def delete_book_by_ISBN(ISBN):
    i = 0
    is_book_found_and_deleted = False
    for book in books:
        if book['ISBN'] == ISBN:
            books.pop(i)
            is_book_found_and_deleted = True
            break
        i += 1

    if is_book_found_and_deleted:
        response = Response('', 204, mimetype='application/json')
        return response
    else:
        invalidBookObjectErrorMessage = {
            'error': 'Book not found'
        }
        response = Response(json.dumps(
            invalidBookObjectErrorMessage), 404, mimetype='application/json')
        return response


app.run(port=5000)
