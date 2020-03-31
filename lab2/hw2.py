'''
Homework 2b
@author: Carhat Eusebiu 
'''

import random
import math

#city class for TSP problem
class City:
        def __init__(self,nr,x,y):
                self.nr=nr;
                self.x=x;
                self.y=y;

        def getNr(self):
                return self.nr;
        def getX(self):
                return self.x;
        def getY(self):
                return self.y;
        
        #get euclidian dist from one city to another
        def distanceTo(self,city):
                xdist = abs(self.getX()-city.getX());
                ydist = abs(self.getY()-city.getY());
                dist = math.sqrt((xdist*xdist)+(ydist*ydist));
                return dist;

        def toString(self):
                return str(self.nr);
                

class TSP:
        def __init__(self,file,n,l):
                self.file=file
                self.n=n
                self.l=l
                self.outputFileName=file.split('.')[0]+".out"

        #print only indexes as solution
        def toString(self,tour):
                string=''
                for i in range(0,self.n):
                        string = string +tour[i].toString()+" "
                string = string+"\n"
                return string

        #generate solution by shuffle initial list
        def generateRandom(self):
                tour = self.l[:]
                random.shuffle(tour)
                return tour;

        #get city by index 
        def getCity(self,index):
                for i in range(0,self.n):
                        if(self.l[i].getNr()==index):
                                return self.l[i];

        def getTourDistance(self,tour):
                dist = 0
                for i in range(0,self.n-1):
                        dist=dist+tour[i].distanceTo(tour[i+1])
                #dist between last city and first from tour
                dist=dist+tour[self.n-1].distanceTo(tour[0])
                return dist;
                        
                
            

#find the neighbor by 2swap method
        def getNeighbor(self,c):
                r1=random.randrange(0,self.n)
                r2=random.randrange(0,self.n)
                while(r1==r2):
                        r2=random.randrange(0,self.n)
                c[r1],c[r2]=c[r2],c[r1]
                return c;

                

#Simulated Annealing algorithm
        def sa(self, T, alpha, minT, nrit):
                c = self.generateRandom();
                print("initial distance: %d"%(self.getTourDistance(c)))
                best=c[:];
                while(T>minT):
                        for i in range(0,nrit):
                                x = self.getNeighbor(c);
                                delta = self.getTourDistance(x)-self.getTourDistance(c);
                                if(delta<0):
                                        c=x[:];
                                elif(random.uniform(0,1)<math.exp(delta/T)):
                                        c=x[:];
                                if(self.getTourDistance(best)>self.getTourDistance(c)):
                                       best=c[:];        
                        T=alpha*T;
                print("best distance: %d"%(self.getTourDistance(best)))
                return best;

#run SA algorithm for n times and write a table report in file
        def run(self,n,T,alpha,minT,nrit):
                
                bestsol=self.sa(T,alpha,minT,nrit)
                bestd=self.getTourDistance(bestsol)
                sumd=bestd
                #add first solution in table
                with open(self.outputFileName,"a") as f:
                                f.write("|%d\t\t|%d\t|%d\t\t|%d\t\t\t|\n"% (1,self.getTourDistance(bestsol),bestd,sumd))
                #generate another n-1 sol and store avg/best sol
                for i in range(0,n-1):
                        #get solution from sa algorithm
                        x=self.sa(T,alpha,minT,nrit)
                        #store sum of distance to compute avg
                        sumd=sumd+self.getTourDistance(x);
                        #store best sol
                        if self.getTourDistance(x)<bestd:
                                bestd=self.getTourDistance(x)
                                bestsol=x[:];
                        #append sol to table
                        with open(self.outputFileName,"a") as f:
                                f.write("|%d\t\t|%d\t|%d\t\t|%d\t\t\t|\n"% (i+2,self.getTourDistance(x),bestd,sumd/(i+2)))
                with open(self.outputFileName,"a") as f:
                        f.write("--------------------------------------------\n")
                        f.write("|%d\t\t|\t\t|%d\t\t|%d\t\t\t|\n"% (n,bestd,sumd/n))
                        f.write(self.toString(bestsol)+"\n");
                        f.write("--------------------------------------------\n")
                
        
        def write_table_header(self,T,alpha,minT,nrit):
                with open(self.outputFileName,"a") as f:
                        f.write("For T="+str(T)+", alpha="+str(alpha)+", minT="+str(minT)+", nrit="+str(nrit)+"\n")
                        f.write("|-------------------------------------------|\n")
                        f.write("|Run\t|Dist\t|Best dist\t|Average\t\t|\n")
                        f.write("|-------------------------------------------|\n")
        
        
def main():
        try:
                file=input("Filename:")
                f=open(file,"r")
        except IOError:
                print("The file does not exist!")
                main()
        l=[]
        f.readline()
        f.readline()
        f.readline()
        #read nr of cities
        n=int(f.readline().split()[2])
        f.readline()
        f.readline()
        #for each city store index, x pos and y pos
        for i in range(0,n):
                line=f.readline()
                s=line.rstrip().split()
                s=list(map(int, s))
                c=City(s[0],s[1],s[2])
                l.append(c)
        #make new instance of problem
        tsp = TSP(file,n,l);
        #empty file
        open(tsp.outputFileName,"w").close()
        
        #tsp.write_table_header(10000,0.9,1,10);
        #tsp.run(20,10000,0.9,1,10);
        #tsp.write_table_header(10000,0.999,0.001,10);
        #tsp.run(3,10000,0.999,0.001,10);
        tsp.write_table_header(10000,0.9999,0.00001,100);
        tsp.run(2,10000,0.9999,0.00001,100);
        
        
        
main()
