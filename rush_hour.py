from z3 import *
import numpy

#Read the input file
file1 = open(sys.argv[1], "r+")
Lines = file1.readlines()

data = (Lines[0].split(','))
n = int(data[0]) #Get Dimension of the Board
max_steps = int(data[1].strip()) #Get Maximum number of moves
# print(n,max_steps)

#Get Position of the Red Car
redline = (Lines[1].split(',')) 
r_i = int(redline[0])
r_j = int(redline[1].strip())

red={}
red[r_i]=[[]]
red[r_i][0].append(r_j)
# print(r_i,r_j)

#Get Information on the horizontal/vertical cars and mines
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

# print("end71")

##Initialise solver..
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

# print("125")
#Red-Vertical
for timestamp in range(1, max_steps+1):
    # red[r_i][t][0] will give column number of red car at timestamp t
    for vertColumn in vertical:
        for row in vertical[vertColumn][timestamp]:
            s.add(Or(r_i != row, red[r_i][timestamp][0] != vertColumn))
            s.add(Or(r_i != row, red[r_i][timestamp][0]+1 != vertColumn))
            s.add(Or(r_i != row+1, red[r_i][timestamp][0] != vertColumn))
            s.add(Or(r_i != row+1, red[r_i][timestamp][0]+1 != vertColumn))

# print("136")

#Horizontal-Horizontal
for rownumber,carlistbytime in horizontal.items():
    for carlist in carlistbytime:
        for car in carlist:
            for car1 in carlist:
# print("hhend")
                s.add((car1+1)!=car, car1!=(car+1))
# print("145")
#Red-Horizontal
for rownumber,carlistbytime in horizontal.items():
    if(rownumber == r_i):
        for carlist in carlistbytime:
            for car in carlist:
                for redcar in red[r_i]:
# print("rhend")
                    s.add((redcar[0]+1)!=car, redcar[0]!=(car+1))
# print("154")
###Horizontal-Vertical
############################################################################
for time in range(1, max_steps+1):
    for row in horizontal:
        for col in horizontal[row][time]:
            for col2 in vertical:
                for row2 in vertical[col2][time]:
                    s.add(Or(row2+1!=row, col2 != col))
                    s.add(Or(row2!=row, col2!=col))
                    s.add(Or(row2+1!=row2, col2!=col+1))
                    s.add(Or(row2!=row, col2!= col+1))
# print("end166")
##Step contraint
##Initialising movement variables
hm_bools={} #Horizontal movement bools
vm_bools={} #Vertical movement bools
red_bools={} #Red Car movement bools

for row in horizontal:
    # print("end5")
    hm_bools[row]=[[Bool("hb%s%s%s"%(row,t,m)) for m in range(len(horizontal[row][0]))]for t in range(max_steps)]
    # for t in range(max_steps):
    #     hm_bools[row].append([Bool("hb%s%s%s"%(row,t,m)) for m in range(len(horizontal[row][0]))])
#print(horizontal)  
#print(hm_bools)

for col in vertical:
    # print("end4")
    vm_bools[col]=[[Bool("vb%s%s%s"%(col,t,m)) for m in range(len(vertical[col][0]))]for t in range(max_steps)]
    #vm_bools[col]=[[]]
    # for t in range(max_steps):
    #     vm_bools[col].append([Bool("vb%s%s%s"%(col,t,m)) for m in range(len(vertical[col][0]))])        
#print(vertical)

red_bools[r_i]=[[Bool("rb%s"%t)]for t in range(max_steps)]
# for t in range(max_steps):
#     red_bools[r_i].append([Bool("rb%s"%t)])
   
## One Step at a time constraint
for t in range(max_steps):
    timestep=[]
    for row in horizontal:
        #print(len(horizontal[3]))
        #print(len(hm_bools[3]))
        for car in  range(len(horizontal[row][t])):
            # print("end3")
            s.add(And(horizontal[row][t+1][car]-horizontal[row][t][car]<=1,horizontal[row][t+1][car]-horizontal[row][t][car]>=-1))
            hm_bools[row][t][car]=horizontal[row][t+1][car]!=horizontal[row][t][car]
            timestep.append(horizontal[row][t+1][car]!=horizontal[row][t][car])
            # timestep.append(hm_bools[row][t][car])

    for col in vertical:
        for car in  range(len(vertical[col][t])):
            # print("end2")
            s.add(And(vertical[col][t+1][car]-vertical[col][t][car]<=1,vertical[col][t+1][car]-vertical[col][t][car]>=-1))
            vm_bools[col][t][car]=vertical[col][t+1][car]!=vertical[col][t][car]
            # timestep.append(vm_bools[col][t][car])
            timestep.append(vertical[col][t+1][car]!=vertical[col][t][car])
    
    red_bools[r_i][t][0]=red[r_i][t+1][0]!=red[r_i][t][0]
    s.add(And(red[r_i][t+1][0]-red[r_i][t][0]<=1,red[r_i][t+1][0]-red[r_i][t][0]>=-1))
    # timestep.append(red_bools[r_i][t][0])
    timestep.append(red[r_i][t+1][0]!=red[r_i][t][0])  
    Atleast1=Or(timestep)

    for i in range(len(timestep)):
        for j in range(i):
            s.add(Or(Not(timestep[i]), Not(timestep[j])))
            # print("end1")
        
    s.add(Atleast1)


