
import copy
        # 1  2  3  4  5  6  7  8  9  10
import math

Facts = [[1, 1, 0, 0, 0, 1, 0, 1, 0, 1,"Наруто Удзумакі з аніме 'Наруто'"]
        ,[1, 1, 0, 0, 0, 1, 0, 0, 0, 0,"Ізуку Мідорія з аніме 'Моя геройська академія'"]
        ,[1, 0, 0, 0, 0, 0, 0, 1, 0, 1,"Соске Сагара з аніме 'Сталева тривога'"]
        ,[0, 1, 0, 0, 1, 0, 0, 1, 1, 0,"Телета Тестаросса з аніме 'Сталева тривога'"]

         ]
Questions = ["Цей персонаж є головним героєм аніме-серіалу?"#1
,"Чи має цей персонаж володіння магією або надприродними здібностями?"#2
,"Чи є цей персонаж роботом або механічним створінням?"#3
,"Чи має цей персонаж яку-небудь ознаку тварини (крила, хвіст тощо)?"#4
,"Цей персонаж жіночої статі?"#5
,"Чи навчався цей персонаж у будь-якому закладі на початку історії аніме?"#6
,"Цей персонаж був заснований на реальній історичній або міфічній фігурі?"#7
,"Цей персонаж є членом якої-небудь команди або групи?"#8
,"Цей персонаж має високий інтелект?"#9
,"Цей персонаж має багато різноманітних бойових навичок або володіє спеціальною зброєю?"]#10



def select_question(facts, visited):
    entrop = 100
    questN = 0
    for i in range(10):
        if i not in visited:
            calc0 = 0
            calc1 = 0
            calcNone = 0
            A = len(facts)
            for el in facts:
                if el[i] == 0:
                    calc0+=1
                elif el[i]== 1:
                    calc1+=1
                else:
                    calcNone+=1

            entropi = 0
            if calc0!=0:
                entropi+=-calc0/A * (math.log2(1/calc0))
            if calc1!=0:
                entropi+= -calc1/A * (math.log2(1/calc1))
            if calcNone !=0:
                entropi += -calcNone/A * (math.log2(1/calcNone))
            if entropi < entrop:
                entrop = entropi
                questN = i
    return questN


def work():
    fact = [None, None, None, None, None, None, None, None, None, None, None]
    current_facts = copy.deepcopy(Facts)
    asked = []
    for i in range(0, 7):
        quest = select_question(current_facts, asked)
        asked.append(quest)
        answ = 0
        while True:
            res = input(Questions[quest] + "\n")
            if res == "1":
                answ = 1
                break
            elif res != "0":
                print("введіть 0 - ні, 1 - так")
            else:
                break
        new_facts = []
        fact[quest] = answ
        for el in current_facts:
            if el[quest] == answ or el[quest] is None:
                new_facts.append(el)
        current_facts = copy.deepcopy(new_facts)
    if len(current_facts) > 0:
        answ = 0
        name = ""
        for el in current_facts:

            while True:
                res = input("Ваш персонаж - " + el[10] + "?\n")
                if res == "1":
                    answ = 1
                    name = el[10]
                    break
                elif res != "0":
                    print("введіть 0 - ні, 1 - так")
                else:
                    break
            if answ == 1:
                for j in range(len(Facts)):
                    if Facts[j][10]==name:
                        for i in range(len(Facts[j])):
                            if Facts[j][i] is None and fact[i] is not None:
                                Facts[j][i] = fact[i]
                break
        if answ == 0:
            res = input("Введіть вашого персонажа \n")
            fact[10] = res
            Facts.append(fact)
    else:
        res = input("Введіть вашого персонажа \n")
        fact[10] = res
        Facts.append(fact)

if __name__ == "__main__":
    while True:
        res = input("Start")
        if res == "1":
            work()
        else:
            break

