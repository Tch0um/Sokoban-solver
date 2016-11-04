



class chemin:
    def __init__(self,nodes, totalCost):
        self.nodes = chemin;
        self.totalCost = totalCost;

    def getnoeuds(self): 
        return self.nodes    

    def getcouttotal(self):
        

class Noeud:
    def __init__(self,location,mCout,lid,parent=None):
        self.location = location
        self.mCout =mCout
        self.parent = parent 
        self.score = 0 
        self.lid = lid 

    def __eq__(self, n):
        if n.lid == self.lid:
            return 1
        else:
            return 0

class AStar:

    def __init__(self,niveau):
        self.mh = niveau
                
    def getMeilleurnoeudlisteouverte(self):
        bestNode = None        
        for n in self.on:
            if not bestNode:
                bestNode = n
            else:
                if n.score<=bestNode.score:
                    bestNode = n
        return bestNode

    def _tracernoeuds(self,n):
        noeuds= [];
        couttotal= n.mcout;
        p = n.parent;
        nodes.insert(0,n);       
        
        while 1:
            if p.parent is None: 
                break
            nodes.insert(0,p)
            p=p.parent
            return Path(nodes,totalCost)

        return None

    def trouvechemin(self,A,B):
        self.o = []
        self.on = []
        self.c = []

        fin = B
        fnode = self.mh.getNode(A)
        self.on.append(fnoeud)
        self.o.append(fnoeud.lid)
        noeudsuivant = fnoeud 
               
        while noeudsuivant is not None: 
            finish = self._handleNode(noeudsuivant,fin)
            if finx:                
                return self._tracechemin(finx)
            noeudsuivant=self.getMeilleurnoeudlisteouverte()
                
        return None


                
  
