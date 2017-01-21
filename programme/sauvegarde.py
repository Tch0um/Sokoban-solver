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
            historyC+=[l[7:-1].split(':')]
        else:
            grilleO+=[list(l[:-1])]
            print(list(l[:-1]))
    fichier.close()
    return grilleO,nbNiveau,collection,list(historyP),historyC


def rewind(fenetre,variables,niveau,coordPerso):
    direction = variables['historyP'][-1]
    del variables['historyP'][-1]

    if direction=='h':
        direction = 1
    elif direction=='b':
        direction = -1
    elif direction=='g':
        direction = 2
    elif direction=='d':
        direction = -2

    niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(direction,niveau,fenetre)
    niveau.afficheNiveau(fenetre)
    if variables['historyC']!=[] and len(variables['historyP']) == int(variables['historyC'][-1][2]):
        print('if2')
        niveau.gameO[int(variables['historyC'][-1][0])][int(variables['historyC'][-1][1])].deplace(direction,niveau,fenetre)
        del variables['historyC'][-1]
