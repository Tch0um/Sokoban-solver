def saveGame(port,variables):
    niveau = variables['niveauObj']
    fichier=open('sauvegardes/save'+str(port)+'.txt','w')
    fichier.write('--niv--'+str(variables['nbNiveau'])+'\n')
    fichier.write('--col--'+variables['collection']+'\n')
    fichier.write('--hsp--'+''.join(variables['historyP'])+'\n')
    for x in range(len(variables['historyC'])):
        fichier.write('--hsc->'+':'.join(variables['historyC'][x])+'\n')
    for x in range(len(niveau.gameO)):
        for y in range (len(niveau.gameO[0])):
            fichier.write(niveau.gameO[x][y].repr)
        fichier.write('\n')
    fichier.close()
    print('sauvegarde effectuée')


def loadGame(port,variables):
    grilleO=[]
    historyC=[]
    fichier = open('sauvegardes/save'+str(port)+'.txt','r')
    for l in fichier:
        if l[:7]=='--niv--':
            nbNiveau=int(l[7:-1])
        elif l[:7]=='--col--':
            variables['collection']=l[7:-1]
        elif l[:7]=='--hsp--':
            historyP=l[7:-1]
        elif l[:7]=='--hsc->':
            historyC+=[l[7:-1].split(':')]
        else:
            grilleO+=[list(l[:-1])]
            #print(list(l[:-1]))
    fichier.close()
    
    variables['historyP']=list(historyP)
    variables['historyC']=historyC
    return grilleO,nbNiveau


def rewind(variables):
    direction = variables['historyP'][-1]
    del variables['historyP'][-1]

    if direction=='h':
        direction = (1,0)
    elif direction=='b':
        direction = (-1,0)
    elif direction=='g':
        direction = (0,1)
    elif direction=='d':
        direction = (0,-1)

    #print(niveau.gameO[coordPerso[0]][coordPerso[1]].repr)
    variables['persoObj'].deplace(direction)
    if variables['historyC']!=[] and len(variables['historyP']) == int(variables['historyC'][-1][2]):
        variables['niveauObj'].gameO[int(variables['historyC'][-1][0])][int(variables['historyC'][-1][1])].deplace(direction)
        del variables['historyC'][-1]
