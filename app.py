from flask import Flask, jsonify, request
from pydantic import BaseModel
from database import Database
from typing import Optional

app = Flask(__name__)

class User(BaseModel):
    id: str
    name: str
    age: Optional[str]
    profession: str
    email: str

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Pong!"})

@app.route("/users", methods=["GET"])
def get_users():
    users = Database.select_all()

    if len(users) == 0:
        return jsonify({"message": "No users", "users": users})
    return jsonify({"message": "Available users", "users": users})

@app.route("/users/<string:user_id>")
def get_user(user_id: str):
    user = Database.select(user_id)
    if len(user) == 0:
        return jsonify({"message": "User not found", "user": user})
    return jsonify({"message": "User found", "user": user})

@app.route("/users", methods=["POST"])
def create_user():
    # print(f"{request} -> {type(request)} (type)")
    # print(request.method)
    # print(request.json)
    user = User(
        id=request.json.get("id", "Unknown"),
        name=request.json.get("name", "Unknown"),
        age=request.json.get("age", "Unknown"),
        profession=request.json.get("profession", "Unknown"),
        email=request.json.get("email", "Unknown"),
    )
    users = Database.select_all()
    users.append(dict(user))
    Database.insert(users)

    confirmed_user = Database.confirm_last_save()

    return jsonify({
        "message": "User created successfully",
        "user": confirmed_user
    })

@app.route("/users/<string:user_id>", methods=["PUT"])
def update_user(user_id: str):
    users = Database.select_all()

    for index, user in enumerate(users):
        if user["id"] == user_id:
            users[index]["id"] = request.json.get("id", user["id"])
            users[index]["name"] = request.json.get("name", user["name"])
            users[index]["age"] = request.json.get("age", user["age"])
            users[index]["profession"] = request.json.get("profession", user["profession"])
            users[index]["email"] = request.json.get("email", user["email"])

            Database.insert(users)
            modified_user = Database.select(user_id)

            return jsonify({
                "message": "Recently updated user",
                "user": modified_user
            })
    return jsonify({"message": "User not found", "user": []})

@app.route("/users/<string:user_id>", methods=["DELETE"])
def delete_user(user_id: str):
    users = Database.select_all()
    user = [user for user in users if user["id"] == user_id]

    if len(user) == 0:
        return jsonify({"message": "User not found", "user": []})
    
    users.remove(user[0]) # Becuase "user" contains [{found object}]
    Database.insert(users)

    return jsonify({
        "message": "Recently deleted user",
        "user": user[0]
    })

if __name__ == "__main__":
    app.run(debug=True, port=4000) # To see changes
