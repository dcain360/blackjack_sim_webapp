# source venv/bin/activate
# flask run --debug / flask run 


from flask import Flask, render_template, request
from models.Player import Player

app = Flask(__name__)
import pandas as pd

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-table', methods=['POST'])
def submit_table():
    content = request.get_json()
    table_data = content.get('table', [])
    
    
    player_strategy = pd.DataFrame(table_data)
    player = Player("Hermann")
    player.print()
    print(player_strategy)

    return "Data received and processed into DataFrame"