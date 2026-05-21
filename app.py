from flask import Flask, render_template, request, jsonify
from core_logic import organize_directory

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/organize', methods=['POST'])
def organize():
    directory_path = request.form.get('directory_path')
    if not directory_path:
        return jsonify({"status": "error", "message": "Please provide a path."})
    
    result = organize_directory(directory_path)
    return jsonify(result)

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
