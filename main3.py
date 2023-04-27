import copy
import random

Groups = [[1,20],[2,30],[3,10],[4,15],[5,13]] #id + Number of students
SubIds = [1,2,3]
Subjects = [[1, "Практика"], [2,"Практика"], [3,"Лекція"]]  #id + 1 - lecture, 0 - practice
Rooms = [[101,15],[222,25],[300,40],[440,50],[55,17],[6,20]]
Teachers = ["Перший викладач","Другий викладач","Третій викладач","Четвертий викладач","П'ятий викладач"]
TIME_START = 9
TIME_END = 15
Days = ["ПН","ВТ","СР","ЧТ","ПТ"]

SUBJECTS_PER_WEEK = 10
#Class (list of id) - day, time, group, room, subj, teacher

def checkFunction(classes):
    teacher_check = []
    group_check = []
    lecture_check = []
    problems = 0
    for el in classes:
        teacher0 = [el[5], el[1], el[0]]
        if teacher0 in teacher_check:
            problems += 1
        else:
            teacher_check.append(teacher0)
        group0 = [el[2], el[1], el[0]]
        if group0 in group_check:
            problems += 1
        else:
            group_check.append(group0)
        if Subjects[el[4]][1]=="Лекція":
            lecture0 = [el[5],el[4]]
            lecture_check.append(lecture0)
        if Groups[el[2]][1] > Rooms[el[3]][1]:
            problems+=1

    for id in SubIds:
        calc = 0
        teach0 =-1
        for el in lecture_check:
            if el[1]==id and teach0==-1:
                calc+=1
                teach0=el[0]
            elif el[1]== id and teach0>=0:
                calc+=1
        if calc > 1:
            problems+=1

    return problems

def breeding(el1,el2):
    point = random.randint(2,len(el1)-3)
    ch1 = copy.deepcopy(el1[0:point])+copy.deepcopy(el2[point:len(el2)])
    ch2 = copy.deepcopy(el2[0:point])+copy.deepcopy(el1[point:len(el1)])
    return ch1, ch2

def mutate(el):
    el2 = copy.deepcopy(el)
    rand = random.randint(0, len(el2)-1)
    day = random.randint(0, len(Days)-1)
    time = random.randint(TIME_START, TIME_END)
    teacher = random.randint(0, len(Teachers) - 1)
    room = random.randint(0, len(Rooms) - 1)
    subj = random.randint(0, len(Subjects) - 1)
    group = random.randint(0,len(Groups)-1)
    el2[rand] = [day, time, group, room, subj, teacher]
    return el2





def generate_start(Start_Number):
    res = []
    for j in range(Start_Number):
        res0 = []
        for j in range(len(Groups)):
            for i in range(SUBJECTS_PER_WEEK):
                day = random.randint(0, len(Days)-1)
                time = random.randint(TIME_START, TIME_END)
                teacher = random.randint(0, len(Teachers) - 1)
                room = random.randint(0, len(Rooms) - 1)
                subj = random.randint(0, len(Subjects)-1)
                res0.append([day, time, j, room,  subj,teacher])
        res.append(copy.deepcopy(res0))
    return res

START_POPULATION_NUMBER = 100
MUTATION_RATE = 10
CROSSING_RATE = 90
MAX_GENERATIONS = 50
if __name__ == "__main__":
    schedule = generate_start(START_POPULATION_NUMBER)
    min_fintess = 10000
    best_result = []
    for population_index in range(MAX_GENERATIONS):
        print(str(population_index) +" ітерація")
        fitness = []
        for el in schedule:
            fitness.append(checkFunction(el))
        print(str(sum(fitness)/len(fitness))+" - середня пристосованість")
        print(str(min(fitness))+" - найкраща пристосованість")




        if min(fitness) < min_fintess:
            best_result = schedule[fitness.index(min(fitness))]
            min_fintess = min(fitness)

        if min(fitness)==0:
            break
        random.shuffle(schedule)
        after_cross = []
        for el1,el2 in zip(schedule[::2],schedule[1::2]):
            if random.randint(0,100) < CROSSING_RATE:
                ch1,ch2 = breeding(el1,el2)
                after_cross.append(ch1)
                after_cross.append(ch2)
            else:
                after_cross.append(el1)
                after_cross.append(el2)
        after_mutation = []
        for el in after_cross:
            if random.randint(0,100)<MUTATION_RATE:
                el1 = mutate(el)
                after_mutation.append(el1)
            else:
                after_mutation.append(el)

        schedule = copy.deepcopy(after_mutation)
    print(sorted(best_result,key=lambda x:(x[0],x[2])))
    print(min_fintess)


    temp_day = -1
    temp_time = -1
    for el in sorted(best_result,key=lambda x:(x[0],x[1],x[2])):
        if temp_day<el[0]:
            temp_day = el[0]
            temp_time = -1
            print("=========================================================")
            print("День - ", Days[el[0]])
        if temp_time<el[1]:
            temp_time = el[1]
            print("Час - ", el[1], ":00")

        print("Група - ", Groups[el[2]][0], " Студентів у групі - ", Groups[el[2]][1])
        print("Аудиторія - ", Rooms[el[3]][0], "Макс студентів - ", Rooms[el[3]][1])
        print("Предмет - ", Subjects[el[4]][0], "Тип - ", Subjects[el[4]][1])
        print("Викладач - ", Teachers[el[5]])
        print("-------------")

    print("пристосованість = ", min_fintess)
