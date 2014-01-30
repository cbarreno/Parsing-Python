import sys
import fileinput

def imprimirXml (a):
    l=len(a)
    for i in range(l):
        print (a[i],)
        
	
def main():
    f = open('copiawurfl.xml', 'r+')
##    print (f.read())
    l=f.readlines()
    print(l)


def imprimirXml2 (a):
    if(a==[] or a==""):
        print ("FIN")
    else:
        print (a[0])
        imprimirXml2 (a[1:])
    


def obtenerChar (l, pos, i):
    if(l==[] or l==""):
        return ' '
    if i == pos:
        return l[0]
    else:
        return obtenerChar (l[1:], pos, i+1)

    	



def buscarHasta (l, bus, ini, i):
    if (l==[] or l==""):
        return -1
    if i < ini:
        return buscarHasta (l[1:], bus, ini, i+1)
    if (l[0]==bus): 
        return i
    
    if (l[0]!=bus):
        return buscarHasta (l[1:], bus, ini, i+1)

    



def extraerNombre (l,ini,i,nombre):
    if (l==[] or l==""):
        return nombre
    if (i < ini): 
        return extraerNombre (l[1:],ini,i+1,nombre)
    else:
        if (l[0]==' ' or l[0]=='>'):
            return nombre
        else:
            return extraerNombre (l[1:],ini,i+1,nombre+l[0])
            


def recorrerLineas (l, buscar,i):
    if(l==[] or l==""):
        print (i)
        return
        
    pos = buscarHasta (l[0], '<', 0, 0)
    c = obtenerChar (l[0], pos+1, 0);
    nom = extraerNombre (l[0],pos+1,0,"")


    if (c != '/'):
        if (nom == buscar):
            print (l[0])
            recorrerLineas (l[1:], buscar, i+1)
        else:
            recorrerLineas (l[1:], buscar, i)            
    else:
        recorrerLineas (l[1:], buscar, i)
    
        
    
        

    
        
    
##print (" Fin "  ++ show i)


def prueba(l):
    if(l==[]):
        print("Lista vacia")
    else:
        print("petite salope")

def prueba2(l):
    if(l==[] or l==""):
        print ("FIN")
        
    else:
        print(l[0])
        prueba2(l[1:])


  
    
    

##def main():
##    f = open('copiawurfl.xml', 'r+')
####    print (f.read())
##    l=f.readlines()
##    print(l)
				
