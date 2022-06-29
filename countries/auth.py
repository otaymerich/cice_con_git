
import json
from uuid import uuid4
from os import getcwd
from hashlib import sha1


        

CWD = getcwd()
file_path = f"{CWD}/users.json"

# def create_author(name, pwd):
#     user = {
#         "name": name,
#         "pwd": pwd
#     }
#     with open(f"{CWD}/users.json", "r+", encoding="utf8") as file:
#         file_data = json.load(file)
#         file_data["data"].append(user)
#         file.seek(0)
#         json.dump(file_data, file, indent = 4)

def read(file_path):
    file = open(file_path, encoding="utf8")
    data = json.load(file)
    file.close()
    return data

def write(file_path, data):
    file = open(file_path, mode="w")
    json.dump(data, file, indent=4, ensure_ascii=True)
    return True

def get_by_name(name, users):
    return next(filter(lambda user: user["name"] == name, users["data"]), False)

def get_by_id(id, users):
    return next(filter(lambda user: user["id"] == id, users["data"]), False)

def create_user(name, pwd):  
    users = read(file_path)
    uniq_user = get_by_name(name, users)
    if uniq_user:
        return False
    pwd = sha1(pwd.encode()).hexdigest()
    user = {
        "id":uuid4().hex,
        "name": name,
        "pwd": pwd
    }
    users["data"].append(user)
    write(file_path, users)
    return True

def is_authanticated(name, pwd):
    pwd = sha1(pwd.encode()).hexdigest()
    users = read(file_path)
    user = get_by_name(name, users)
    if user:
        if user["pwd"]==pwd:
            return True
    return False

def login():
    print("\n")
    print("Login".center(50, "-"))
    print("1. Login".center(50))
    print("2. Create account".center(50))
    print("Q. Exit".center(50))
    print("".center(50, "-"))



if __name__ == "__main__":
    #TESTING
    create_user("test_3", "12345")
    print(is_authanticated("test_3", "1235"))
