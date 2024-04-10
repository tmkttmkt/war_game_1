import random
i=100
list=[0,0,0,0,0,0,0,0,0,0]
while i>0:
    ex=random.randint(1,10)
    list[ex-1]+=1
    print(ex)
    i-=1
print()
print(list)