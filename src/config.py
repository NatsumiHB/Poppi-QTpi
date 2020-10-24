import json


class Config:
    def __init__(self):
        with open("../config.json", "r") as config:
            self.config = json.loads(config.read())
        self.profile_restraints = self.config["profile_restraints"]
        self.empty_profile = self.config["empty_profile"]
        self.money_config = self.config["money_config"]
