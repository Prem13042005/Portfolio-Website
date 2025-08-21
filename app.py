from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
# Database configuration

DB_CONFIG = {
    'host': 'localhost',
    'database': 'portfolio_db',
    'user': 'root',  
    'password': 'WJ28@krhps'   
}

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return connection

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling contact form submission
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    connection = create_connection()
    if connection is None:
        return jsonify({'success': False, 'message': 'Database connection failed'})

    try:
        cursor = connection.cursor()
        query = "INSERT INTO contacts (name, email, subject, message) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, subject, message))
        connection.commit()
        return jsonify({'success': True, 'message': 'Message sent successfully'})
    except Error as e:
        print(f"Error inserting data: {e}")
        return jsonify({'success': False, 'message': 'Failed to send message'})
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)