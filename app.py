from flask import Flask, request, jsonify
from image_captioning import generate_captions

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Image Captioning API"})

@app.route('/captions', methods=['POST'])
def generate():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    captions = generate_captions(url)
    return jsonify({"captions": captions})

if __name__ == '__main__':
    app.run(debug=True)
