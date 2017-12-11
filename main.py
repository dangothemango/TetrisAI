# -*- coding: utf-8 -*-
#Dan GORMAN
#3/12/13
#Tetris


import pygame, sys, time, random, datetime
from pygame.locals import *
from queue import Queue
import random

# set up pygame

pygame.init()

# set up the window
WINDOWWIDTH = 340
WINDOWHEIGHT = 2*WINDOWWIDTH
columnwidth=int(WINDOWWIDTH/10)
rowheight=int(WINDOWHEIGHT/20)
notplaywindow=WINDOWWIDTH+(5*columnwidth)
window = pygame.display.set_mode((notplaywindow, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Tetris')

# set up the play variables
BLACK = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple=(120,0,120)
WHITE=(255,255,255)
yellow=(255,255,0)
cyan=(0, 255, 255)
grey=(128, 128, 128)
orange=(255, 127, 0)

blocks=[[[-1,0],[1,0],[2,0],cyan],[[-1,0],[-1,-1],[1,0],blue],[[-1,0],[1,0],[1,-1],orange],[[0,-1],[1,-1],[1,0],yellow],[[-1,0],[0,-1],[1,-1],green],[[-1,0],[0,-1],[1,0],purple],[[-1,-1],[0,-1],[1,0],red]]
startspotx=columnwidth*4
startspoty=-rowheight
blockonscreen=[]
points=0
newblock=1
fix=0
speed=.02
hi=0
blockmovecount=9
a=0
b=0
c=0
d=0
trials = 0
maxTrials = 2

FILE = open('Outputs.txt', 'a+')

# set up the rect data structure
def makenewblock(block):
    return [pygame.Rect(startspotx,startspoty,columnwidth,rowheight),pygame.Rect(startspotx+(block[0][0]*columnwidth),startspoty+(block[0][1]*rowheight),columnwidth,rowheight),pygame.Rect(startspotx+(block[1][0]*columnwidth),startspoty+(block[1][1]*rowheight),columnwidth,rowheight),pygame.Rect(startspotx+(block[2][0]*columnwidth),startspoty+(block[2][1]*rowheight),columnwidth,rowheight),block[3]]

def overlap(one,two):
    for bk in two:
        if bk!=curblock:
            for b in range(len(bk)-1):
                if one==bk[b]:
                    return True
    return False

def harddrop():
    fix=0
    while True:
        for i in range(4):
            curblock[i].top+=(rowheight)
            if curblock[i].top==WINDOWHEIGHT:
                fix=1
            if overlap(curblock[i],blockonscreen):
                fix=1
        if fix:
            for i in range(4):
                curblock[i].top-=(rowheight)
                fix=0
            lineclear()
            break

def makeghost():
    fix=0
    ghost=[]
    for i in range(4):
        ghost.append(pygame.Rect(curblock[i].left,curblock[i].top,curblock[i].width,curblock[i].height))
    ghost.append((40,40,40))
    while True:
        for i in range(4):
            ghost[i].top+=(rowheight)
            if ghost[i].top==WINDOWHEIGHT:
                fix=1
            if overlap(ghost[i],blockonscreen):
                fix=1
        if fix:
            for i in range(4):
                ghost[i].top-=(rowheight)
                fix=0
            break
        
    return ghost
                
def rotfix(drec):
    if drec=='UP':
        for i in range(4):
            curblock[i].top-=rowheight
    elif drec=='LEFT':
        for i in range(4):
            curblock[i].left-=columnwidth
    elif drec=='RIGHT':
        for i in range(4):
            curblock[i].left+=columnwidth
bag=[0,1,2,3,4,5,6]

def shufflefirst():
    newbag=[]
    newbag2=[]
    for i in range (7):
        while True:
            x=random.choice(bag)
            if x not in newbag:
                newbag.append(x)
                break
        while True:
            y=random.choice(bag)
            if y not in newbag2:
                newbag2.append(x)
                break
    newbag3=newbag+newbag2
    
    return newbag3

def shuffle():
    newbag1=pieces[7:]
    newbag=[]
    for i in range (7):
        while True:
            x=random.choice(bag)
            if x not in newbag:
                newbag.append(x)
                break
    newbag3=newbag1+newbag
    return newbag3

def copyrect(rect):
    return pygame.Rect(rect.left,rect.top,rect.width,rect.height)

def rotatecheck(curc, ro, col):
    new=[]
    for z in range(len(curc)):
        if z != 4:
            new.append(copyrect(curc[z]))
        else:
            new.append(curc[4])
    rotate(new, ro, col)
    for i in range(len(new)-1):
        if new[i].left<0 or new[i].left>=WINDOWWIDTH:
            return False
        for b in blockonscreen:
            if b != curc:
                for x in range(len(b)-1):
                    if new[i] == b[x]:
                        return False
    return True

def rotate(curr,ro,col):
     if curr[4]==yellow:
         rotateo(curr,ro,col)
     if curr[4]==cyan:
         rotatei(curr,ro,col)
     else:
         rotatea(curr,ro,col)

def rotatei(curr,ro,col):
    if curr[2].centerx>curr[0].centerx and curr[3].centerx>curr[0].centerx:
        horiz=True
        curr[0].centerx+=col
        bla=1
    elif curr[2].centerx<curr[0].centerx and curr[3].centerx<curr[0].centerx:
        horiz=True
        curr[0].centerx-=col
        bla=-1
    elif curr[2].centery>curr[0].centery and curr[3].centery>curr[0].centery:
        horiz=False
        curr[0].centery+=ro
        bla=-1
    elif curr[2].centery<curr[0].centery and curr[3].centery<curr[0].centery:
        horiz=False
        curr[0].centery-=ro
        bla=1
    for f in range (1,4):
        if horiz:
            curr[f].left=curr[0].left
            curr[f].top=curr[0].top+(blocks[0][f-1][0]*ro*bla)
        else:
            curr[f].top=curr[0].top
            curr[f].right=curr[0].right+(blocks[0][f-1][0]*col*bla)
def rotateo(curr,ro,col):
    pass

def rotatea(curr,ro,col):
    middlex=curr[0].centerx
    middley=curr[0].centery
    for r in range(1,4):
        if curr[r].centery==middley and curr[r].centerx>middlex:
            curr[r].centery+=ro
            curr[r].centerx-=col
        elif curr[r].centery==middley and curr[r].centerx<middlex:
            curr[r].centery-=ro
            curr[r].centerx+=col
        elif curr[r].centerx==middlex and curr[r].centery>middley:
            curr[r].centery-=ro
            curr[r].centerx-=col            
        elif curr[r].centerx==middlex and curr[r].centery<middley:
            curr[r].centery+=ro
            curr[r].centerx+=col            
        elif curr[r].centerx>middlex and curr[r].centery>middley:
            curr[r].centerx-=(2*col)
        elif curr[r].centery>middley and curr[r].centerx<middlex:
            curr[r].centery-=(2*ro)
        elif curr[r].centerx<middlex and curr[r].centery<middley:
            curr[r].centerx+=(2*col)
        elif curr[r].centerx>middlex and curr[r].centery<middley:
            curr[r].centery+=(2*ro)

def makenextpiece(block,startx,starty,row,column):
    return [pygame.Rect(startx,starty,column,row),pygame.Rect((block[0][0]*column)+startx,(block[0][1]*row)+starty,column,row),pygame.Rect((block[1][0]*column)+startx,(block[1][1]*row)+starty,column,row),pygame.Rect((block[2][0]*column)+startx,(block[2][1]*row)+starty,column,row),block[3]]

def nextpiece():
    nextpieces=[]
    for b in range (4):
        if b==0:
            newrowheight=WINDOWHEIGHT/20
            newcolumnwidth=WINDOWWIDTH/10
        else:
            newrowheight=WINDOWHEIGHT/40
            newcolumnwidth=WINDOWWIDTH/20
        nextpiece=makenextpiece(blocks[pieces[piece+b]],notplaywindow-(3*rowheight),startspoty+(rowheight*((3*b)+3)),newrowheight,newcolumnwidth)
        if nextpiece[4]!=cyan and newrowheight!=WINDOWWIDTH/20:
            rotate(nextpiece,newrowheight,newcolumnwidth)
        else:
            for i in range(4):
                nextpiece[i].left-=(newcolumnwidth/2)
        nextpieces.append(nextpiece)

    return nextpieces

def lineclear():
    bla=False
    numd=[]
    for d in reversed(range(20)):
        a=0
        for c in blockonscreen:
            for x in range(len(c)-1):
                if c[x].top==rowheight*d:
                    a+=1
        if a>=10:
            for c in blockonscreen:
                b=0
                for x in range(len(c)-1):
                    x=x-b
                    if c[x].top==rowheight*d:
                        c.remove(c[x])
                        b+=1
            bla=True
            for c in blockonscreen:
                for x in range(len(c)-1):
                    if c[x].top<rowheight*d:
                        c[x].top+=rowheight
            numd.append('')
            global points
            points+=10
            lineclear()
            break
    for bk in blockonscreen:
        if len(bk)==1:
            blockonscreen.remove(bk)
    return len(numd)

held=[]

def holdblock():
    newblock=0
    curb=''
    if len(held)==0:
        held.append(curblock[4])
        for i in range (7):
            if blocks[i][3]==held[0]:
                held.append(i)
                held.remove(held[0])
        blockonscreen.remove(curblock)

        newblock=1
    else:
        blockonscreen.append(makenewblock(blocks[held[0]]))
        held.remove(held[0])
        blockonscreen.remove(curblock)
        held.append(curblock[4])
        for i in range (7):
            if blocks[i][3]==held[0]:
                held.append(i)
                held.remove(held[0])
        curb=blockonscreen[len(blockonscreen)-1]
    return newblock,curb

pieces=shufflefirst()
piece=0
print (datetime.datetime.now())     

def triggerEnd():
    global a, b, c, d
    values = [a, b, c, d, points]
    L = str(values)
    L = "\n" + L[1:len(L)-1]
    print("Writing " + L + " to output file")
    global FILE
    FILE.write(L)
    reset()

    global trials, maxTrials
    if trials < maxTrials:
        global ai
        GeneticAlgorithm()
        ai = tetrai(a,b,c,d,1,columnwidth,rowheight)
        trials += 1
    else:
        FILE.close()

def reset():
    global pieces
    pieces=shufflefirst()
    global piece
    piece=0
    global held
    held=[]
    global blockonscreen
    blockonscreen=[]
    global points
    points=0
    global newblock
    newblock=1
    global fix
    fix=0
    global hi
    hi=0
    global blockmovecount
    blockmovecount=9

#AI GOES HERE
from AI.Tetrai import tetrai

#Genetic Algorithm being read from Text file for actual genetic variables
def GeneticAlgorithm():
    grid_data = []
    with open('Outputs.txt', 'r') as file:
        grid_data = [line.strip('\n').split(', ') for line in file.readlines()]

    v = 0
    while v < len(grid_data):
        if len(grid_data[v]) != 5:
            grid_data.pop(v)
        else:
            v += 1

    #Natural Selection (survival of the fittest)
    """
    f_mother = 0.0
    f_father = 0.0
    i_mother = 0
    i_father = 0
    for j in range(0, len(grid_data)):
        fitness = float(grid_data[j][4])
        if fitness > f_mother:
            i_father = i_mother
            f_father = f_mother        
            i_mother = j
            f_mother = fitness
    """
    #Random selection
    i_father = random.randint(0,len(grid_data) - 1)
    i_mother = random.randint(0,len(grid_data) - 1)
    while i_mother == i_father:
        random.randint(0,len(grid_data) - 1)

    global a, b, c, d
    a = (float(grid_data[i_mother][0]) + float(grid_data[i_father][0])) / 2.0
    b = (float(grid_data[i_mother][1]) + float(grid_data[i_father][1])) / 2.0
    c = (float(grid_data[i_mother][2]) + float(grid_data[i_father][2])) / 2.0
    d = (float(grid_data[i_mother][3]) + float(grid_data[i_father][3])) / 2.0

GeneticAlgorithm()
ai = tetrai(a,b,c,d,1,columnwidth,rowheight)

moves = Queue()

# run the game loop
while True:

    if (not moves.empty()):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,key=moves.get()))

    # check for the QUIT event
    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #moves piece
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for i in range(4):
                    curblock[i].left-=columnwidth
                    if curblock[i].left==-columnwidth:
                        fix=1
                    if overlap(curblock[i],blockonscreen):
                        fix=1
                if fix:
                    for i in range(4):
                        curblock[i].left+=columnwidth
                        fix=0
                ghost=makeghost()
            elif event.key == pygame.K_RIGHT:
                for i in range(4):
                    curblock[i].left+=columnwidth
                    if curblock[i].left==WINDOWWIDTH:
                        fix=1
                    if overlap(curblock[i],blockonscreen):
                        fix=1
                if fix:
                    for i in range(4):
                        curblock[i].left-=columnwidth
                        fix=0
                ghost=makeghost()
            elif event.key == pygame.K_UP:
                if rotatecheck(curblock,rowheight,columnwidth):
                    rotate(curblock,rowheight,columnwidth)
                    ghost=makeghost()
            elif event.key == pygame.K_DOWN:
                origblockmovecount=blockmovecount
                blockmovecount=2
            elif event.key == pygame.K_SPACE:
                harddrop()
                newblock=1
                hi=0
                ghost=ghost[4:]
            elif event.key == pygame.K_p:
                brea=False
                while True:
                    for event in pygame.event.get():
                        
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type==pygame.KEYDOWN:
                            brea=True
                    if brea:
                        break
            elif event.key == pygame.K_r:
                reset()

            elif event.key==pygame.K_RSHIFT or event.key==pygame.K_LSHIFT:
                n=holdblock()
                newblock=n[0]
                curblock=n[1]
                if curblock!='':
                    ghost=makeghost()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                blockmovecount=origblockmovecount
 

    # draw the black background onto the surface
    window.fill(BLACK)

    if newblock:
        ending=False
        newb = makenewblock(blocks[pieces[piece]])
        for bbbb in blockonscreen:
            for i in range(len(newb)-1):
                for j in range(len(bbbb)-1):
                    if newb[i].left == bbbb[j].left and newb[i].top == bbbb[j].top:
                        ending=True
                        triggerEnd()
                        break
        if ending:
            continue
        blockonscreen.append(newb)
        newblock=0
        curblock=blockonscreen[len(blockonscreen)-1]
        ghost=makeghost()
        piece+=1
        if piece==7:
            pieces=shuffle()
            piece=0
        nexpiece=nextpiece()
        print(points)
        moves = ai.calculateNewMove(blockonscreen,curblock,makenewblock(blocks[pieces[piece]]))
    if hi>=blockmovecount:
        for i in range(4):
            curblock[i].top+=(rowheight)
            if curblock[i].bottom>WINDOWHEIGHT:
                fix=1
                newblock=1
            if overlap(curblock[i],blockonscreen):
                fix=1
                newblock=1
        hi=0
    if fix:
        for i in range(4):
            curblock[i].top-=(rowheight)
            fix=0
        lineclear()

    for i in range (len(ghost)-1):
        pygame.draw.rect(window,ghost[len(ghost)-1],ghost[i])
    
    for block in blockonscreen:
        for i in range(len(block)-1):
            pygame.draw.rect(window,block[len(block)-1],block[i])
    
    for n in nexpiece:
        for i in range (4):
            pygame.draw.rect(window,n[4],n[i])



    if len(held)!=0:
        heldblock=makenextpiece(blocks[held[0]],notplaywindow-(columnwidth*3),WINDOWHEIGHT-(rowheight*3),rowheight,columnwidth)
        if heldblock[4]==cyan:
            blueswitch=columnwidth/2
            for i in range(4):
                heldblock[i].left-=(columnwidth/2)
        else:
            blueswitch=0
        for i in range (4):
            pygame.draw.rect(window,heldblock[4],heldblock[i])
        for i in range(4):
                pygame.draw.line(window,BLACK,(WINDOWWIDTH+blueswitch+((i+1)*columnwidth),rowheight*15),(WINDOWWIDTH+blueswitch+((i+1)*columnwidth),(rowheight*20)))

    for i in range (4):
        pygame.draw.line(window,BLACK,(WINDOWWIDTH+1,rowheight*(i+1)),(notplaywindow,rowheight*(i+1)))
    if nexpiece[0][4]==cyan:
        blueswitch=columnwidth/2
    else:
        blueswitch=0
    for i in range(4):
        pygame.draw.line(window,BLACK,(WINDOWWIDTH+blueswitch+((i+1)*columnwidth),0),(WINDOWWIDTH+blueswitch+((i+1)*columnwidth),(rowheight*4)))
    

    for i in range (1,10):
        pygame.draw.line(window, BLACK, (columnwidth*i,0),(columnwidth*i,WINDOWHEIGHT))
    for i in range (1,20):
        pygame.draw.line(window, BLACK, (0,rowheight*i),(WINDOWWIDTH,rowheight*i))
    pygame.draw.line(window, BLACK, (WINDOWWIDTH,rowheight*17),(notplaywindow,rowheight*17))
    pygame.draw.line(window, (255,255,255), (WINDOWWIDTH,0), (WINDOWWIDTH,WINDOWHEIGHT),4)
    hi+=1
    pygame.display.update()
    time.sleep(speed)
