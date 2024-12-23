import shelve  
from typing import Any    
from pydantic import BaseModel


class PersistentSettings(BaseModel):       
    def __init__(self, **data: Any):  
        with shelve.open("config.db") as db:  
            super().__init__(**db.get("settings", default={}), **data)  
    def update(self):  
        with shelve.open("config.db") as db:   
            db["settings"] = self.dict()  

class BotConfig(PersistentSettings):  
    MODE: str = "Paper"  
    def parameter_block(self, st):  
        self.MODE = str(st.radio(  
            "Mode",  
            ["Paper", "Live"],  
            index=0,  
        ))  
    def ib_client_port(self):  
        if self.MODE == "Paper":  
            return 4002  
        elif self.MODE == "Live":  
            return 4001