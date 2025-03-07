from flask import Flask, request, jsonify
from image_captioning import generate_captions

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Image Captioning API. Please send a POST request to /captions with url as raw json format to get captions"})

@app.route('/captions', methods=['GET', 'POST'])
def generate():
    if request.method == 'GET':
        return jsonify({"message": "Please make a POST request to /captions"}), 405
    
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    captions = generate_captions(url)
    return jsonify({"captions": captions})

if __name__ == '__main__':
    app.run(debug=True)
