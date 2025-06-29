# source venv/bin/activate
# flask run --debug / flask run 


from flask import Flask, render_template, request
from models.simulation import BlackjackSimulation

app = Flask(__name__)
import pandas as pd

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-table', methods=['POST'])
def submit_table():
    content = request.get_json()
    table_data = content.get('table', []) # using javascript to get strategy table

    strategy = pd.DataFrame(table_data) # Converting table to DataFrame
    strategy = strategy.set_index('label')
    print(strategy)
    print(strategy.loc['10', 'col6'])

    
    sim = BlackjackSimulation()
    sim.run_simulation(strategy)
   
    return "Data received and processed into DataFrame"