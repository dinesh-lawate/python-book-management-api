from flask import Flask, jsonify, request, Response, json
from bookModel import *
from settings import *


def is_post_request_data_valid(bookObject):
    if('name' in bookObject and 'price' in bookObject and 'ISBN' in bookObject):
        return True
    else:
        return False


def is_put_request_data_valid(bookObject):
    if('name' in bookObject and 'price' in bookObject):
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
    return jsonify({'books': Book.get_all_books()})

# GET /books/<int:ISBN>
@app.route('/books/<int:ISBN>')
def get_book_by_ISBN(ISBN):
    return_value = Book.get_book(ISBN)
    if return_value is None:
        invalidBookObjectErrorMessage = {
            'error': 'Book not found'
        }
        response = Response(json.dumps(
            invalidBookObjectErrorMessage), 400, mimetype='application/json')
        return response
    return jsonify(return_value)

# POST /books
@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(is_post_request_data_valid(request_data)):
        Book.add_book(request_data['name'],
                      request_data['price'], request_data['ISBN'])
        response = Response('', 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(request_data['ISBN'])
    else:
        invalidBookObjectErrorMessage = {
            'error': 'Invalid book object passed in request',
            'helpString': 'Data passed in should be similar to this {"name": "Green Eggs and Ham","price": 7.99,"ISBN": 9811223344}'
        }
        response = Response(json.dumps(
            invalidBookObjectErrorMessage), 400, mimetype='application/json')
    return response

# PUT /books/<int:ISBN>
@app.route('/books/<int:ISBN>', methods=['PUT'])
def update_book(ISBN):
    request_data = request.get_json()
    if(is_put_request_data_valid(request_data)):
        Book.replace_book(ISBN, request_data['name'], request_data['price'])
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
    if(is_patch_request_data_valid(request_data)):
        if 'name' in request_data:
            Book.update_book_name(ISBN, request_data['name'])
        elif 'price' in request_data:
            Book.update_book_name(ISBN, request_data['price'])

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
    is_book_found_and_deleted = False
    if Book.get_book(ISBN) is not None:
        Book.delete_book(ISBN)
        is_book_found_and_deleted = True

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
