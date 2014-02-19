from test.regrtest import count
from getpass import fallback_getpass
from http.client import ImproperConnectionState
class Arbol:
    def __init__(self,contenido,hijos): #constructor
        self.contenido=contenido
        self.hijos=hijos
    
    def getContenido(self):
        return self.contenido
    def getHijos(self):
        return self.hijos
    def setContenido(self,newContenido):
        self.contenido=newContenido
    def setHijos(self,newHijos):
        self.hijos=newHijos
    def agragarHijos(self,nuevoh):
        self.hijos.append(nuevoh)
    def mostrarArbol(self):
        
        return self.contenido

class Devices:
    def __init__(self,ldevice): #constructor
        self.ldevice=ldevice
    def getLdevice(self):
        return self.ldevice
    def setLdevice(self,newLdevice):
        self.ldevice=newLdevice
        
class Device:
    def __init__(self,iddev,useragent,fallback,lgroups): #constructor
        self.iddev=iddev
        self.useragent=useragent
        self.fallback=fallback
        self.lgroups=lgroups
    #def __init__(self):
       # self.iddev=None
        #self.useragent=None
       # self.fallback=None
       # self.lgroups=None
        
    def getIddev(self):
        return self.iddev 
    def getUseragent(self):
        return self.useragent
    def getFallback(self):
        return self.fallback
    def getLgroups(self):
        return self.lgroups
    def setIddev(self,newIddev):
        self.iddev=newIddev
    def setUserAgent(self,newUseragent):
        self.useragent=newUseragent
    def setFallback(self,newFallback):
        self.fallback=newFallback
    def setLgroups(self,newLgroups):
        self.lgroups=newLgroups
    
            
class Groups:
    def __init__(self,idgroups): #constructor
        self.idgroups=idgroups
    def getIdgroups(self):
        return self.idgroups
    def setIdgroups(self,newIdgroups):
        self.idgroups=newIdgroups
                    
class Capabilities:
    def __init__(self,idcap,name,value): #constructor
        self.idcap=idcap
        self.name=name
        self.value=value
    def getIdcap(self):
        return self.idcap
    def getName(self):
        return self.name
    def getValue(self):
        return self.value
    def setIdcap(self,newIdcap):
        self.idcap=newIdcap
    def setName(self,newName):
        self.name=newName
    def setValue(self,newValue):
        self.value=newValue


#Dada una lista devuelve su tamaño
def tamanio(caden):
    totalc = 0
    for dia in caden:
        totalc=totalc +1
    return totalc

# comprueba si la vaersion del xml esta bien estructurada
def compruebaVersion(cadena):
    c= tamanio (cadena)
    u="".join(cadena[c-1]).replace('"', " ").split()
    if cadena[0]=="<?xml" and u[c-1]=="?>" :
        return 1
    
    else:
        u="".join(cadena[c-1]).replace('"', " ").split()
        print(u)
        return 8

# Dada una lista y su tamaño devuelve que tipo de tag esta contenido en la lista
def compruebatipoetiqueta(cadena,taman):   
    if cadena==[]:
        return  15
    elif cadena[0]=="<devices>":
        return  1
    elif cadena[0]=="<device" and cadena[taman]==">" :
        return 2
    elif cadena[0]=="<device" and cadena[taman].count("/>")==1 :
        return 3
    elif cadena[0]=="<group" and cadena[taman].count(">")==1 :
        return 4
    elif cadena[0]=="<capability" and cadena[taman].count("/>")==1 :
        return 5
    elif cadena[0]=="</devices>" :
        return 8
    elif cadena[0]=="</device>" :
        return 7
    elif cadena[0]=="</group>" :
        return 6
    elif cadena[0]=="</wurfl>" :
        return 9
    elif cadena[0]=="<wurfl>":
        return  10
    else :
        return 0
    
# Dado el archivo xml , le quita la parte de la version del xml
def quitaversion(cadena):
    i=0
    cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
    
    while cadena1 !=["</version>"] :
        i+=1
        cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
        
    return cadena[(i+1):]


# Esta funcion realiza el parseo del xml comprobando que esten bien estructurados los tags y que todos concuerden
def parseo():
    archivo=leerArchivo()
    resulta=compruebaVersion(archivo[0].split())
    if resulta==1:
        cadena=[archivo[1]]
     
        caden=quitaversion(archivo[2:])
     
        cadena.extend(caden)
        return  parseointernos(cadena,[])
    else:
        return  [0,Arbol(None,[])]
        

