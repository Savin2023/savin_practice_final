from util import randbool
from util import randcell
from util import randcell2
 
# 0 - поле
# 1 - дерево
# 2 - река
# 3 - госпиталь
# 4 - апгрейд-шоп
# 5 - огонь
 
CELL_TYPES="📗🌴🌊🏥🏠🔥"
TREE_BONUS=100
UPGRADE_COST=300
LIFE_COST=100

class Map:

    def generate_river(self,l):     #  l - длина реки
        rc=randcell(self.w,self.h)
        rx,ry=rc[0],rc[1]   # rc - список из двух велеичин
        self.cells[rx][ry]=2
        while l>0:
            rc2=randcell2(rx,ry)
            rx2,ry2=rc2[0],rc2[1]
            if(self.check_bounds(rx2,ry2)):
                self.cells[rx2][ry2]=2
                rx,ry=rx2,ry2
                l-=1
                

    def generate_forest(self,r,mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if randbool(r,mxr):
                    self.cells[ri][ci]=1

    def generate_tree(self):
        c=randcell(self.w,self.h)
        cx,cy=c[0],c[1]
        if (self.cells[cx][cy]==0):
            self.cells[cx][cy]=1

    def generate_upgrade_shop(self):        # you may refactor on previous function
        c=randcell(self.w,self.h)
        cx,cy=c[0],c[1]
        self.cells[cx][cy]=4

    def generate_hospital(self):        # you may refactor on previous function
        c=randcell(self.w,self.h)
        cx,cy=c[0],c[1]
        if self.cells[cx][cy]!=4:      # to avoid duplicate with shop
            self.cells[cx][cy]=3
        else:
            self.generate_hospital()


    def print_map(self,helico,clouds):  # добавлен вертолет и облака
        print("📘" * (self.w+2)) # рамочка сверху
        for ri in range(self.h):                       # изменено row in self.cells:
            print("📘",end="") #рамочка слева
            for ci in range(self.w):                                    # изменено cell in row:
                cell=self.cells[ri][ci]
                if (clouds.cells[ri][ci]==1):   # clouds above all
                    print("⬜",end="")          # error with smiles     
                elif(clouds.cells[ri][ci]==2):   
                    print("🎈",end="")          # same error
                elif (helico.x==ri and helico.y==ci):     # проверка наличия вертолета #was BIG MISTAKE
                    print("🚁",end="")
                elif (cell>=0 and len(CELL_TYPES)):     # думаю здесь не надо рисовать
                    print(CELL_TYPES[cell],end="")
            print("📘") # рамочка справа и перевод строки
        print("📘" * (self.w+2)) # рамочка снизу       

    def check_bounds(self,x,y):
        if (x<0 or y<0 or x>=self.h or y>=self.w): 
            return False     # проверка принадлежности клетки полю
        return True
    
    def add_fire(self):
        c=randcell(self.w,self.h)
        cx,cy=c[0],c[1]
        if self.cells[cx][cy]==1:
            self.cells[cx][cy]=5

    def update_fires(self):
        for ri in range(self.h):
            for ci in range(self.w):
                cell=self.cells[ri][ci]
                if cell==5:
                   self.cells[ri][ci]=0
        for i in range(5):
            self.add_fire()


    def __init__(self,w,h):
        self.w=w
        self.h=h
        self.cells=[[0 for i in range(w)] for j in range(h)]
        self.generate_forest(3,10)
        self.generate_river(20)
        self.generate_river(20)
        self.generate_upgrade_shop()
        self.generate_hospital()

    def process_helicopter(self,helico,clouds):
        c=self.cells[helico.x][helico.y]   # upload water  ERROR out of range
        d=clouds.cells[helico.x][helico.y]      # cloud coords
        if (c==2):
            helico.tank=helico.mxtank
        if (c==5 and helico.tank>0):     # download water to fire
            helico.tank-=1
            helico.score+=TREE_BONUS
            self.cells[helico.x][helico.y]=1
        if (c==4 and helico.score>UPGRADE_COST):     # UPGRADE shop
            helico.mxtank+=1
            helico.score-=UPGRADE_COST
        if (c==3 and helico.score>LIFE_COST):     # medical
            helico.lives+=1000
            helico.score-=LIFE_COST
        if (d==2):
            helico.lives-=1
            if (helico.lives==0):
                helico.gameover()
                
    def export_data(self):
        return {"cells":self.cells}
    
    def import_data(self,data):
        self.sellc=data["cells"] or [[0 for i in range(self.w)] for j in range(self.h)]
            




