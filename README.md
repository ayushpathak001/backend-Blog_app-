# Blog API 🚀

A RESTful Blog API built with **FastAPI** and **MongoDB**.

This project provides user authentication, blog post management, password reset functionality, and protected API endpoints using JWT authentication.

---

## ✨ Features

* User registration
* User login
* JWT-based authentication
* Protected API routes
* Create blog posts
* Get all blog posts
* Get a single blog post
* Update blog posts
* Delete blog posts
* Author ownership validation
* MongoDB database integration
* Password reset through email
* Pydantic request/response validation
* Automatic API documentation with Swagger UI

---

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **MongoDB**
* **Motor** - Async MongoDB driver
* **Pydantic**
* **JWT**
* **Passlib / bcrypt**
* **FastAPI-Mail**
* **Uvicorn**

---

## 📁 Project Structure

```text
API/
│
├── routes/
│   ├── auth.py
│   ├── users.py
│   ├── password_reset.py
│   └── blog_content.py
│
├── templates/
│   ├── email.html
│   └── password_reset.html
│
├── main.py
├── oauth2.py
├── schemas.py
├── utils.py
├── send_email.py
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd API
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```env
MONGO_URI=your_mongodb_connection_string

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

MAIL_USERNAME=your_email
MAIL_PASSWORD=your_email_password
MAIL_FROM=your_email
MAIL_PORT=587
MAIL_SERVER=your_smtp_server
MAIL_FROM_NAME=Your Blog API
```

### Important

Never commit your `.env` file to GitHub.

Add it to `.gitignore`:

```text
.env
venv/
__pycache__/
```

---

## ▶️ Running the Application

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The API will normally run at:

```text
http://127.0.0.1:8000
```

---

## 📚 API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

### ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

Swagger UI can be used to test the API directly from the browser.

---

# 🔑 Authentication

The API uses JWT-based authentication.

Some endpoints require a valid access token.

After logging in, copy the returned access token and use it in Swagger's **Authorize** button.

The token should be sent as:

```text
Bearer <access_token>
```

---

# 👤 Authentication APIs

## Register User

### Endpoint

```http
POST /registration
```

### Example Request

```json
{
    "name": "Ayush",
    "email": "ayush@example.com",
    "password": "your_password"
}
```

This creates a new user in MongoDB.

---

## Login

### Endpoint

```http
POST /login
```

### Example Request

```text
username: Ayush
password: your_password
```

A successful login returns an access token.

Example:

```json
{
    "access_token": "your_jwt_token",
    "token_type": "bearer"
}
```

Use this token to access protected endpoints.

---

# 📝 Blog APIs

The blog API provides complete CRUD functionality.

CRUD means:

* **Create** → POST
* **Read** → GET
* **Update** → PUT
* **Delete** → DELETE

---

## 1. Create Blog Post

### Endpoint

```http
POST /blog
```

### Authentication

Required.

### Example Request

```json
{
    "title": "My First Blog",
    "body": "This is my first blog post."
}
```

The authenticated user's information is automatically added to the blog post.

The stored document contains information such as:

```json
{
    "_id": "MongoDB ObjectId",
    "title": "My First Blog",
    "body": "This is my first blog post.",
    "author_name": "Ayush",
    "author_id": "user_id",
    "created_at": "2026-09-25 07:14:18"
}
```

---

# 📖 Read Blog Posts

## Get All Blog Posts

### Endpoint

```http
GET /blog
```

### Optional Parameters

You can limit the number of posts:

```http
GET /blog?limit=5
```

You can also specify the field used for sorting:

```http
GET /blog?limit=5&orderby=created_at
```

The API returns a list of blog posts.

---

## Get a Single Blog Post

### Endpoint

```http
GET /blog/{id}
```

Example:

```http
GET /blog/6ab61f4a735521a42b49361b
```

The `{id}` must be the MongoDB `_id` of the blog post.

Example response:

```json
{
    "_id": "6ab61f4a735521a42b49361b",
    "title": "My First Blog",
    "body": "This is my first blog post.",
    "author_name": "Ayush",
    "author_id": "6ab0dad3f9e20ffc9235c3b5",
    "created_at": "2026-09-25 07:14:18"
}
```

---

# ✏️ Update Blog Post

### Endpoint

```http
PUT /blog/{id}
```

### Authentication

Required.

### Example

```http
PUT /blog/6ab61f4a735521a42b49361b
```

### Request Body

```json
{
    "title": "Updated Blog Title",
    "body": "Updated blog content."
}
```

Only the author of the blog post can update it.

The API checks the authenticated user's ID against the `author_id` stored in the blog post.

MongoDB's `_id` is converted from the URL string into an `ObjectId` before querying the database.

---

# 🗑️ Delete Blog Post

### Endpoint

```http
DELETE /blog/{id}
```

### Authentication

Required.

Example:

```http
DELETE /blog/6ab61f4a735521a42b49361b
```

Only the author of the blog post can delete it.

After successful deletion, the API returns:

```http
204 No Content
```

A `204` response intentionally does not contain a response body.

---

# 🔒 Author Authorization

Blog update and delete operations are protected.

Before modifying or deleting a blog post, the API checks:

```text
blog.author_id == current_user._id
```

Because `author_id` is stored as a string, the authenticated user's MongoDB ID is converted to a string:

```python
str(current_user["_id"])
```

This prevents one user from modifying or deleting another user's blog post.

---

# 🔄 Blog CRUD Overview

| Method | Endpoint     | Authentication | Purpose       |
| ------ | ------------ | -------------- | ------------- |
| POST   | `/blog`      | ✅              | Create blog   |
| GET    | `/blog`      | ❌              | Get all blogs |
| GET    | `/blog/{id}` | ❌              | Get one blog  |
| PUT    | `/blog/{id}` | ✅              | Update blog   |
| DELETE | `/blog/{id}` | ✅              | Delete blog   |

---

# 🔑 Password Reset

The project also contains a password reset system.

## Request Password Reset

```http
POST /password
```

The user provides their email address.

If the email exists, the application generates a reset token and sends a password reset email.

---

## Reset Password

The reset link contains a JWT reset token.

The token is verified before allowing the user to set a new password.

Example request body:

```json
{
    "password": "new_password"
}
```

The password reset system includes:

* Reset token generation
* Token expiration
* JWT validation
* Email delivery
* New password submission
* User lookup from the reset token

---

# 🗄️ MongoDB

The application uses MongoDB as its database.

The blog posts are stored in the:

```text
blogPost
```

collection.

A blog document contains fields such as:

```json
{
    "_id": "ObjectId",
    "title": "Blog title",
    "body": "Blog content",
    "author_name": "Ayush",
    "author_id": "user_id",
    "created_at": "timestamp"
}
```

---

# 🆔 MongoDB ObjectId

MongoDB automatically generates an `ObjectId` for every document.

For example:

```text
6ab61f4a735521a42b49361b
```

FastAPI receives URL parameters as strings.

Therefore, when querying MongoDB by `_id`, the string needs to be converted into an `ObjectId`:

```python
blog_id = ObjectId(id)
```

Then it can be used:

```python
await db["blogPost"].find_one({
    "_id": blog_id
})
```

This conversion is used for operations such as:

* Get one blog
* Update blog
* Delete blog

---

# 🧪 Testing the API

The easiest way to test the API is through Swagger UI.

Start the server:

```bash
uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Recommended testing order:

