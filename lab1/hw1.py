'''
Homework 2b
@author: Carhat Eusebiu 
'''

import random

class Backpack:
        def __init__(self,n,l,w):
                self.n=n
                self.l=l
                self.w=w
                self.outputFileName=str(n)+"_input_data.out"

#get random base2 nr
        def randomNr(self):
                l=[]
                for i in range(0,self.n):
                        l.append(0)
                d=pow(2,self.n)-1
                number=random.randrange(0,d)
                i=0
                while(number):
                        bit=int(number)%2
                        l[i]=bit
                        number=int(number/2)
                        i+=1
                l.reverse()
                return l
            
#get weight of sol
        def fitness(self,x):
                w=0
                for i in range(0,self.n):
                        w=w+self.l[i][2]*x[i]
                return w

#get max value of elems from input
        def maxValue(self):
            sum=0
            for i in range(0,self.n):
                sum=sum+self.l[i][1]
            return sum

#get value of solution
        def valueSum(self,x):
                w=0
                for i in range(0,self.n):
                        w=w+self.l[i][1]*x[i]
                return w

#get random solution
        def generateRandSol(self):
                x=self.randomNr()
                w=self.fitness(x)
                v=self.valueSum(x)
                while w>self.w:
                        x=self.randomNr()
                        w=self.fitness(x)
                        v=self.valueSum(x)
                return x,w,v;

#determine best solution from k random solutions
        def generate(self,k):
                x,w,v = self.generateRandSol()
                bestx=x
                bestw=w
                bestv=v
                for i in range(0,k):
                        x,w,v = self.generateRandSol()
                        if v>bestv:
                                bestx=x
                                bestw=w
                                bestv=v
                return bestw,bestx,bestv

#find best neighbor from one solution
        def best_neighbor(self,x):
                best=x[:]
                for i in range(0,self.n):
                        aux=x[:]
                        if aux[i]==0:
                                aux[i]=1
                        if self.valueSum(aux)>self.valueSum(best) and self.fitness(aux)<self.w:
                                best=aux[:]
                                
                return best;

#SAHC algorithm
        def sahc(self,k):
                c,w,v = self.generateRandSol()
                best_c=c[:]
                for i in range(0,k):
                        x = self.best_neighbor(c)
                        if self.valueSum(x)>self.valueSum(c):
                                c=x[:]
                                w=self.fitness(x)
                                v=self.valueSum(x)
                        elif self.valueSum(best_c)<self.valueSum(c):
                                best_c=c[:]
                                w=self.fitness(c)
                                v=self.valueSum(c)
                                c,w,v=self.generateRandSol()
                return best_c,w,v;

#run SAHC algorithm with param k for n times and write a table report in file
        def run(self,n,k):
                bestv=0
                avgv=0
                for i in range(0,n):
                        sol,solw,solv=self.sahc(k)
                        avgv=avgv+solv
                        if solv>bestv:
                                bestv=solv
                                bestsol=sol
                        with open(self.outputFileName,"a") as f:
                                f.write("|%d\t\t|%d\t|%d\t|%d\t\t|%d\t\t\t|\n"% (i+1,k,solv,bestv,avgv/(i+1)))
                with open(self.outputFileName,"a") as f:
                        f.write("----------------------------------------------------\n")
                        f.write("|%d\t\t|%d\t|\t\t|%d\t\t|%d\t\t\t|\n"% (i+1,k,bestv,avgv/(i+1)))
                        f.write("----------------------------------------------------\n")
                
        

        def write_table_header(self):
                open(self.outputFileName,"w").close()
                with open(self.outputFileName,"w") as f:
                        f.write("|---------------------------------------------------|\n")
                        f.write("|Run\t|k\t\t|Value\t|Best value|Average\t\t\t|\n")
                        f.write("|---------------------------------------------------|\n")
        
        
def main():
        stop=False
        while(stop==False):
                x=int(input("Choose\n1. for read from file\n2. for keyboard input\n0. for exit\n"))
                if x==1:
                        try:
                                s=input("Filename:")
                                f=open(s,"r")
                        except IOError:
                                print("The file does not exist!")
                                main()
                        l=[]
                        n=int(f.readline())
                        for i in range(0,n):
                                line=f.readline()
                                s=line.split()
                                s=list(map(int, s))
                                l.append(s)
                        w=int(f.readline())
                elif x==2:
                        n=input("Nr of objects:")
                        for i in range(0,n):
                                l[i][0]=i
                                l[i][1]=input("Value:")
                                l[i][2]=input("Weight:")
                        w=input("Max weight")
                elif x==0:
                        stop=True
                else:
                        print("Enter a valid nr\n")
                        main()
                if stop==False:
                        bp = Backpack(n,l,w)
                        print("Value of all elems: "+str(bp.maxValue())+"\n")
                        print("Backpack max weight: "+str(bp.w)+"\n")
                        x,w,v=bp.generateRandSol()
                        print("Random solution:"+str(x))
                        print("Value:"+str(v))
                        print("Fitness:"+str(w))
                        bestf,bestx,minc=bp.generate(10000)
                        print("Best solution:"+str(bestx))
                        print("Value:"+str(minc))
                        print("Fitness:"+str(bestf))
                        bp.write_table_header()
                        bp.run(10,100)
                        bp.run(10,1000)
	
main()
