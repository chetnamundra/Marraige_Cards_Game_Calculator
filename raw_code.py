n = int(input("Enter the number of players : "))

d={}
for i in range(n):
    name=input("Enter player {} name : ".format(i+1))
    d[i]=[name,[]]

r=0
while True:
    tm=0
    tp=0
    for i in d:
        m=int(input("Enter player {}  Maal : ".format(d[i][0])))
        p=int(input("Enter player {}  Points : ".format(d[i][0])))
        d[i][1].append([m,p,0,0])
        tm+=m
    cp=input("Enter the player who closed the game : ")

    for i in d:
        if d[i][0]==cp:
            cp=i
            break
    #to calculate round ka points
    for i in d:
        if i == cp:
            pass
        else:
            d[i][1][r][2]=(d[i][1][r][0]*n)-(tm+d[i][1][r][1])
            tp+=d[i][1][r][2]
    d[cp][1][r][2]=-tp

    #to calculate final points
    for i in d:
        if r==0:
            d[i][1][r][3]=d[i][1][r][2]
        else:
            d[i][1][r][3]=d[i][1][r-1][3]+d[i][1][r][2]
    
    for i in d:
        print(d[i])
    r+=1
    k=int(input("Do you want to continue (0/1)? : "))
    if k==0:
        break