```text
1. Register
      ↓
2. Login
      ↓
3. Copy access token
      ↓
4. Authorize in Swagger
      ↓
5. Create blog
      ↓
6. Get blogs
      ↓
7. Get single blog
      ↓
8. Update blog
      ↓
9. Delete blog
```

---

# ⚠️ Common Errors

## 401 Unauthorized

Usually means authentication is missing or invalid.

Make sure you provide:

```text
Authorization: Bearer <token>
```

---

## 404 Blog Not Found

Make sure you are using the blog's `_id`, not the user's `author_id`.

For example:

```text
Blog ID:
6ab61f4a735521a42b49361b
```

is different from:

```text
Author ID:
6ab0dad3f9e20ffc9235c3b5
```

---

## Invalid ObjectId

If the supplied blog ID is not a valid MongoDB ObjectId, the API should return a `400 Bad Request`.

---

## 500 Internal Server Error

Check the Uvicorn terminal for the actual exception.

Run:

```bash
uvicorn main:app --reload
```

and inspect the terminal output when the request fails.

---

# 📦 Requirements

Typical dependencies used by this project include:

```text
fastapi
uvicorn
motor
pymongo
pydantic
python-dotenv
python-jose
passlib
bcrypt
fastapi-mail
```

Install them using:

```bash
pip install -r requirements.txt
```

---

# 🔐 Security Notes

* Never commit `.env` to GitHub.
* Never expose your MongoDB connection string.
* Never expose your JWT secret key.
* Use strong passwords.
* Use HTTPS when deploying the application.
* Validate user input before storing it.
* Keep authentication tokens secure.

---

# 🚀 Future Improvements

Possible improvements for the project:

* Add pagination
* Add blog categories
* Add tags
* Add comments
* Add likes
* Add search functionality
* Add image uploads
* Add refresh tokens
* Add role-based authorization
* Add automated tests
* Add Docker support
* Deploy the API to a cloud platform
* Add frontend using React or another frontend framework

---

# 👨‍💻 Author

**Ayush Pathak**

Built as a learning project to understand:

* FastAPI
* REST APIs
* MongoDB
* JWT authentication
* CRUD operations
* Pydantic validation
* Async Python
* Email-based password reset
* API security

---

## 📄 License

This project is created for learning and development purposes.
