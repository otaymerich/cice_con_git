from os import mkdir, getcwd, stat, system
from types import NoneType
from typing import Any
import requests as req
import random
from typing import Union, Tuple

CWD = getcwd()
url = "https://restcountries.com/v3.1"

#coje todos los paises
def get_all() -> Tuple[list, str]: 
    res = req.get(url + "/all").json()
    return res, url
print(type(get_all()))
input()

'''
FRONT
'''
#limpiamos terminal manteniendo menu
def clear(): 
    system("clear")
    menu()

#imprime menu
def menu():
    print("\n")
    print("Countires".center(50, "-"))
    print("1. Serch country".center(50))
    print("2. Play a game".center(50))
    print("Q. Exit".center(50))
    print("".center(50, "-"))

#impresion de busqueda de pais
def info(data: dict, country: str) -> bool: 
    if data == None:  #si no encontramos pais buscamos posibles similitudes
        if len(guess(country)) > 0: 
            aprox = guess(country)
            if aprox != "Not found":
                print(f"Maybe you mean: {guess(country)}\n")
            else:
                print("Couldn't find it")
        return False
    else:
        print(f"\n{name(data)}\n") #si encontramos pais imprimimos informacion
        return True

#listamos los continentes
def continent_choises(regions):
    for k, cont in enumerate(regions,start=1):
        print(f'''{k}: {cont}''')

#imprimimos pregunta, posibles respuestas y evaluamos la respuesta que da el usuario. Devolvemos puntuación
def questions(question: str, answers: list, correct_answer: str) -> int:
    print(question) #imprimimos pregunta
    for k, ans in enumerate(answers, start=1): #imprimimos posibles respuestas
        print(f'''{k}. {ans}''')
    player_guess = input("Answer: ")
    if player_guess.isnumeric(): #evaluamos respuesta usuario
        if int(player_guess) in range(1,5):
            if answers[int(player_guess)-1] == correct_answer:
                print("\nCorrect answer\n")
                return 2
            else:
                print(f"\nIncorrect answer, the correct answer was {correct_answer}.\n")
                return 0
        else:
            print("\nThe answer is not valid, therefore you got 0 points in this question\n")
            return 0
    else:
        print("\nThe answer is not valid, therefore you got 0 points in this question\n")
        return 0

#damos puntuación
def result(points: int):
    if points >= 5:
        print(f"Congrats you got {points}/10.")
    else:
        print(f"Dummy, you got {points}/10.")



'''
BACK
'''
#Checks if the country exists, returns the country dic if yes or None if not
def exist_country(country: str) -> Union[dict, NoneType]:
    try:
        data = req.get(f"{url}/name/{country}?fullText=true").json()[0]
        return data
    except KeyError:
        return None

#When the country is not found tries to make an educated guess of the country the user meant (not working so good yet)
def guess(country: str) -> str:
    maybe = []
    for data in get_all()[0]:
        letter = 0
        letter_position = 0
        for k, s in enumerate(data["name"]["common"]):
            if k == len(country):
                break
            if s in country:
                letter += 1
            if country[k] == s:
                letter_position += 1
            if letter_position > len(data["name"]["common"])-2:
                return data["name"]["common"]
        if letter > len(data["name"]["common"])/2 and letter_position > len(data["name"]["common"])/3:
            maybe.append(data["name"]["common"])
    if len(maybe) > 0:
        coun_maybe = ", ".join(maybe)
    else:
        coun_maybe = "Not found"
    return coun_maybe

#Gets all the required information about a country
def name(data: dict) -> str:
    try:
        capital = data["capital"][0]
    except KeyError:
        capital = "No hay capital"
    population = data["population"]
    area = data["area"]
    try:
        language = ", ".join([leng for leng in data["languages"].values()])
    except KeyError:
        language = "No hay lengua própia"
    info = f"Capital: {capital}\nPopulation: {population}\nArea: {area}\nLenguage: {language}"
    return info

#saves the flag of the country in the dir flags
def bandera(country: str, flag_im: str, img_format: str):
    try: #crea directorio en caso que no este
        mkdir(f"{CWD}/flags")
    except FileExistsError:
        pass
    open(f'''{CWD}/flags/{country}.{img_format}''', "wb").write(flag_im.content)


def count_in_continent(continent):
    list_countries = req.get(f"{url}/region/{continent}").json()
    return list_countries

def numerical(list_countries, request):
    if request == "area":
        quest = "Whats the biggest country of the continent?"
    else:
        quest = "Whats the most populated country of the continent?"
    list_countries.sort(key=lambda list_countries: list_countries[request], reverse=True)
    random_list = random.sample(range(1,int(len(list_countries)/2)),3)
    answers = [list_countries[0]["name"]["common"]]
    [answers.append(list_countries[q]["name"]["common"]) for q in random_list]
    return quest, answers

def capital(list_countries):
    random.shuffle(list_countries)
    quest =  f'''What's the capital of {list_countries[0]["name"]["common"]}'''
    answers = list(map(lambda a: a["capital"][0], list_countries[0:4]))
    return quest, answers

def language(list_countries):
    lang = []
    for data in list_countries:
        try:
            for i in data["languages"].values():
                if i not in lang:
                    lang.append(i)
        except:
            pass

    country = "Not defined"
    while country == "Not defined":
        random.shuffle(list_countries)
        try:
            list_countries[0]["languages"]
            country = list_countries[0]["name"]["common"]
        except:
            pass
    
    quest = f"Which of the following is an official language of {country}?"
    correct_answer = [random.choice(list(list_countries[0]["languages"].values()))]
    list(map(lambda s: lang.remove(s), list_countries[0]["languages"].values()))
    other_answers = [others for others in lang[1:4]]
    answers = correct_answer + other_answers
    return quest, answers

def car_side(list_countries):
    country = "Not defined"
    while country == "Not defined":
        random.shuffle(list_countries)
        try:
            list_countries[0]["car"]["side"]
            country = list_countries[0]["name"]["common"]
        except:
            pass
    quest = f'''What side of the road do they drive in {country}'''
    if list_countries[0]["car"]["side"] == "left":
        answer = ["left", "right"]
        return quest, answer
    answer = ["right", "left"]
    return quest, answer

if __name__ == "__main__": #testing this file
    pass