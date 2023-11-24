#============imports=============
import random
import time
import os
import matrix
from pynput import keyboard
from colorama import Fore, Back
#================================


class Tetris:
    def __init__(self):
        # creates a 24x10 grid of 0s as base
        self.grid = [[0 for i in range(10)] for j in range(24)] + [[2 for i in range(10)]]
        
        # shapes in tetris
        self.shapes = [[[0,0,0,0,1,0,0,0,0,0],
                        [0,0,0,0,1,0,0,0,0,0],
                        [0,0,0,0,1,0,0,0,0,0],
                        [0,0,0,0,1,0,0,0,0,0]], # I shape

                       [[0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,1,1,0,0,0,0],
                        [0,0,0,0,1,1,0,0,0,0]], # O shape

                       [[0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,1,1,0,0,0,0],
                        [0,0,0,1,1,0,0,0,0,0]], # S shape

                       [[0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,1,1,0,0,0,0],
                        [0,0,0,0,0,1,1,0,0,0]], # Z shape

                       [[0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,1,0,0,0,0,0],
                        [0,0,0,0,1,0,0,0,0,0],
                        [0,0,0,0,1,1,0,0,0,0]], # L shape

                       [[0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,1,0,0,0,0],
                        [0,0,0,0,0,1,0,0,0,0],
                        [0,0,0,0,1,1,0,0,0,0]], # J shape

                       [[0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,1,1,1,0,0,0,0],
                        [0,0,0,0,1,0,0,0,0,0]]]# T shape
        
        self.rt = None
        self.point = 0
        self.num_arr = []
        self.next_shape = [list(row) for row in self.chose_shape()]  # Create a copy of the chosen shape
        self.current_shape = [list(row) for row in self.next_shape]  # Create a copy of the next shape
        self.shape_location = 1
        self.horizontal = 0
        self.game_state = False
        self.fast_drop = False


    def remove_grid(self,row):
            ''' Removes a row from the grid and shifts all the rows above it down by one '''
            for i in range(row,0,-1):
                self.grid[i] = self.grid[i-1]
            self.grid[0] = [0 for i in range(10)]
    
    def check_grid(self):
        for i in range(24):
            if sum(self.grid[i])==10:
                self.remove_grid(i)
    
    def chose_shape(self):
        shape_num =  random.randint(0,len(self.shapes)-1)
        self.num_arr.append(shape_num)
        self.point += 1
        return self.shapes[shape_num]


    def display(self):
        os.system("clear")
        print(f"           {self.point}")
        print("+---------------------+     +---------+")
        cut_shape = self.cut_shape()
        c = 0
        for i,row in enumerate(self.grid[:-1]):
            if self.shape_location<=i<=self.shape_location+3:
                if i>3:
                    sum = []
                    for j in range(len(self.current_shape[c])):
                        a = self.current_shape[c][j]+self.grid[i][j]
                        if a==0:
                            sum.append(" ")
                        else:
                            sum.append(Back.WHITE+" ")
                    print("|",*sum,"|", sep=" "+Back.RESET,end="     " if i<=8 and i>3 else "\n")
                c+=1
            else:
                if i>3:
                    row = [" " if i==0 else Back.WHITE+" " for i in row]
                    print("|",*row,"|", sep=" "+Back.RESET,end="     " if i<=8 and i>3 else "\n")

            if i<=7 and i>3:
                temp_cut_shape = cut_shape.copy()
                for j in range(len(temp_cut_shape)):
                    temp_cut_shape[j] = [" " if i==0 else Back.WHITE+" " for i in temp_cut_shape[j]]
                print("|",*temp_cut_shape[i-4],"|",sep=" "+Back.RESET)
            elif i==8:
                print("+---------+")
        print("+---------------------+")
    
    def cut_shape(self,shape = None): # crops the shape list to fit the 5x5 box
        if not shape:
            shape = self.next_shape
        l = []
        for i in shape:
            a = i[3:7]
            l.append(a)
        return l
    
    def paste_shape(self):
        for i in range(4):
            for j in range(10):
                self.grid[self.shape_location+i][j] += self.current_shape[i][j]

    def load_new(self):
        self.paste_shape()
        self.current_shape = self.next_shape.copy()  # Create a new copy of the list
        self.next_shape = self.chose_shape().copy()  
        self.shape_location = 1

        if sum(self.grid[4])>1:
            self.game_over()

    def game_over(self):
        self.game_state = True
        print("Game Over: points: ",self.point) 

    def move_down(self):
        flag = True
        for i in range(4):
            for j in range(10):
                if self.grid[self.shape_location+i+1][j] + self.current_shape[i][j] > 1:
                    flag = False
        if flag:
            self.shape_location += 1
        else:
            self.on_collision()

    def on_collision(self):
        self.fast_drop = False
        self.rt = None
        self.horizontal = 0
        self.load_new()

    def move_left(self,times=1):
        new_shape = [list(row) for row in self.current_shape]  # Create a copy of self.current_shape
        for _ in range(times):
            for i, j in enumerate(new_shape):
                if j[0] != 1:
                    new_shape[i].pop(0)
                    new_shape[i].insert(-1, 0)

        self.current_shape = new_shape
        self.horizontal -= 1

    def move_right(self,times=1):
        new_shape = [list(row) for row in self.current_shape]  # Create a copy of self.current_shape
        for _ in range(times):
            for i, j in enumerate(new_shape):
                if j[-1] != 1:
                    new_shape[i].pop(-1)
                    new_shape[i].insert(0, 0)
        self.current_shape = new_shape
        self.horizontal += 1

    def rotate(self):

        if self.rt == None:
            try:
                self.rt = self.shapes[self.num_arr[-2]]
            except:
                self.rt = self.shapes[self.num_arr[0]]
        temp_shape = [list(row) for row in self.rt]
        new_cut_shape = self.cut_shape(temp_shape)
        new_cut_shape = matrix.rotate(new_cut_shape, dir)

        for i in range(len(temp_shape)):
            temp_shape[i][3:7] = new_cut_shape[i]

        for i in range(4):
            for j in range(10):
                if self.grid[self.shape_location + i][j] + temp_shape[i][j] > 1:
                    return self.current_shape.copy()

        self.rt = temp_shape
        return temp_shape

a = Tetris()

def press(key):
    if key == keyboard.Key.left:
        a.move_left()
    elif key == keyboard.Key.right:
        a.move_right()
    elif key == keyboard.Key.up:
        a.current_shape = a.rotate()
        if a.horizontal>0:
            a.move_right(a.horizontal)
        if a.horizontal<0:
            a.move_left(abs(a.horizontal))
    elif key == keyboard.Key.down:
        a.fast_drop = True
    elif key == keyboard.KeyCode.from_char('q'):
        a.game_over()


inp=keyboard.Listener(on_press=press)
inp.start()   

while not a.game_state:
    a.check_grid()
    a.display()
    if a.fast_drop:
        time.sleep(0.05)
        a.move_down()
    else:
        time.sleep(0.40)
    a.move_down()
    