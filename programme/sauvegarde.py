def saveGame(niveau,port,nbNiveau,collection,variables):
    fichier=open('sauvegardes/save'+str(port)+'.txt','w')
    fichier.write('--niv--'+str(nbNiveau)+'\n')
    fichier.write('--col--'+collection+'\n')
    fichier.write('--hsp--'+''.join(variables['historyP'])+'\n')
    for x in range(len(variables['historyC'])):
        fichier.write('--hsc->'+':'.join(variables['historyC'][x])+'\n')
    for x in range(len(niveau.gameO)):
        for y in range (len(niveau.gameO[0])):
            fichier.write(niveau.gameO[x][y].repr)
        fichier.write('\n')
    fichier.close()

def loadGame(port):
    grilleO=[]
    historyC=[]
    fichier = open('sauvegardes/save'+str(port)+'.txt','r')
    for l in fichier:
        if l[:7]=='--niv--':
            nbNiveau=int(l[7:-1])
        elif l[:7]=='--col--':
            collection=l[7:-1]
        elif l[:7]=='--hsp--':
            historyP=l[7:-1]
        elif l[:7]=='--hsc->':
            historyC+=[[l[8:-1].split(':')]]
        else:
            grilleO+=[list(l[:-1])]
            print(list(l[:-1]))
    fichier.close()
    return grilleO,nbNiveau,collection,list(historyP)
