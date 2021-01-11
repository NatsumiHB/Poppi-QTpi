import json


class Config:
    def __init__(self):
        config, store_items, profile_config = open("../config.json", "r"), \
                                              open("../store_items.json", "r"), \
                                              open("../profile_config.json", "r")
        self.config = {
            **json.loads(config.read()),
            **json.loads(profile_config.read()),
            "base_store_items": json.loads(store_items.read())
        }

        self.profile_restraints = self.config["profile_restraints"]
        self.empty_profile = self.config["empty_profile"]
        self.money_config = self.config["money_config"]
