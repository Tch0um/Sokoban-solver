from PIL import Image
import pygame


def ouvrir(nomimage):
    #Creer l'objet image a partir du fichier image, exemple : nomimage='lena.jpg'
    img=Image.open(nomimage).convert('RGBA')
    #Renvoie l'objet image a partir du fichier image
    return img


def redimensionner2(img,sign=True):
    image = img
    if sign:
        imageS = Image.new("RGBA",(int(image.size[0]/2),int(image.size[1]/2)))
    else:
        imageS = Image.new("RGBA",(int(image.size[0]*2),int(image.size[1]*2)))
    pix1 = image.load()
    pix2=imageS.load()
    width,height = imageS.size
    for j in range(height):
        for i in range(width):
            if sign:
                pix2[i,j] = (int((pix1[i*2,j*2][0] + pix1[(i*2)+1,j][0] + pix1[i,(j*2)+1][0] + pix1[(i*2)+1,(j*2)+1][0])/4),int((pix1[i*2,j*2][1] + pix1[(i*2)+1,j][1] + pix1[i,(j*2)+1][1] + pix1[(i*2)+1,(j*2)+1][1])/4),int((pix1[i*2,j*2][2] + pix1[(i*2)+1,j][2] + pix1[i,(j*2)+1][2] + pix1[(i*2)+1,(j*2)+1][2])/4),int((pix1[i*2,j*2][3] + pix1[(i*2)+1,j][3] + pix1[i,(j*2)+1][3] + pix1[(i*2)+1,(j*2)+1][3])/4))
            else:
                pix2[i,j] = pix1[i//2,j//2]
    return imageS

def pyToPil(surface):
    size = surface.get_size()
    data = pygame.image.tostring(surface,'RGBA')
    return Image.frombytes('RGBA',size,data)

def pilToPy(img):
    return pygame.image.fromstring(img.tobytes(),img.size,img.mode)


def scaleUpSurface(surface):
    img = pyToPil(surface)
    return pilToPy(redimensionner2(img,False))

def scaleDownSurface(surface):
    img = pyToPil(surface)
    return pilToPy(redimensionner2(img))


    
if __name__=="__main__":
    imgL = "images/menu_title.png"
    img = ouvrir(imgL)
    img.show()

    img2 = redimensionner2(img,False)
    img2.show()

    pygame.init()
    fen = pygame.display.set_mode((800,600))
    sf = pilToPy(img2)
    fen.blit(sf,(0,0))
    pygame.display.flip()
