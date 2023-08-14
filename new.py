from z3 import *
import numpy

#Read the input file
file1 = open(sys.argv[1], "r+")
Lines = file1.readlines()

data = (Lines[0].split(','))
n = int(data[0]) #Get Dimension of the Board
max_steps = int(data[1].strip()) #Get Maximum number of moves
# print(n,max_steps)

redline = (Lines[1].split(',')) #Get Position of the Red Car
r_i = int(redline[0])
r_j = int(redline[1].strip())

red={}
red[r_i]=[[]]
red[r_i][0].append(r_j)
# print(r_i,r_j)

#Get Information on the horizontal/vertical cars and mines
# h_count = 0
# v_count = 0
# mine_count = 0
##
vertical={}
horizontal={}
mines = []

##Store the positions of the cars and mines 

i = 2
while i<len(Lines):
    l = (Lines[i].split(','))
    # print(l)
    i1 = int(l[1])
    # print(i1)
    j1 = int(l[2].strip())
    # print(j1)
    if(int(l[0]) == 0):
        if j1 in vertical:
            vertical[j1][0].append(i1)
        else:
            vertical[j1]=[[]]
            vertical[j1][0].append(i1)   
    if(int(l[0]) == 1):
        if i1 in horizontal:
            horizontal[i1][0].append(j1)
        else:
            horizontal[i1]=[[]]
            horizontal[i1][0].append(j1)
    if(int(l[0]) == 2):
        mines.append((int(l[1]), int(l[2].strip())))
    i += 1

###Initialising variables
for row in horizontal:
    # print(row)
    for t in range(1,max_steps+1):
        horizontal[row].append([Int("h%s,%s,%s"%(row,t,m)) for m in range(len(horizontal[row][0]))])
#print(horizontal)
for col in vertical:
    for t in range(1,max_steps+1):
        vertical[col].append([Int("v,%s,%s,%s"%(col,t,m)) for m in range(len(vertical[col][0]))])        
#print(vertical)

for t in range(1, max_steps+1):
    red[r_i].append([Int("r%s"%t)])


##Init solver..
s=Solver()

###Boundary Constraints
##Horizontal
for row in horizontal:
    for t in range(1,max_steps+1):
        for car in range(len(horizontal[row][t])):
            s.add(horizontal[row][t][car]>=0,horizontal[row][t][car]<n-1)

##Vertical
for col in vertical:
    for t in range(1,max_steps+1):
        for car in range(len(vertical[col][t])):
            s.add(vertical[col][t][car]>=0,vertical[col][t][car]<n-1)
##Red Car            
for t in range(1,max_steps+1):
    s.add(red[r_i][t][0]>=0,red[r_i][t][0]<n-1)

###OverLapping constraints
##Mine Overlap
#Red Car
for point in mines:
    for redcar in red[r_i]:
        cond1 = Or((point[0]!=r_i),(point[1]!=redcar[0]))
        cond2 = Or((point[0]!=r_i),(point[1]!=(redcar[0]+1)))
        s.add(cond1,cond2)

#Horizontal Car
for point in mines:
    for rownumber,carlistbytime in horizontal.items():
        for carlist in carlistbytime:
            for car in carlist:
                cond1 = Or((point[0]!=rownumber),(point[1]!=car))
                cond2 = Or((point[0]!=rownumber),(point[1]!=(car+1)))
                s.add(cond1,cond2)

#Vertical Car
for point in mines:
    for colnumber,carlistbytime in vertical.items():
        for carlist in carlistbytime:
            for car in carlist:
                cond1 = Or((point[0]!=car),(point[1]!=colnumber))
                cond2 = Or((point[0]!=car+1),(point[1]!=colnumber))
                s.add(cond1,cond2)

##Car Overlaps
#Vertical-Vertical
for colnumber,carlistbytime in vertical.items():
    for carlist in carlistbytime:
        for car in carlist:
            for car1 in carlist:
                    s.add((car1+1)!=car, car1!=(car+1))
                    # 

#Red-Vertical
# for colnumber,carlistbytime in vertical.items():
#     for carlist in carlistbytime:
#         for car in carlist:
#             for redcar in red[r_i]:
#                 s.add(Implies(Or((colnumber == redcar[0]),(colnumber == (redcar[0]+1))), And(r_i!=car, (r_i+1)!=car, r_i!=(car+1))))

