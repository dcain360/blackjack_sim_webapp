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
    
    df = pd.DataFrame([data])

    print(df)
    return 'Data saved successfully!'