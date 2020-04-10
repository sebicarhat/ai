'''
Homework 3
@author: Carhat Eusebiu 
'''

import random

#keep solution with its attributes
class Solution:
        def __init__(self,sol,v,w):
                #solution itself
                self.sol=sol
                #value
                self.v=v
                #weight
                self.w=w
                
        def getSol(self):
                return self.sol;

        def __getitem__(self,index):
                return self.sol[index]

        def __setitem__(self,index,value):
            self.sol[index] = value

        def setValue(self,x):
                self.v=x;
        
        def getValue(self):
                return self.v;

        def setWeight(self,x):
                self.w=x;

        def getWeight(self):
                return self.w;
                
#the class for backpack problem with evolutive algorithm
class BackpackEAP:
        def __init__(self,n,l,w):
                #nr of all things that we have
                self.n=n
                #list with their values and weight
                self.l=l
                #max weight of backpack
                self.w=w
                self.outputFileName=str(n)+"_input_data.out"

        #get random solution (base2 nr)
        def randomSol(self):
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

        #generate valid solution
        def generateValidSol(self):
                x=self.randomSol()
                w=self.fitness(x)
                v=self.eval(x)
                while w>self.w:
                        x=self.randomSol()
                        w=self.fitness(x)
                        v=self.eval(x)
                return Solution(x,v,w);
            
        #get weight of sol
        def fitness(self,x):
                w=0
                for i in range(0,self.n):
                        w=w+self.l[i][2]*x[i]
                return w;

        #get value of solution
        def eval(self,x):
                w=0
                for i in range(0,self.n):
                        w=w+self.l[i][1]*x[i]
                return w;
        
        #generate population of N individuals from random valid solutions
        def populate(self,N):
                p=[]
                for i in range(0,N):
                        p.append(self.generateValidSol())
                return p;
        
        #for strong mutation
        def flip(self,bit):
                if(bit==0):
                        return 1;
                else:
                        return 0;
                
        #mutation algorithm(strong/weak)
        #get a population
        #return new population resulted by mutation
        def mutation(self,p,pm,type):
                l=len(p)
                x=[]
                #for each individuals for population received
                for i in range(0,l):
                        #take default invalid solution(with weight above max) to entry in while
                        x.append(Solution([],0,self.w+1))
                        while(x[i].getWeight()>self.w):
                                x[i].sol=[]
                                for j in range(0, self.n):
                                        #set each bit
                                        q=random.uniform(0,1)
                                        if(q<pm):
                                                x[i].sol.append(self.flip(p[i].sol[j]) if type=="strong" else random.choice([0,1]))
                                        else:
                                                x[i].sol.append(p[i].sol[j])
                                #compute value and weight of sol
                                x[i].setValue(self.eval(x[i].sol))
                                x[i].setWeight(self.fitness(x[i].sol))
                return x;
        
        #cross algorithm(uniform/point)
        #get parents population
        #return childrens population
        def cross(self,parents,type):
                l = len(parents)
                childrens=[Solution([],0,0)]
                #take pair of 2 parents
                for i in range(0,l-1,2):
                        p1=parents[i]
                        p2=parents[i+1]
                        #for each pair generate 2 childrens by chosen method
                        if(type=="uniform"):
                                c1,c2=self.uniformCross(p1,p2,0.3)
                        elif(type==" point "):
                                c1,c2=self.pointCross(p1,p2)

                        childrens.append(c1)
                        childrens.append(c2)
                del childrens[0]
                return childrens

        def uniformCross(self,p1,p2,pm):
                c1=Solution([],0,self.w+1)
                c2=Solution([],0,self.w+1)
                #only valid solutions
                while(c1.getWeight()>self.w):
                        c1.sol=[]
                        for i in range(0,self.n):
                                q=random.uniform(0,1)
                                if(q<pm):
                                        c1.sol.append(p1.sol[i])
                                else:
                                        c1.sol.append(p2.sol[i])
                        c1.setWeight(self.fitness(c1.sol))
                        c1.setValue(self.eval(c1.sol))
                        
                #to short the time verify the solutions separately
                while(c2.getWeight()>self.w):
                        c2.sol=[]
                        for i in range(0,self.n):
                                q=random.uniform(0,1)
                                if(q<pm):
                                        c2.sol.append(p2.sol[i])
                                else:
                                        c2.sol.append(p1.sol[i])
                        c2.setWeight(self.fitness(c2.sol))
                        c2.setValue(self.eval(c2.sol))
                        
                return c1,c2

        def pointCross(self,p1,p2):
                c1=Solution([],0,self.w+1)
                c2=Solution([],0,self.w+1)
                #only valid solutions
                while(c1.getWeight()>self.w or c2.getWeight()>self.w):
                        k=random.randrange(0,self.n)
                        c1.sol[:k]=p1.sol[:k]
                        c1.sol[k:]=p1.sol[k:]
                        c2.sol[:k]=p2.sol[:k]
                        c2.sol[k:]=p2.sol[k:]
                        
                        c1.w=self.fitness(c1.sol)
                        c1.v=self.eval(c1.sol)
                        c2.w=self.fitness(c1.sol)
                        c2.v=self.eval(c1.sol)
                return c1,c2;

        def turnir(self,p):
                bestSol=p[0]
                bestIndex=0
                nr=10
                #if don't have enough parents select from how many remained
                if(len(p)<10):
                        nr=len(p)
                                
                #selecting best parent from 10 or less individuals
                for i in range(0,nr):
                        x=random.randrange(0,len(p))
                        if(p[x].getValue()>bestSol.getValue()):
                                bestSol=Solution(p[x],p[x].getValue(),p[x].getWeight())
                                bestIndex=i
                return bestSol, bestIndex;
                                        
        def selectParents(self,p):
                #will be n/2 pair of parents
                n=len(p)
                parents=[]
                for i in range(0,int(n/2)):
                        #select first parent by turnir method
                        bestSol, bestIndex = self.turnir(p)
                        parents.append(bestSol)
                        #remove selected parent from population to not select again
                        del p[bestIndex]
                        #select second parent random
                        x=random.randrange(0,len(p))
                        parents.append(p[x])
                        del p[x]
                return parents

        def survivalSelection(self,p,px,pm,N):
                l=p[:]
                for i in range(0,len(px)):
                        l.append(px[i])
                for i in range(0,len(pm)):
                        l.append(pm[i])
                #sorting all poulation(parents+desc+mutations) desc by fitness
                l.sort(key=lambda x: x.v, reverse=True)
                #select 20% of population by fitness
                population=l[:int(N/5)]
                del l[:int(N/5)]
                #select another 80% by turnir method
                n=N-int(N/5)
                for i in range(0,n):
                        bestSol, bestIndex = self.turnir(l)
                        #remove selected parent from population
                        population.append(bestSol)
                        del l[bestIndex]
                return population          

        #evolutive algorithm
        def ea(self,N,M,crossType,mutationType):
                t=0
                p = self.populate(N)
                while(t<M):
                        parents = self.selectParents(p)
                        px = self.cross(parents,crossType)
                        pm = self.mutation(px,0.3,mutationType)
                        p = self.survivalSelection(parents,px,pm,N)
                        t=t+1
                #return best individual from actual population
                p.sort(key=lambda x: x.v, reverse=True)
                return p[0]
                
        #run EA algorithm with different param for n times and write a table report in file
        def run(self,n,N,M,crossType,mutationType):
                best=self.ea(N,M,crossType,mutationType)
                sum=0
                for i in range(0,n):
                        sol=self.ea(N,M,crossType,mutationType)
                        sum=sum+self.eval(sol.sol)
                        if self.eval(sol.sol)>self.eval(best.sol):
                                best=sol
                with open(self.outputFileName,"a") as f:
                        f.write("|%d\t\t|%d\t\t|%d\t|%s\t|%s\t\t\t|%d\t\t|%d\t\t|\n"% (n,N,M,crossType,mutationType,self.eval(best.sol),sum/n))
                        f.write("----------------------------------------------------------------------------\n")

        def write_table_header(self):
                with open(self.outputFileName,"w") as f:
                        f.write("|---------------------------------------------------------------------------|\n")
                        f.write("|Runs\t|N\t\t|M\t\t|cross type\t|mutation type\t|Best value\t|Average\t|\n")
                        f.write("|---------------------------------------------------------------------------|\n")
        
        
def main():
        stop=False
        while(stop==False):
                x=int(input("Choose\n1. for read from file\n0. for exit\n"))
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
                elif x==0:
                        stop=True
                else:
                        print("Enter a valid nr\n")
                        main()
                if stop==False:
                        bp = BackpackEAP(n,l,w)
                        print("Backpack max weight: "+str(bp.w)+"\n")
                        bp.write_table_header()
                        bp.run(10,10,100,"uniform","strong")
                        bp.run(10,10,100,"uniform","weak")
                        bp.run(10,10,100," point ","strong")
                        bp.run(10,10,100," point ","weak")
                        bp.run(10,10,1000,"uniform","strong")
                        bp.run(10,10,1000,"uniform","weak")
                        bp.run(10,10,1000," point ","strong")
                        bp.run(10,10,1000," point ","weak")	
main()
