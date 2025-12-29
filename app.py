from flask import Flask, request, render_template
import toon
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", toon_text="", json_text="")

@app.route('/toon-to-json', methods=['POST'])
def toon_to_json_conversion():
    toon_text = request.form.get('toon_text', '')
    json_text = ''
    try:
        if toon_text.strip():
            data = toon.loads(toon_text)
            json_text = json.dumps(data, indent=2, ensure_ascii=False)
    except Exception as e:
        json_text = f"An error occurred: {e}"
    return render_template("index.html", toon_text=toon_text, json_text=json_text)

@app.route('/json-to-toon', methods=['POST'])
def json_to_toon_conversion():
    json_text = request.form.get('json_text', '')
    toon_text = ''
    try:
        if json_text.strip():
            data = json.loads(json_text)
            toon_text = toon.dumps(data)
    except Exception as e:
        toon_text = f"An error occurred: {e}"
    return render_template("index.html", toon_text=toon_text, json_text=json_text)

if __name__ == '__main__':
    app.run(debug=True)