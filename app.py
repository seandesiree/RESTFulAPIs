from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
ma = Marshmallow(app)

class MembersSchema():
    id = fields.String(required=True)
    name = fields.String(required=True)
    age = fields.String(required=True)

    class Meta:
        fields = ("id", "name", "age")

members_schema = MembersSchema()

def get_db_connection():
    db_name = {
    'user': 'root',
    'password': 'evangelista4ever',
    'host': 'localhost',
    'database': 'new_schema'
}
    try:
        conn = mysql.connector.connect(**db_name)
        print("Connected to MySQL database successfully")
        return conn
    except Error as e:
        print(f"Error: {e}")



@app.route('/members', methods=['POST'])
def add_member():
    member_data = members_schema.load(request.json)
    conn = get_db_connection()
    cursor = conn.cursor(dicionary = True)
    new_member = (member_data["id"], member_data["name"], member_data["age"])
    query = "INSERT INTO Members (id, name, age) VALUES (%s, %s, %s)"
    cursor.execute(query, (new_member))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "New Customer addedd successfully"}), 201
 


@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dicionary = True)
        query = "SELECT * FROM Members"
        cursor.execute(query)
        members = cursor.fetchall()
        return members_schema.jsonify(members)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


    
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        member_data = members_schema.load(request.json)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        update_member = (member_data["id"], member_data["name"], member_data["age"], id)
        query = "UPDATE Members SET id = %s, name = %s, age = %s"
        cursor.execute(query, update_member)
        conn.commit()
        return jsonify({"message": "New Customer addedd successfully"}), 201
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()
        member_to_remove = (id,)
        cursor.execute("SELECT * FROM Members WHERE id = %s", member_to_remove)
        member = cursor.fetchone()
        if not member:
            return jsonify({"error": "Member not found"}), 404
        query = "DELETE FROM Members WHERE id = %s"
        cursor.execute(query, member_to_remove)
        conn.commit()
        return jsonify({"message": "Member removed successfully"}), 200
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()



if __name__ =="__main__":
    app.run(debug = True)