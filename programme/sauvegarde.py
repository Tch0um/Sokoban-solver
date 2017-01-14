def saveGame(niveau,port,nbNiveau):
    fichier=open('sauvegardes/save'+str(port)+'.txt','w')
    fichier.write(str(nbNiveau)+'\n')
    for x in range(len(niveau.gameO)):
        for y in range (len(niveau.gameO[0])):
            fichier.write(niveau.gameO[x][y].repr)
        fichier.write('\n')
    fichier.close()

def loadGame(port):
    grilleO=[]
    fichier = open('sauvegardes/save'+str(port)+'.txt','r')
    for l in fichier:
        if len(l)==2:
            nbNiveau=int(l[0])
        else:
            grilleO+=[l.split()]
    fichier.close()
    return grilleO,nbNiveau
