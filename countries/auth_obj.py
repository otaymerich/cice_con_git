import json
from typing import Tuple
from uuid import uuid4
from os import getcwd
from hashlib import sha1

CWD = getcwd()

class Auth():
    def __init__(self, file_path: str):
        self.file_path = file_path

    @property
    def users(self) -> dict:
        file = open(self.file_path, encoding="utf8")
        data = json.load(file)
        file.close()
        return data
    
    def write(self, data: dict) -> bool:
        file = open(self.file_path, mode="w")
        json.dump(data, file, indent=4, ensure_ascii=True)
        return True
    
    def get_by_name(self, name: str) -> Tuple[dict, bool]:
        return next(filter(lambda user: user["name"] == name, self.users["data"]),False)

    def get_by_id(self, id: str):
        return next(filter(lambda user: user["id"] == id, self.users["data"]),False)
    
    def create_user(self, name: str, pwd: str) -> bool:  
        uniq_user = self.get_by_name(name)
        if uniq_user:
            return False
        pwd = sha1(pwd.encode()).hexdigest()
        user = {
            "id":uuid4().hex,
            "name": name,
            "pwd": pwd
        }
        users_list = self.users
        users_list["data"].append(user)
        self.write(users_list)
        return True
    
    def is_authanticated(self, name: str, pwd: str) -> bool:
        pwd = sha1(pwd.encode()).hexdigest()
        user = self.get_by_name(name)
        if user:
            if user["pwd"]==pwd:
                return True
        return False
        
if __name__ == "__main__":
    test_1 = Auth(f"{CWD}/users.json")
    test_1.create_user("test_11", "12345")