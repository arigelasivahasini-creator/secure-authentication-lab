# Secure Authentication Lab

A beginner-friendly cybersecurity project demonstrating secure authentication practices using Flask and Python.

## Features

- Password hashing using Werkzeug
- Server-side input validation
- Generic authentication error messages
- Login rate limiting
- Secure session configuration
- 15-minute session expiry
- Logout and session clearing
- Automated security tests

## Technologies Used

- Python 3.11
- Flask
- Werkzeug
- Pytest

## Security Controls

### Password Hashing
Passwords are stored as secure hashes instead of plain text.

### Input Validation
The server validates username and password length and checks for empty input.

### Generic Authentication Errors
The application uses the same error message for invalid usernames and passwords.

### Rate Limiting
Login attempts are limited to 5 failed attempts per IP address within 60 seconds.

### Secure Sessions
Session cookies use:

- HttpOnly
- SameSite=Lax
- 15-minute session lifetime

### Logout
The session is completely cleared when the user logs out.

## Project Structure

```text
secure-authentication-lab/
│
├── app.py
├── test_auth.py
├── security-note.md
├── requirements.txt
├── .gitignore
└── README.md