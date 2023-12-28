import os
import json
from typing import Dict

class Database:

    @classmethod
    def select_all(cls):
        # Does the database exist? If not, create it
        if not os.path.isfile('user_table.json'):
            with open('user_table.json', 'w') as f:
                # Inserting an empty array
                json.dump([], f)
        
        # If the file was found
        with open('user_table.json', 'r') as f:
            data = json.load(f)
        return data
    
    @classmethod
    def insert(cls, data: Dict):
        with open('user_table.json', 'w') as f:
            json.dump(data, f)

    @classmethod
    def confirm_last_save(cls):
        with open('user_table.json', 'r') as f:
            data = json.load(f)
        return data[-1]
    
    @classmethod
    def select(cls, id: str):
        with open('user_table.json', 'r') as f:
            data = json.load(f)

        for d in data:
            if d["id"] == id:
                return d
        
        return []