# Comprueba que el xml este correcto
def parseointerno(cadena,lista):
    i=0
    valor=1
    tama=tamanio(cadena)
    
    while (valor==1 and tama!=i):
        arbol=Arbol(None,[])
        cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
        #print(cadena1)
        taman2=tamanio(cadena1)
        tipoE=compruebatipoetiqueta(cadena1, taman2-1)
        i+=1
        #print (cadena1)
        if (tipoE==1):
            lista.append("</devices>")
        elif (tipoE==2):
            lista.append("</device>")
        elif (tipoE==3):
            pass
        elif (tipoE==4):
            lista.append("</group>")
        elif (tipoE==5):
            pass
        elif (tipoE==6):
            eti=lista.pop()
            if eti==cadena1[0] :
                valor=1
            else :
                valor=0
        elif (tipoE==7):
            eti=lista.pop()
            if eti==cadena1[0] :
                valor=1
            else :
                valor=0
        elif (tipoE==8):
            eti=lista.pop()
            if eti==cadena1[0] :
                valor=1
            else :
                valor=0
        elif (tipoE==9):
            eti=lista.pop()
            if eti==cadena1[0] :
                valor=1
            else :
                valor=0
        elif (tipoE==10):
            lista.append("</wurfl>")
        else :
            valor=0
        
        
    if valor==1 :
        return 1
    else :
        return 0   
    
    

# Esta funcion aparte de comprobar si el archivo esta bien , 
#crea una estructura como un arbo para almacenar ahy la informacion momentaneamente
def parseointernos(cadena,lista):
     i=0
     valor=1
     salir=0
     contador=0
     tama=tamanio(cadena)
     while (valor==1 and tama!=i and salir==0):
         
         cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
         arbol=Arbol(cadena1,[])
         lista.append("</wurfl>")
         i+=1
         cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
         taman2=tamanio(cadena1)
         tipoE=compruebatipoetiqueta(cadena1, taman2-1)
         arboldevices=Arbol(None,[])
         while (valor==1 and tama!=i and salir==0):
            if (tipoE==1):
                lista.append("</devices>")
                i+=1
                arbolDs=Arbol(cadena1,[])
                
                cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
                taman2=tamanio(cadena1)
                tipoE=compruebatipoetiqueta(cadena1, taman2-1)
                arboldds=Arbol(None,[])
                while (valor==1 and  tama!=i and salir==0):
                   
                    if (tipoE==2 or tipoE==3):
                        if tipoE==3 :
                            contador+=1
                            i+=1
                            arbolD=Arbol(cadena1,[])
                            arboldds.agragarHijos(arbolD) 
                            cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
                            taman2=tamanio(cadena1)
                            tipoE=compruebatipoetiqueta(cadena1, taman2-1)
                            arbolggs=Arbol(None,[])
                        else :
                            contador+=1
                            lista.append("</device>")
                            i+=1
                            arbolD=Arbol(cadena1,[])
                    
                            cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
                            taman2=tamanio(cadena1)
                            tipoE=compruebatipoetiqueta(cadena1, taman2-1)
                            arbolggs=Arbol(None,[])
                            while(valor==1 and tama!=i and salir==0):
                               
                                
                                if (tipoE==4):
                                    lista.append("</group>")
                                    i+=1
                                    arbolg=Arbol(cadena1,[])
                                    arbolggs.agragarHijos(arbolg)
                                    cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
                                    taman2=tamanio(cadena1)
                                    tipoE=compruebatipoetiqueta(cadena1, taman2-1)
                                    arbolcs=Arbol(None,[])
                                    while (valor==1 and tama!=i and salir==0):
                                        if (tipoE==5):
                                            i+=1
                                            arbolc=Arbol(cadena1,[])
                                            arbolcs.agragarHijos(arbolc)
                                            cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
                                            taman2=tamanio(cadena1)
                                            tipoE=compruebatipoetiqueta(cadena1, taman2-1)
                                
                                        elif tipoE==6 :
                                           
                                            eti=lista.pop()
                                           
                                            if eti==cadena1[0] :
                                                valor=1
                                                salir=1
                                               
                                                
                                            else :
                                                valor=0
                                                arbolcs=Arbol(None,[])  
                                        else :
                                            valor=0
                                            arbolcs=Arbol(None,[])
                                    
                                    arbolg.setHijos(arbolcs.getHijos())
                                    arbolggs.agragarHijos(arbolg)
                                    i+=1
                                    salir=0
                                    cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
                                    taman2=tamanio(cadena1)
                                    tipoE=compruebatipoetiqueta(cadena1, taman2-1)
                                    
                               
                                elif (tipoE==7):
                                    
                                    eti=lista.pop()
                                    if eti==cadena1[0] :
                                        valor=1
                                        salir=1
                                        
                                    else :            
                                        valor=0
                                        arbolggs=Arbol(None,[])            
                                else :
                                    valor=0
                                    arbolggs=Arbol(None,[])
                               
                            arbolD.setHijos(arbolggs.getHijos())  
                            arboldds.agragarHijos(arbolD)  
                            i+=1
                            salir=0
                            cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
                            taman2=tamanio(cadena1)
                            tipoE=compruebatipoetiqueta(cadena1, taman2-1)
                                    

                    elif tipoE==8 :
                                eti=lista.pop()
                                if eti==cadena1[0] :
                                    valor=1
                                    salir=1
                        
                                else :
                                    valor=0
                                    arbolcs=Arbol(None,[])
                    else :
                                    valor=0
                                    arbolggs=Arbol(None,[])
                arbolDs.setHijos(arboldds.getHijos())
                arboldevices.agragarHijos(arbolDs)  
                i+=1
                salir=0
                cadena1=cadena[i].strip().replace("\n","").replace('"', " ").split()
                taman2=tamanio(cadena1)
                tipoE=compruebatipoetiqueta(cadena1, taman2-1)
                                    
                
            elif tipoE==9 :
                                eti=lista.pop()
                                if eti==cadena1[0] :
                                    valor=1
                                    salir=1
                                               
                                else :
                                    valor=0
                                    arbolcs=Arbol(None,[])
                                     
            else :
                    valor=0
                    arbolggs=Arbol(None,[])                               
         arbol.setHijos(arboldevices.getHijos())   
                                 
     if(valor==1):
        print(contador)
        return (valor,arbol)
     else:
        return (0,Arbol(None,[]))
         
         
