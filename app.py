# source venv/bin/activate
# flask run --debug / flask run 


from flask import Flask, render_template, request

app = Flask(__name__)
import pandas as pd

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(data)
    with open('output.txt', 'w') as f:
        for key, value in data.items():
            f.write(f'{key}: {value}\n')

    return 'Data saved successfully!'