import copy
import math

import pygame
import random

# Define the colors used in the labyrinth
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255,0,0)

# Set the dimensions of the labyrinth
WIDTH = 600
HEIGHT = 600
MARGIN = 0
CELL_SIZE = 20
ROWS = (HEIGHT - 2 * MARGIN) // CELL_SIZE +1
COLS = (WIDTH - 2 * MARGIN) // CELL_SIZE + 1
FOOD = 3
GHOSTS = 2

# Initialize the Pygame library
pygame.init()

# Set the size of the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT+200))

# Set the title of the screen
pygame.display.set_caption("Pac-Man Labyrinth")

button_rect = pygame.Rect(WIDTH//2-100,HEIGHT+100, 200, 50)
button_color = (255, 0, 0)
button_text = 'Next step'
button_font = pygame.font.Font(None, 36)
button_text_color = (255, 255, 255)

def check_dead_end(arr, cell, col_bound, row_bound):
    if cell[0]<= 0 or cell[0]>=col_bound or cell[1]>=row_bound or cell[1]<=0:
        return False

    calc = 0
    neighbors = []
    for cell0 in arr:
        if (cell0[0]==cell[0] and (cell0[1]+1==cell[1] or cell0[1]-1==cell[1])) or (cell0[1]==cell[1] and (cell0[0]+1==cell[0] or cell0[0]-1==cell[0])):
            calc+=1
            neighbors.append(cell0)
    if calc == 1:
        return True
    return False

# Create the 2D array to represent the labyrinth
def check_next(arr, cell, col_bound, row_bound):
    if cell[0]<= 0 or cell[0]>=col_bound or cell[1]>=row_bound or cell[1]<=0:
        return False
    if cell in arr:
        return False
    calc = 0
    neighbors = []
    for cell0 in arr:
        if (cell0[0]==cell[0] and (cell0[1]+1==cell[1] or cell0[1]-1==cell[1])) or (cell0[1]==cell[1] and (cell0[0]+1==cell[0] or cell0[0]-1==cell[0])):
            calc+=1
            neighbors.append(cell0)

    if calc == 2:
        if neighbors[0][0]==neighbors[1][0] or neighbors[0][1]==neighbors[1][1]:
            return True
        return False
    if calc >2:
        return False
    return True

def next_cell(cell, dir):
    res = copy.deepcopy(cell)
    if dir == 0:
        res[0]+=1
    if dir == 1:
        res[1]+=1
    if dir == 2:
        res[0]-=1
    if dir == 3:
        res[1]-=1
    return res

def remove_dead_ends(arr, col_bound, row_bound):
    arr_copy = copy.deepcopy(arr)

    while len(arr_copy)>0:
        el = arr_copy.pop(0)
        if check_dead_end(arr, el, col_bound, row_bound):
            arr.remove(el)
            arr_copy = copy.deepcopy(arr)
    return arr



def generate_labyrinth(CNum, RNum, FNum, GNum):
    # Initialize the labyrinth with solid walls
    #random.seed(3) - ghosts win
    #random.seed(1)  - packman wins

    labyrinth = [[1 for col in range(CNum)] for row in range(RNum)]
    for i in range(CNum):
        for j in range(RNum):
            if i == 0 or i == CNum-2 or j == 0 or j == RNum-2:
                labyrinth[i][j]=1
    istart = random.randint(1, CNum-3)
    jstart = random.randint(1, RNum - 3)
    current = [istart, jstart]
    visited = [[istart,jstart]]
    Length = int(CNum*RNum*0.35)
    visited2 = []
    direct = random.randint(0,4)
    while Length>0:
        direction = random.randint(0, 4)
        n_cell = next_cell(current,direction)
        checker = 0
        while not check_next(visited,n_cell, CNum-2, RNum-2) and checker<5:
            n_cell = next_cell(current, (direction+1)%4)
            checker+=1
        if checker !=4 and check_next(visited,n_cell, CNum-2, RNum-2):
            visited.append(n_cell)
            current = n_cell
            Length-=1
            visited2.clear()

        else:

            visited2.append(current)

            if len(visited)==len(visited2):
                break
            for cell in visited:
                if cell not in visited2 :
                    current = cell
                    break
    visited = remove_dead_ends(visited, CNum-2, RNum-2)
    ghosts = []
    food = []
    for cell in visited:
        labyrinth[cell[0]][cell[1]]=0
    for i in range(FNum):
        ran = random.randint(0, len(visited)-1)

        food.append([visited[ran][0],visited[ran][1]])
    for i in range(GNum):
        ran = random.randint(0, len(visited)-1)

        ghosts.append([visited[ran][0],visited[ran][1]])

    ran = random.randint(0, len(visited) - 1)
    #labyrinth[visited[ran][0]][visited[ran][1]] = 4
    pacman = [visited[ran][0],visited[ran][1]]
    return labyrinth, visited, ghosts, pacman, food










def draw_labyrinth(labyrinth, ghosts, pacman, food):
    for row in range(ROWS):
        for col in range(COLS):
            if labyrinth[row][col] == 0:
                color = WHITE

            else:
                color = YELLOW
            """if row==1 and col == 1:
                color = BLUE"""
            pygame.draw.rect(screen, color, [(MARGIN + CELL_SIZE) * col + MARGIN, (MARGIN + CELL_SIZE) * row + MARGIN, CELL_SIZE, CELL_SIZE])

    for el in ghosts:
        color = BLACK
        pygame.draw.circle(screen, color, [(MARGIN + CELL_SIZE) * el[1] + MARGIN + CELL_SIZE // 2,
                                           (MARGIN + CELL_SIZE) * el[0] + MARGIN + CELL_SIZE // 2], CELL_SIZE // 3)
    for el in food:
        color = BLUE
        pygame.draw.rect(screen, color,
                         [(MARGIN + CELL_SIZE) * el[1] + MARGIN + CELL_SIZE // 4,
                          (MARGIN + CELL_SIZE) * el[0] + MARGIN + CELL_SIZE // 4, CELL_SIZE // 2,
                          CELL_SIZE // 2])
    color = RED

    pygame.draw.circle(screen, color, [(MARGIN + CELL_SIZE) * pacman[1] + MARGIN + CELL_SIZE // 2,
                                       (MARGIN + CELL_SIZE) * pacman[0] + MARGIN + CELL_SIZE // 2], CELL_SIZE // 3)

# Define a function to display the labyrinth on the screen
def display_labyrinth(labyrinth, ghosts, pacman, food):

    draw_labyrinth(labyrinth, ghosts, pacman, food)
    pygame.display.flip()

# Call the function to display the labyrinth on the screen
def get_ne(lab, cell):
    neighbors = []
    for cell0 in lab:
        if (cell0[0] == cell[0] and (cell0[1] + 1 == cell[1] or cell0[1] - 1 == cell[1])) or (
                cell0[1] == cell[1] and (cell0[0] + 1 == cell[0] or cell0[0] - 1 == cell[0])):
            neighbors.append(cell0)
    return neighbors

def a_star_for_actor(lab, ghosts, pacman, food):
    neighbors = get_ne(lab, pacman)
    if pacman in food:
        food.remove(pacman)
        return lab, ghosts, pacman, food
    visited_p = [pacman]
    paths = []
    for el in neighbors:
        if el in food and el not in ghosts:
            pacman = copy.deepcopy(el)
            food.remove(el)
            return lab, ghosts, pacman, food
    for el in neighbors:
        if el in ghosts:
            continue
        visited_p.append(el)
        paths.append([el])
    finish_paths = []
    while True:
        new_paths = []
        for path in paths:
            last = path[len(path) - 1]

            neighbors_temp = get_ne(lab, last)
            for el in neighbors_temp:
                temp = copy.deepcopy(path)
                if el in visited_p:
                    continue

                check = 0
                for pa in paths:
                    if el in pa:
                        check = 1
                if check == 0 and el not in ghosts:
                    temp.append(el)
                    new_paths.append(temp)
                    visited_p.append(el)
                if check == 0 and el not in ghosts and el in food:
                    finish_paths.append(temp)
        if len(finish_paths) > 0:
            break
        paths = copy.deepcopy(new_paths)

    if len(finish_paths) > 1:
        path = copy.deepcopy(finish_paths[0])
        for i in range(1, len(finish_paths)):
            if len(finish_paths[i]) <= len(path):
                path = copy.deepcopy(finish_paths[i])
        finish_paths = copy.deepcopy([path])
    path0 = finish_paths[0]
    cell = path0[0]
    pacman = copy.deepcopy(cell)

    return lab, ghosts, pacman, food

def greedy_for_actor(lab, ghosts, pacman, food):
    neighbors = get_ne(lab, pacman)
    if pacman in food:
        food.remove(pacman)
        return lab, ghosts, pacman, food

    for el in neighbors:
        if el in food and el not in ghosts:
            pacman = copy.deepcopy(el)
            food.remove(el)
            return lab, ghosts, pacman, food
    sum = 10000
    next = []
    for el in neighbors:
        if el in ghosts:
            continue
        for f in food:
            temp= math.sqrt(abs(el[0]-f[0])**2+abs(el[1]-f[1])**2)
            if temp < sum:
                next = copy.deepcopy(el)
                sum = temp
    pacman = copy.deepcopy(next)


    return lab, ghosts, pacman, food

def next_step_a_star(lab, ghosts, pacman, food):
    lab, ghosts, pacman, food = a_star_for_actor(lab, ghosts, pacman, food)
    if len(food)==0:
        print("packman wins!")
        return lab, ghosts, pacman, food
    pacman2 = copy.deepcopy(pacman)
    check = 0
    for i in range(len(ghosts)):
        lab, temp1, ghosti, temp2 = a_star_for_actor(lab, [], ghosts[i], [pacman])
        if temp2 == []:
            print("ghosts win!")
            check=1
        ghosts[i]= copy.deepcopy(ghosti)
    if check == 1:
        return lab, ghosts, pacman2, []
    return lab, ghosts, pacman, food

def next_step_greedy(lab, ghosts, pacman, food):
    lab, ghosts, pacman, food = greedy_for_actor(lab, ghosts, pacman, food)
    if len(food)==0:
        print("packman wins!")
        return lab, ghosts, pacman, food
    pacman2 = copy.deepcopy(pacman)
    check = 0
    for i in range(len(ghosts)):
        lab, temp1, ghosti, temp2 = greedy_for_actor(lab, [], ghosts[i], [pacman])
        if temp2 == []:
            print("ghosts win!")
            check=1
        ghosts[i]= copy.deepcopy(ghosti)
    if check == 1:
        return lab, ghosts, pacman2, []
    return lab, ghosts, pacman, food

if __name__ == "__main__":
    screen.fill(WHITE)
    labyrinth, path, ghosts, pacman, food = generate_labyrinth(COLS, ROWS, FOOD, GHOSTS)
    display_labyrinth(labyrinth, ghosts, pacman, food)

    pygame.draw.rect(screen, button_color, button_rect)
    button_surface = button_font.render(button_text, True, button_text_color)
    button_surface_rect = button_surface.get_rect(center=button_rect.center)
    screen.blit(button_surface, button_surface_rect)
    pygame.display.flip()
    # Wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    path, ghosts, pacman, food = next_step_a_star(path, ghosts, pacman, food)
                    #path, ghosts, pacman, food = next_step_greedy(path, ghosts, pacman, food)
                    if len(food)>=0:
                        display_labyrinth(labyrinth, ghosts, pacman, food)

        """ for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.time.wait(100)
        path, ghosts, pacman, food = next_step_g(path, ghosts, pacman, food)
        if len(food) >= 0:
            display_labyrinth(labyrinth, ghosts, pacman, food)"""



