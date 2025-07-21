import os
import hashlib


class SubscriberWorker:
    subs: list[int | str]

    def __init__(self):
        if not os.path.exists("../subscribers.txt"):
            with open("../subscribers.txt", "w") as file:
                pass

        with open("../subscribers.txt", "r") as file:
            self.subs = file.readlines()
        self.subs = list(map(int, self.subs))
        self.password_hash = hashlib.sha256(os.getenv("PASSWORD").encode()).hexdigest()


    def _save_file(self):
        with open("../subscribers.txt", "w") as file:
            for sub in self.subs:
                file.write(str(sub) + "\n")

    def add_sub(self, sub_id, password:str):
        password = password.strip()
        password = hashlib.sha256(password.encode()).hexdigest()
        if password != self.password_hash:
            raise PermissionError
        if sub_id in self.subs:
            raise ValueError()
        self.subs.append(sub_id)
        self._save_file()

    def del_sub(self, sub_id):
        if sub_id not in self.subs:
            raise ValueError()
        self.subs.remove(sub_id)
        self._save_file()

    def state(self, sub_id):
        return sub_id in self.subs
