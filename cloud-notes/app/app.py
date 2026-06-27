from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route("/")
def home():
    try:
        conn = mysql.connector.connect(
            host="mysql",
            user="root",
            password="suryaa123",
            database="cloudlab"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT 'Database Connected Successfully!'")
        message = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return message

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