#New Red-Vertical
for timestamp in range(1, max_steps+1):
    # red[r_i][t][0] will give column number of red car at timestamp t
    for vertColumn in vertical:
        for row in vertical[vertColumn][timestamp]:
            s.add(Or(r_i != row, red[r_i][timestamp][0] != vertColumn))
            s.add(Or(r_i != row, red[r_i][timestamp][0]+1 != vertColumn))
            s.add(Or(r_i != row+1, red[r_i][timestamp][0] != vertColumn))
            s.add(Or(r_i != row+1, red[r_i][timestamp][0]+1 != vertColumn))



#Horizontal-Horizontal
for rownumber,carlistbytime in horizontal.items():
    for carlist in carlistbytime:
        for car in carlist:
            for car1 in carlist:
                 s.add((car1+1)!=car, car1!=(car+1))

#Red-Horizontal
for rownumber,carlistbytime in horizontal.items():
    if(rownumber == r_i):
        for carlist in carlistbytime:
            for car in carlist:
                for redcar in red[r_i]:
                    s.add((redcar[0]+1)!=car, redcar[0]!=(car+1))

###Horizontal-Vertical
############################################################################
for rownumber,rowcarlistbytime in horizontal.items():
    for rowcarlist in rowcarlistbytime:
        for rowcar in rowcarlist:
            for colnumber,colcarlistbytime in vertical.items():
                for colcarlist in colcarlistbytime:
                    for colcar in colcarlist:
                        s.add(Or(rownumber!=colcar, colnumber!=rowcar))
                        s.add(Or(rownumber!=colcar, colnumber!=rowcar+1))
                        s.add(Or(rownumber-1!=colcar, colnumber!=rowcar))
                        s.add(Or(rownumber-1!=colcar, colnumber!=rowcar+1))


move_bools = []

for timestamp in range(max_steps):
    for row in horizontal:
        for i in range(len(horizontal[row][timestamp])):
            move_bool.


##Step contraint
##Initialising movement variables
# hm_bools={}#Horizontal movement bools
# vm_bools={}
# red_bools={}
# for row in horizontal:
#     hm_bools[row]=[[Bool("hb%s%s%s"%(row,t,m)) for m in range(len(horizontal[row][0]))]for t in range(max_steps)]
#     # for t in range(max_steps):
#     #     hm_bools[row].append([Bool("hb%s%s%s"%(row,t,m)) for m in range(len(horizontal[row][0]))])
# #print(horizontal)  
# #print(hm_bools)
# for col in vertical:
#     vm_bools[col]=[[Bool("vb%s%s%s"%(col,t,m)) for m in range(len(vertical[col][0]))]for t in range(max_steps)]

#     #vm_bools[col]=[[]]
#     # for t in range(max_steps):
#     #     vm_bools[col].append([Bool("vb%s%s%s"%(col,t,m)) for m in range(len(vertical[col][0]))])        
# #print(vertical)

# red_bools[r_i]=[[Bool("rb%s"%t)]for t in range(max_steps)]
# # for t in range(max_steps):
# #     red_bools[r_i].append([Bool("rb%s"%t)])
   
# for t in range(max_steps):
#     timestep=[]
#     for row in horizontal:
#         #print(len(horizontal[3]))
#         #print(len(hm_bools[3]))
#         for car in  range(len(horizontal[row][t])):
#             hm_bools[row][t][car]=Or(horizontal[row][t+1][car]-horizontal[row][t][car]==1,horizontal[row][t+1][car]-horizontal[row][t][car]==-1)
#             timestep.append(hm_bools[row][t][car])

#     for col in vertical:
#         for car in  range(len(vertical[col][t])):
#            vm_bools[col][t][car]=Or(vertical[col][t+1][car]-vertical[col][t][car]==1,vertical[col][t+1][car]-vertical[col][t][car]==-1)
#            timestep.append(vm_bools[col][t][car])
#     red_bools[r_i][t][0]=Or(red[r_i][t+1][0]-red[r_i][t][0]==1,red[r_i][t+1][0]-red[r_i][t][0]==-1)
#     timestep.append(red_bools[r_i][t][0])
    
#     Atleast1=Or(timestep)
#     timestep.append(1)
#     Atmost1=AtMost(timestep)
#     s.add(And(Atleast1,Atmost1))



###Winning constraints
agg=[]
for t in range(0,max_steps+1):
    agg.append(red[r_i][t][0]==n-2)
F1=Or(agg)
#print(F1)
s.add(F1)


###Solver
r=s.check()
if r==sat:

    m=s.model()
    print(m)
else:
    print("unsat")








