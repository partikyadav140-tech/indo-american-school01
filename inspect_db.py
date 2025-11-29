import sqlite3
import os

DATABASE = os.path.join('data', 'app.db')

def inspect_contacts():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, phone, subject, message, created_at FROM contact;")
        contacts = cursor.fetchall()

        if contacts:
            print("--- Contact Messages ---")
            for contact in contacts:
                print(f"ID: {contact[0]}, Name: {contact[1]}, Email: {contact[2]}, Phone: {contact[3]}, Subject: {contact[4]}, Message: {contact[5]}, Created At: {contact[6]}")
        else:
            print("No contact messages found in the database.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    inspect_contacts()
