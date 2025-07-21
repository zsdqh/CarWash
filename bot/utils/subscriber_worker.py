import json
import os


class JsonWorker:
    def __init__(self):
        if not os.path.exists("../subscribers.json"):
            with open("../subscribers.json", "w") as file:
                json.dump(dict(), file)
        with open("../subscribers.json", "r") as file:
            self.subs = json.load(file)
        print(self.subs)

a = JsonWorker()
