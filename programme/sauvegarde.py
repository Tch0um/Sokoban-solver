def saveGame(niveau,port,nbNiveau,collection):
    fichier=open('sauvegardes/save'+str(port)+'.txt','w')
    fichier.write('--niv--'+str(nbNiveau)+'\n')
    fichier.write('--col--'+collection+'\n')
    for x in range(len(niveau.gameO)):
        for y in range (len(niveau.gameO[0])):
            fichier.write(niveau.gameO[x][y].repr)
        fichier.write('\n')
    fichier.close()

def loadGame(port):
    grilleO=[]
    fichier = open('sauvegardes/save'+str(port)+'.txt','r')
    for l in fichier:
        if l[:7]=='--niv--':
            nbNiveau=int(l[7:-1])
        elif l[:7]=='--col--':
            collection=l[7:-1]
        else:
            grilleO+=[list(l[:-1])]
            print(list(l[:-1]))
    fichier.close()
    return grilleO,nbNiveau,collection
