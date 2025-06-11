import pandas as pd



class Sim:
    def __init__(self, strategy: pd.DataFrame):
        self.strategy = strategy
        self.strategy = strategy.set_index("label")

    def run(self):
        print("Sim is running...")
       
        print(self.strategy.loc["A,9"])
