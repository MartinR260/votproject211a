from flask import Flask, request, make_response
from flask_cors import CORS
import requests

realm_id = "myrealm"
client_id = "backend"
client_secret = "6UegGiQgnZo3pcOyGh0azilWfY1z02Gv"

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def validate_token():
    data = request.json
    response = requests.post(f"http://localhost:8080/realms/{realm_id}/protocol/openid-connect/token/introspect", {"client_id": client_id, "client_secret": client_secret, "token": data["token"]}).json()
    return make_response(response, 200)

if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0", debug=True)