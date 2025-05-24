# source venv/bin/activate
# flask run --debug / flask run 


from flask import Flask, render_template, request

app = Flask(__name__)
import pandas as pd

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-table', methods=['POST'])
def submit_table():
    content = request.get_json()
    table_data = content.get('table', [])

    df = pd.DataFrame(table_data)

    print(df)

    return "Data received and processed into DataFrame"