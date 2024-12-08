from werkzeug.security import generate_password_hash, check_password_hash

# When creating a new account
hashed_password = generate_password_hash(password)
cursor.execute('INSERT INTO users (first_name, last_name, email, phone, username, password) VALUES (%s, %s, %s, %s, %s, %s)', 
               (first_name, last_name, email, phone, username, hashed_password))

# When logging in
cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
user = cursor.fetchone()
if user and check_password_hash(user['password'], password):
    # User authenticated
