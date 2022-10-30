start = int(input("start: "))
delta = int(input("delta: "))
row = int(input("row: "))

def sumPart(n):
    du=0
    sum=0
    while (n>0):
        du=int(n%10)
        n=int(n/10)
        sum=sum+du
    return sum

array=[]
start=sumPart(start)
print(start)
for i in range(0,row-1):
    for j in range(0,i+2):
        start=start+delta
        if(start<=9):
            print(start,end=" ")
        else:
            start=sumPart(start)
            print(start,end=" ")
    print("hello")


