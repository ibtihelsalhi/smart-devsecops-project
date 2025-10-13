from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import secrets
import datetime

app = Flask(__name__)

# VULNERABILITY: Hardcoded secret key for secret scanning tools
#app.secret_key = "super_secret_key_12345_DO_NOT_COMMIT"



# In-memory user database (simulating SQL database)
users_db = {
    "admin": {
        "password": "admin123",
        "name": "Administrateur",
        "account_number": "FR7612345678901234567890123",
        "balance": 50000.00,
        "transactions": [
            {"date": "2024-01-15", "description": "Salaire", "amount": 3000.00},
            {"date": "2024-01-10", "description": "Loyer", "amount": -1200.00},
            {"date": "2024-01-05", "description": "Courses", "amount": -150.00}
        ]
    },
    "user1": {
        "password": "password123",
        "name": "Jean Dupont",
        "account_number": "FR7698765432109876543210987",
        "balance": 15000.00,
        "transactions": [
            {"date": "2024-01-12", "description": "Virement reçu", "amount": 500.00},
            {"date": "2024-01-08", "description": "Restaurant", "amount": -45.00}
        ]
    },
    "user2": {
        "password": "test123",
        "name": "Marie Martin",
        "account_number": "FR7611223344556677889900112",
        "balance": 8500.00,
        "transactions": [
            {"date": "2024-01-14", "description": "Achat en ligne", "amount": -89.99}
        ]
    }
}

def log_security_event(event_type, details):
    """Log security events to console for monitoring"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[SECURITY] {timestamp} - {event_type}: {details}")

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Log login attempt
        log_security_event("LOGIN_ATTEMPT", f"User: {username}")
        
        # VULNERABILITY: SQL Injection simulation
        # In a real app, this would be: SELECT * FROM users WHERE username='...' AND password='...'
        # Simulating SQL injection: username = admin' OR '1'='1' -- will bypass authentication
        
        if "' OR '1'='1" in username or "' OR '1'='1" in password:
            # SQL injection successful
            log_security_event("SQL_INJECTION_DETECTED", f"Injection attempt with username: {username}")
            session['username'] = 'admin'  # Grant admin access
            session['user_data'] = users_db['admin']
            return redirect(url_for('dashboard'))
        
        # Normal authentication
        if username in users_db and users_db[username]['password'] == password:
            session['username'] = username
            session['user_data'] = users_db[username]
            log_security_event("LOGIN_SUCCESS", f"User: {username}")
            return redirect(url_for('dashboard'))
        else:
            log_security_event("LOGIN_FAILED", f"Invalid credentials for user: {username}")
            return render_template('login.html', error="Identifiants invalides")
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_data = session.get('user_data', {})
    return render_template('dashboard.html', user=user_data, username=session['username'])

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        recipient = request.form.get('recipient', '')
        amount = request.form.get('amount', '')
        
        try:
            amount = float(amount)
            user_data = session.get('user_data', {})
            
            log_security_event("TRANSFER_ATTEMPT", f"From: {session['username']}, To: {recipient}, Amount: {amount}")
            
            if amount <= 0:
                return render_template('transfer.html', error="Le montant doit être positif")
            
            if amount > user_data['balance']:
                log_security_event("TRANSFER_FAILED", "Insufficient funds")
                return render_template('transfer.html', error="Solde insuffisant")
            
            if recipient not in users_db:
                return render_template('transfer.html', error="Destinataire introuvable")
            
            # Perform transfer
            users_db[session['username']]['balance'] -= amount
            users_db[recipient]['balance'] += amount
            
            # Add transactions
            users_db[session['username']]['transactions'].insert(0, {
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "description": f"Virement vers {users_db[recipient]['name']}",
                "amount": -amount
            })
            
            users_db[recipient]['transactions'].insert(0, {
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "description": f"Virement de {user_data['name']}",
                "amount": amount
            })
            
            # Update session
            session['user_data'] = users_db[session['username']]
            
            log_security_event("TRANSFER_SUCCESS", f"Transfer completed: {amount}€ to {recipient}")
            
            return render_template('transfer.html', success=f"Virement de {amount}€ effectué avec succès")
        
        except ValueError:
            return render_template('transfer.html', error="Montant invalide")
    
    return render_template('transfer.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_data = session.get('user_data', {})
    return render_template('profile.html', user=user_data, username=session['username'])

@app.route('/logout')
def logout():
    username = session.get('username', 'Unknown')
    log_security_event("LOGOUT", f"User: {username}")
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("=" * 60)
    print("VULNERABLE BANKING APPLICATION - FOR TESTING ONLY")
    print("=" * 60)
    print(f"Hardcoded Secrets Present:")
    print(f"  - Secret Key: {app.secret_key}")
    print(f"  - API Key: {API_KEY}")
    print(f"  - DB Password: {DATABASE_PASSWORD}")
    print("=" * 60)
    print("SQL Injection Test:")
    print("  Username: admin' OR '1'='1' --")
    print("  Password: anything")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)