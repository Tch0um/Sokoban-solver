from PIL import Image


def ouvrir(nomimage):
    #Creer l'objet image a partir du fichier image, exemple : nomimage='lena.jpg'
    img=Image.open(nomimage)
    print(img.mode)
    #Renvoie l'objet image a partir du fichier image
    return img


def redimensionner2(img,sign=True):
    image = ouvrir(img)
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
    imageS.show()
    return imageS
