import copy

Groups = [[1,20],[2,30],[3,10],[4,15],[5,13]] #id + Number of students
SubIds = [1,2,3,4,5]
Subjects = [[1, "Практика"], [2,"Практика"], [3,"Лекція"],[4,"Лекція"], [5,"Практика"]]
Rooms = [[101,15],[222,25],[300,40],[440,50],[442,50],[4222,50]]
Teachers = ["Перший викладач","Другий викладач","Третій викладач","Четвертий викладач","П'ятий викладач"]#,"П'ятий викладач"
Days = ["ПН","ВТ","СР","ЧТ","ПТ"]
SUBJECTS_PER_WEEK = 30
TIME_START = 9
TIME_END = 15
#Class (list of id) - day, time, group, room, subj, teacher
def checkFunction(classes):
    teacher_check = []
    group_check = []
    lecture_check = []
    rooms_check = []
    problems = 0
    for el in classes:
        room0 = [el[3],el[1],el[0]]
        if None not in room0 and room0 in rooms_check:
            problems+=1
        else:
            rooms_check.append(room0)

        teacher0 = [el[5], el[1], el[0]]
        if None not in teacher0 and teacher0 in teacher_check:
            problems += 1
        else:
            teacher_check.append(teacher0)
        group0 = [el[2], el[1], el[0]]
        if None not in group0 and group0 in group_check:
            problems += 1
        else:
            group_check.append(group0)
        if el[4] is not None and Subjects[el[4]][1]=="Лекція":
            lecture0 = [el[5],el[4]]
            lecture_check.append(lecture0)
        if el[2] is not None and el[3] is not None and Groups[el[2]][1] > Rooms[el[3]][1]:
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
            problems+=calc

    """if problems > 0:
        return False
    return True"""
    return problems

def degree_heuristic(schedule):
    day_time = [[0 for i in range(TIME_START,TIME_END)] for j in range(len(Days))]
    for el in schedule:
        if el[0] is not None and el[1] is not None:
            day_time[el[0]][el[1]] +=1
    min_v = 100000
    minij = []
    for i in range(len(Days)):
        for j in range(TIME_END-TIME_START):
            if day_time[i][j]<min_v:
                minij=[i,j]
                min_v = day_time[i][j]

    groups_day = [0 for i in range(len(Groups))]
    for el in schedule:
        if el[0] is not None and el[1] is not None:
            if el[0]==minij[0]:
                groups_day[el[2]]+=1
    min_g = groups_day.index(min(groups_day))
    return minij[0], minij[1], min_g

def lrv_heuristic(schedule, day, time, group):
    teacher, room, subj = [],[],[]

    rooms_cap = [x for [y,x] in Rooms]
    group_num = Groups[group][1]

    for i in range(len(rooms_cap)):
        dist0 = rooms_cap[i] - group_num
        room.append([i,dist0])
    room = sorted(room, key=lambda x: x[1])
    teacher_day = [[i,0] for i in range(len(Teachers))]
    for el in schedule:
        if el[0] is not None and el[5] is not None:
            if el[0] == day:
                teacher_day[el[5]][1] += 1
    subj_day = [[i,0] for i in range(len(Subjects))]
    for el in schedule:
        if el[0] is not None and el[4] is not None:
            if el[0] == day:
                subj_day[el[4]][1] += 1
    teacher_day = sorted(teacher_day, key=lambda x:x[1])
    subj_day = sorted(subj_day, key=lambda x:x[1])

    result = []
    for r in room:
        for t in teacher_day:
            for s in subj_day:
                result.append([r[0],  s[0],t[0]])
    return result



def backtraking(schedule):
    error = 0
    for i in range(len(Groups)*SUBJECTS_PER_WEEK):
        day, time, group= degree_heuristic(schedule)
        for  room, subj,teacher in lrv_heuristic(schedule,day,time,group):
            schedule[i]=copy.deepcopy([day,time,group,room,subj, teacher])
            if checkFunction(schedule)>0:
                schedule[i]=[None,None,None,None,None,None]
                error = 1
            else:
                error = 0
                break
        if error == 1:
            print("no solution!")
            exit()


    return schedule

if __name__ == "__main__":
    schedule = []
    for i in range(SUBJECTS_PER_WEEK*len(Groups)):
        schedule.append([None,None,None,None,None,None])

    schedule = backtraking(schedule)




    temp_day = -1
    temp_time = -1
    for el in sorted(schedule,key=lambda x:(x[0],x[1],x[2])):
        if temp_day<el[0]:
            temp_day = el[0]
            temp_time = -1
            print("=========================================================")
            print("День - ", Days[el[0]])
        if temp_time<el[1]:
            temp_time = el[1]
            print("Час - ", el[1]+TIME_START, ":00")

        print("Група - ", Groups[el[2]][0], " Студентів у групі - ", Groups[el[2]][1])
        print("Аудиторія - ", Rooms[el[3]][0], "Макс студентів - ", Rooms[el[3]][1])
        print("Предмет - ", Subjects[el[4]][0], "Тип - ", Subjects[el[4]][1])
        print("Викладач - ", Teachers[el[5]])
        print("-------------")
    print(checkFunction(schedule))    

