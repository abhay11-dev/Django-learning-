from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/send", methods=["POST"])
def send():

    data = request.json

    return jsonify({
        "status": "payment_success",
        "data": data
    })

if __name__ == "__main__":
    app.run(port=8003)
