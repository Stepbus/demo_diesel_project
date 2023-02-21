import os
from datetime import datetime

import pytz
from pymongo import MongoClient

MONGO_URL_CONNECTION_STR = os.environ.get('MONGO_URL_CONNECTION_STR')


class DAOMongo:

    def __init__(self):
        self.client = MongoClient(MONGO_URL_CONNECTION_STR)
        self.my_db = self.client["diesel_project"]
        self.collection_petro = self.my_db["petro"]
        self.collection_loves = self.my_db["loves"]
        self.collection_pilot = self.my_db["pilot"]

    def recording_data(self, obj: dict, name: str):
        if name == "petro":
            self._update(obj, self.collection_petro)
        elif name == "loves":
            self._update(obj, self.collection_loves)
        elif name == "pilot":
            self._update(obj, self.collection_pilot)

    def _update(self, obj: dict, collection):
        filter_ = {"name": obj.get("name"), 'address': obj.get("address")}
        if collection.find_one(filter_):
            kyiv_tz = pytz.timezone("Europe/Kyiv")
            time_in_kyiv = datetime.now(kyiv_tz)
            new_values = {
                "diesel": obj.get("diesel"),
                "updated": time_in_kyiv}  # .strftime("%d/%m/%Y %H:%M:%S")}
            collection.update_one(filter_, {'$set': new_values})
        else:
            self._save(obj, collection)

    @staticmethod
    def _save(obj: dict, collection):
        result = collection.insert_one(obj)