# Abre el archivo xml y lo convierte en una lista
def leerArchivo():
    archivo = open('wurfl-2.3.xml', 'r+')
    #l=archivo.read()
    archivolineas=archivo.readlines()
    #ar="".join([archivolineas[0]])
    #cadena="<?xmml version 77 hola que tal como estas ?>"
    #cap=cadena.split()
    archivo.close()
    return archivolineas
    
# Obtieen el fallbacks dada una cadena de device 
def obtenerfallback(cadena): 
    salir=0
    i=0
    fallback=""
    while salir==0 :
        if cadena[i]=="fall_back=" :
            if cadena[i+1] !="" :
                fallback=cadena[i+1]
                salir=1
            else :
                fallback=""
                salir=1
                
        else :   
             i+=1
    return fallback  

    
# Obtieen el id dada una cadena de device 
def obteneridDevice(cadena): 
    salir=0
    i=0
    fallback=""
    while salir==0 :
        if cadena[i]=="id=" :
            if cadena[i+1] !="" :
                fallback=cadena[i+1]
                salir=1
            else :
                fallback=""
                salir=1
                
        else :   
            i+=1
    return fallback 
    
    
#dada una lista de devices retorna otra lista de device pero solo con sus id y su Fallbacks
def listaDevice(listaw,tamanio):
    i=0
    salir=0
    lista=[]
    while i<tamanio :
        tupla=(obteneridDevice(listaw[i].getContenido()),obtenerfallback(listaw[i].getContenido()))
        lista.append(tupla)
        i+=1
        
    return lista   

#Dada dos listas y usus tamaños , esta funcion verifica la herencia de atributos entre los devices 
#y devuelve una lista con todas las herencias posibles que pueda tener la lista1 en el archivo xml
def imprimirHerencia(lista1,tama1,lista2,tama2):
    
    i=0
    lista=[]
    listaprueba=lista1
    y=0
    t=1
    while t!=0:
        lista=[]
        while i< tama1 :
            while y < tama2 :
               
                if(listaprueba[i]==lista2[y][1]):
                    
                    lista.append(lista2[y][0])
                y+=1
            
            y=0   
            i+=1
         
        t=tamanio(lista)
    
        t1=tamanio(lista1)
      
        lista1=juntarlistas(lista1,t1,lista,t)
        
        i=0
        y=0
     
        if (t>0):
            listaprueba=lista1[t1:]
            tama1=tamanio(listaprueba )
        else : 
            pass
    return lista1    

#Dada dos lista las junta pero sin terminos repetidos
def juntarlistas(lista1,tam1,lista,tam): 
    x=0
    y=0
    lista11=lista1
    while y<tam :
     
        if(lista11.count(lista[y])==0) :   
           
            lista1.extend([lista[y]])
            
        y+=1
    return lista1

# funcion pricipal
def main():
    #ar=parseo()[1].getHijos()
    #arr=ar[0].getHijos()
    #t=tamanio(arr)
   # lis=a=ar[0].getHijos()
    #l=listaDevice(lis, t)
    #=tamanio(l)
    #u=imprimirHerencia(["nokia_generic_series30"],1, l, t)
    #ta=tamanio(u)
    #print(u)
    #print(ta)
    print(parseo()[0])
    

main()