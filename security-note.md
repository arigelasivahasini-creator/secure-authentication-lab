# Security Note – Secure Authentication Lab

## 1. Password Storage

Passwords are never stored as plain text.

The application uses Werkzeug password hashing with `generate_password_hash()` and verifies passwords using `check_password_hash()`.

This means the stored password value is a hash instead of the original password.

## 2. Server-Side Input Validation

The server validates username and password input before authentication.

The application checks that:

* Username and password are not empty.
* Username length does not exceed 50 characters.
* Password length does not exceed 128 characters.

Client-side validation alone is not trusted.

## 3. Generic Authentication Errors

The application returns the same message for incorrect usernames and incorrect passwords:

"Invalid username or password."

This helps prevent username enumeration.

## 4. Rate Limiting

The application limits failed login attempts.

A maximum of 5 failed attempts are allowed from the same IP address within 60 seconds.

After the limit is reached, login is temporarily blocked.

This helps reduce brute-force password attacks.

## 5. Secure Session Management

The application uses Flask sessions with the following protections:

* HttpOnly cookie enabled.
* SameSite set to Lax.
* Session lifetime set to 15 minutes.
* Session data is cleared before creating a new authenticated session.
* Logout clears the session.

These controls reduce the risk of session theft and session misuse.

## 6. Session Cookie Security

The `SESSION_COOKIE_SECURE` setting is disabled for this local HTTP demonstration.

In a production deployment using HTTPS, it should be set to `True` so the session cookie is sent only over HTTPS.

## 7. Secret Key

The Flask secret key is loaded from the `SECRET_KEY` environment variable when available.

A development-only fallback is used for this local demonstration.

Production applications should store the secret key securely and never expose it in source code.

## 8. Limitations

This project is a local educational demonstration.

The in-memory rate limiter is suitable for a small local demo but should be replaced with a shared solution such as Redis or a database-backed mechanism in a production or distributed application.

The demo account credentials are for testing only and must not be reused for real accounts.

## Conclusion

The authentication service demonstrates important security controls including password hashing, server-side validation, generic authentication errors, rate limiting, secure session configuration, logout handling, and session expiry.
