from flask import Flask, request, make_response
from flask_cors import CORS
import requests
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from model import *

realm_id = "myrealm"
client_id = "backend"
client_secret = "6UegGiQgnZo3pcOyGh0azilWfY1z02Gv"
app = Flask(__name__)
CORS(app)

def create_db_engine():
    return create_engine(f"mariadb+pymysql://user:password@localhost:3307/database")

@app.route("/", methods=["GET", "POST"])
def validate_token():
    data = request.json
    response = requests.post(f"http://localhost:8080/realms/{realm_id}/protocol/openid-connect/token/introspect", {"client_id": client_id, "client_secret": client_secret, "token": data["token"]}).json()
    return make_response(response, 200)

@app.route("/submit_score", methods=["POST"])
def submit_score():
    data = request.json
    response = requests.post(f"http://localhost:8080/realms/{realm_id}/protocol/openid-connect/token/introspect", {"client_id": client_id, "client_secret": client_secret, "token": data["token"]}).json()
    if response["active"] == False:
        return make_response({"message": "This token is not active"}, 401)

    current_leadervoard_item = Leaderboard(response["sub"], response["name"], data["score"])

    engine = create_db_engine()

    with Session(engine) as session:
        previous_leaderboard_item = session.scalar(select(Leaderboard).where(Leaderboard.user_id == response["sub"]))
        if previous_leaderboard_item is None:
            session.add(current_leadervoard_item)
        elif previous_leaderboard_item.best_score < current_leadervoard_item.best_score:
            previous_leaderboard_item.best_score = current_leadervoard_item.best_score
            previous_leaderboard_item.date_time = current_leadervoard_item.date_time
            previous_leaderboard_item.name = current_leadervoard_item.name
        session.commit()
    return make_response({"message": "Score was added successfully"}, 200)

@app.route("/leaderboard/<string:token>", methods=["GET"])
def load_leaderboard(token):
    response = requests.post(f"http://localhost:8080/realms/{realm_id}/protocol/openid-connect/token/introspect", {"client_id": client_id, "client_secret": client_secret, "token": token}).json()
    if response["active"] == False:
        return make_response({"message": "This token is not active"}, 401)

    engine = create_db_engine()

    with Session(engine) as session:
        leaderboard_items = session.scalars(select(Leaderboard).order_by(Leaderboard.best_score.desc()))
        result = []
        for score in leaderboard_items:
            if score.user_id == response["sub"]:
                result.append({"name": f"You ({score.name})", "score": score.best_score, "datetime": score.date_time})
            else:
                result.append({"name": score.name, "score": score.best_score, "datetime": score.date_time})
        session.commit()
    return make_response({"message": "Leaderboard was loaded successfully", "leaderboard": result}, 200)

Base.metadata.create_all(create_db_engine())

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)