# Authentication System with JWT and Login Attempt Logs

This repository contains a secure authentication system built with Django and JSON Web Tokens (JWT), including logging for login attempts. It's designed for applications that require secure user authentication and tracking of access patterns to monitor unauthorized attempts.

## Features

- **JWT-Based Authentication**: Securely authenticate users with token-based authentication.
- **Email Verification**: Verify users' emails through a secure code-based system.
- **Login Attempt Logging**: Track and log every login attempt, successful or failed, for enhanced security monitoring.
- **Flexible Logging Database**: The database for logging is abstracted, allowing easy changes to the logging system/database (default is PostgreSQL).
- **Admin Access to Login Logs**: Admins can access logs of all login attempts.
- **RESTful API**: Well-defined endpoints for registration, login, email verification, token management, and login logs.

## Tech Stack

- **Backend**: Python / Django
- **Database**: PostgreSQL (default for user data), but logging can be easily switched to another database through an abstract class
- **JWT**: For secure token-based authentication using `djangorestframework-simplejwt`
- **Containerization**: Docker for easy deployment

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/theycallmereza/Auth-and-Log-Login-Attemp-Django.git
   cd Auth-and-Log-Login-Attemp-Django
2. **Create a `.env` file: Copy the contents of `env.sample` to a new `.env` file:**
   ```bash 
   cp env.sample .env
3. **Build and start the Docker containers:**
   ```bash 
   docker-compose up --build
4. **Apply migrations: Once the container is up, open a bash shell inside the Django container:**

   ```bash
   docker-compose exec auth_web bash
   cd auth
   python manage.py migrate
**Access the application: The project will be available at `http://localhost:8585`.**

## Usage

### User Registration and Email Verification

1. **Register**: Send a POST request to `/api/accounts/register/` with user details.

2. **Request Verification Code**: After registration, request a verification code via `/api/accounts/verification/code/`.

3. **Verify Email**: Submit the verification code to `/api/accounts/verification/code/verify/` to activate the account.

### Authentication

- **Login**: Authenticate users by sending a POST request to `/api/accounts/login/`.
- **Token Refresh**: Refresh tokens by sending a POST request to `/api/accounts/login/refresh/`.

### Admin Access to Login Logs

- **View Login Attempt Logs**: Admins can access login attempt logs by sending a GET request to `/api/accounts/logs/login/attemps/`, passing the access token as a Bearer token in the authorization header.

## Example Requests

```bash
# Register a new user
curl -X POST http://localhost:8585/api/accounts/register/ -d "username=newuser&password=newpass"

# Request email verification code
curl -X POST http://localhost:8585/api/accounts/verification/code/ -d "email=newuser@example.com"

# Verify email with code
curl -X POST http://localhost:8585/api/accounts/verification/code/verify/ -d "email=newuser@example.com&code=verification_code"

# Login as a user
curl -X POST http://localhost:8585/api/accounts/login/ -d "username=newuser&password=newpass"

# Refresh token
curl -X POST http://localhost:8585/api/accounts/login/refresh/ -d "refresh=your_refresh_token"

# Get login attempt logs (Admin only, with access token)
curl -X GET http://localhost:8585/api/accounts/logs/login/attemps/ -H "Authorization: Bearer your_access_token"