###Winning constraints
agg=[]
for t in range(0,max_steps+1):
    agg.append(red[r_i][t][0]==n-2)
F1=Or(agg)
#print(F1)
s.add(F1)

# print("end")


###Solver
r=s.check()
# m=s.model()
if r==sat:
    # print("Sjrre")
    m=s.model()
    # print(m)

    for t in range(max_steps):    
        stepcheck=False

        for row in horizontal:
            list1=[]
            list2=[]

            for i in range(len(horizontal[row][t])):

                if t!=0:
            
                    list1.append(int(str(m.evaluate(horizontal[row][t][i]))))
                    list2.append(int(str(m.evaluate(horizontal[row][t+1][i]))))

                else:
                    list1.append(int(str((horizontal[row][t][i]))))
                    list2.append(int(str(m.evaluate(horizontal[row][t+1][i]))))


            for i in range(len(list1)):
                #print(list1[i])
                #print(list2[i])
                if((list1[i]) != (list2[i])):
                    stepcheck=True
                    print("here")
                    if(list1[i]>list2[i]):
                        print(str(row) + ","+str(list1[i]))
                        break
                    else:
                        print(str(row)+","+ str(list2[i]))
                        break
                if(stepcheck == True):
                    break
        # if(stepcheck == True):
        #     break  


        for column in vertical:
            list1=[]
            list2=[]

            for i in range(len(vertical[column][t])):
                if t!=0:

                    list1.append(int(str(m.evaluate(vertical[column][t][i]))))
                    list2.append(int(str(m.evaluate(vertical[column][t+1][i]))))

                else:
                     list1.append(int(str((vertical[column][t][i]))))
                     list2.append(int(str(m.evaluate(vertical[column][t+1][i]))))


            
            for i in range(len(list1)):

                if((list1[i]) != (list2[i])):
                    stepcheck=True
                    if(list2[i]>list1[i]):
                        print(str(list2[i])+ ","+str(column))
                        break
                    else:
                        print(str(list1[i])+","+str(column))
                        break
                if(stepcheck == True):
                    break

        # if(stepcheck == True):
        #     break    

        for row in red:
            list1=[]
            list2=[]

            for i in range(len(red[row][t])):
                if t!=0:

                    list1.append(int(str(m.evaluate(red[r_i][t][i]))))
                    list2.append(int(str(m.evaluate(red[r_i][t+1][i]))))

                else:
                    list1.append((((red[r_i][t][i]))))
                    list2.append(int(str(m.evaluate(red[r_i][t+1][i]))))
                

            for i in range(len(list1)):
                if(list1[i] != list2[i]):
                    stepcheck=True
                    if(list1[i]>list2[i]):
                        print(str(row)+","+str(list1[i]))
                        if(list1[i]==n-2):
                            exit()
                        break
                    else:
                        print(str(row)+","+str(list2[i]))
                        if(list2[i]==n-2):
                            exit()
                        break
                if(stepcheck == True):
                    break
        # if(stepcheck == True):
        #     break

else:
    print("unsat")



####################################################################################iske NICHE DALNA
# for t in range(max_steps):    
#     stepcheck=False
#     for row in horizontal:
#         list1=[]
#         list2=[]
#         for i in range(len(horizontal[row][t])):
#             # print(m[horizontal[row][t][i]].as_long())
#             list1.append(is_int_value(m[(horizontal[row][t][i])]))
#             list2.append(is_int_value(m[(horizontal[row][t+1][i])]))
#         for i in range(len(list1)):
#             if(list1[i] != list2[i]):
#                 stepcheck=True
#                 if(list1[i]>list2[i]):
#                     print(str(row) + ","+str(list1[i]))
#                     break
#                 else:
#                     print(str(row)+","+ str(list2[i]))
#                     break
#         if(stepcheck == True):
#             break
#     for column in vertical:
#         list1=[]
#         list2=[]
#         for i in range(len(horizontal[row][t])):
#             list1.append(is_int_value(m[(vertical[row][t][i])]))
#             list2.append(is_int_value(m[(vertical[row][t+1][i])]))
#         for i in range(len(list1)):
#             if(list1[i] != list2[i]):
#                 stepcheck=True
#                 if(list2[i]>list1[i]):
#                     print(str(list1[i])+ ","+str(column))
#                     break
#                 else:
#                     print(str(list2[i])+","+str(column))
#                     break
#     if(stepcheck == True):
#         break

#     for row in red:
#         list1=[]
#         list2=[]
#         for i in range(len(red[row][t])):
#             list1.append(is_int_value(m[(red[row][t][i])]))
#             list2.append(is_int_value(m[(horizontal[row][t+1][i])]))
#         for i in range(len(list1)):
#             if(list1[i] != list2[i]):
#                 stepcheck=True
#                 if(list1[i]>list2[i]):
#                     print(str(row)+","+str(list1[i]))
#                     break
#                 else:
#                     print(str(row)+","+str(list2[i]))
#                     break
#     if(stepcheck == True):
#         break
