from flask import Flask, jsonify, render_template_string
import psycopg2

app = Flask(__name__)

# Database configuration

DATABASE = "hw3"
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST
        )
        return conn
    except psycopg2.Error as e:
        return str(e)

@app.route('/api/update_basket_a')
def update_basket_a():
    conn = get_db_connection()
    if isinstance(conn, str):  # If connection error
        return conn

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry')")
        conn.commit()
        return "Success!"
    except psycopg2.Error as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/api/unique')
def unique_fruits():
    conn = get_db_connection()
    if isinstance(conn, str):  # If connection error
        return conn

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT fruit_a FROM basket_a")
        unique_a = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT fruit_b FROM basket_b")
        unique_b = [row[0] for row in cursor.fetchall()]

        html = """
        <table border="1">
            <tr><th>Unique Fruits in basket_a</th><th>Unique Fruits in basket_b</th></tr>
            <tr>
                <td>{{ unique_a }}</td>
                <td>{{ unique_b }}</td>
            </tr>
        </table>
        """
        return render_template_string(html, unique_a=unique_a, unique_b=unique_b)
    except psycopg2.Error as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
