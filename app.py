# app.py
from flask import Flask, jsonify, request
from functools import wraps
import jwt
from datetime import datetime, timedelta
from flask_restx import Api, Resource, fields
from config import config

app = Flask(__name__)

# Load configuration
try:
    config.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    exit(1)

# Initialize Flask-RESTX
api = Api(
    app,
    version=config.API_VERSION,
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    doc='/swagger/',
    authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'ApiKey'
        },
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
        }
    }
)

# User credentials (in production, use proper password hashing)
users = {
    config.ADMIN_USER: config.ADMIN_PASSWORD,
    "user": "mypassword"
}

# In-memory storage for books
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"id": 3, "title": "1984", "author": "George Orwell", "year": 1949}
]

# Define namespaces
auth_ns = api.namespace('auth', description='Authentication operations')
books_ns = api.namespace('books', description='Books operations')

# Models for Swagger documentation
login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username', example='admin'),
    'password': fields.String(required=True, description='Password', example='password123')
})

token_model = api.model('Token', {
    'access_token': fields.String(description='JWT access token'),
    'token_type': fields.String(description='Token type', example='bearer'),
    'expires_in': fields.Integer(description='Token expiration time in seconds', example=7200)
})

book_model = api.model('Book', {
    'id': fields.Integer(description='Book ID', example=1),
    'title': fields.String(required=True, description='Book title', example='The Great Gatsby'),
    'author': fields.String(required=True, description='Book author', example='F. Scott Fitzgerald'),
    'year': fields.Integer(required=True, description='Publication year', example=1925)
})

book_input_model = api.model('BookInput', {
    'title': fields.String(required=True, description='Book title', example='Dune'),
    'author': fields.String(required=True, description='Book author', example='Frank Herbert'),
    'year': fields.Integer(required=True, description='Publication year', example=1965)
})

books_response_model = api.model('BooksResponse', {
    'books': fields.List(fields.Nested(book_model), description='List of books')
})

book_created_model = api.model('BookCreated', {
    'message': fields.String(description='Success message', example='Book added successfully'),
    'book': fields.Nested(book_model, description='Created book')
})

error_model = api.model('Error', {
    'error': fields.String(description='Error message')
})

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for API key first
        api_key = request.headers.get('ApiKey')
        if api_key and api_key == config.API_KEY:
            return f(*args, **kwargs)

        # Check for Bearer token
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])
                request.current_user = payload['username']
                return f(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401

        return jsonify({'error': 'Authentication required. Provide either API-Key or Bearer token'}), 401
    return decorated_function

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Application is running'
    })

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from Jenkins Demo!'
    })

# Authentication endpoints
@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(token_model, code=200)
    @auth_ns.response(400, 'Validation error', error_model)
    @auth_ns.response(401, 'Invalid credentials', error_model)
    @auth_ns.doc('login', description='Login with username and password to get access token')
    def post(self):
        """Login to get access token"""
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            api.abort(400, 'Username and password required')

        username = data['username']
        password = data['password']

        if username not in users or users[username] != password:
            api.abort(401, 'Invalid credentials')

        # Generate JWT token with configurable expiration
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=config.JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm='HS256')

        return {
            'access_token': token,
            'token_type': 'bearer',
            'expires_in': config.JWT_EXPIRATION_HOURS * 3600
        }

# Books API endpoints with clear, readable routes
@books_ns.route('/get_books')
class GetBooks(Resource):
    @books_ns.marshal_with(books_response_model)
    @books_ns.response(401, 'Authentication required', error_model)
    @books_ns.doc('get_books', description='Get all books', security=['apikey', 'Bearer'])
    @require_auth
    def get(self):
        """Get all books"""
        return {'books': books}


@books_ns.route('/add_book')
class AddBook(Resource):
    @books_ns.expect(book_input_model)
    @books_ns.marshal_with(book_created_model, code=201)
    @books_ns.response(400, 'Validation error', error_model)
    @books_ns.response(401, 'Authentication required', error_model)
    @books_ns.doc('add_book', description='Add a new book', security=['apikey', 'Bearer'])
    @require_auth
    def post(self):
        """Add a new book"""
        data = request.get_json()

        if not data:
            api.abort(400, 'No JSON data provided')

        required_fields = ['title', 'author', 'year']
        for field in required_fields:
            if field not in data:
                api.abort(400, f'Missing required field: {field}')

        new_id = max([book['id'] for book in books]) + 1 if books else 1
        new_book = {
            'id': new_id,
            'title': data['title'],
            'author': data['author'],
            'year': data['year']
        }

        books.append(new_book)
        return {
            'message': 'Book added successfully',
            'book': new_book
        }, 201

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
