from test.regrtest import count
from getpass import fallback_getpass
from http.client import ImproperConnectionState
import sys
import fileinput
from pickle import APPEND


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


#Imprime archivoXml en forma iterativa
def imprimirXml (a):
    l=len(a)
    for i in range(l):
        print (a[i],)
        
    
#Obtiene un caracter dado una lista y una posicion
def obtenerChar (l, pos):
    if(pos>=len(l)):
        return ' '
    return l[pos]


#Busca hasta un caracter específico y retorna su posición
def buscarHasta (l, bus, ini):
    for i in range(ini,len(l)):
        if (l[i]==bus): 
            return i
    return -1

    
#Extrae el id de un Device
def extraerId(linea):
    ini=buscarHasta (linea, '\"', 0);
    fin = buscarHasta (linea, '\"', ini+1);
    return extraerInfo(linea, ini+1, fin)
        

#Dado una posición inicial y final, extrae el id de un Device
def extraerInfo (l,ini,fin):
    info=""
    for i in range(ini,fin):
        if (i>=len(l)):
            return info
        else:
            info=info+l[i]
    return info


#Dado una lista de Strings(linea-item del xml), extrae el nombre del Tag(Device, Group o Capability)
def extraerNombre (l,ini):
    nombre=""
    for i in range(ini,len(l)):
        if (l[i]==' ' or l[i]=='>'):
            return nombre
        else:
            nombre = nombre+l[i]        
    return nombre

#Dado una lista(linea-item del wurfl) extrae la informacion del Tag grupo(el atributo name). En forma recursiva
def extraerInfoGrupo (l,ini,i,detalle):
    if (l==[] or l==""):
        return detalle
    if i < ini :
        return extraerInfoGrupo (l[1:],ini,i+1,detalle)
    else:
        if l[0]=='>':
            return detalle
        else:
            return extraerInfoGrupo (l[1:],ini,i+1,detalle+l[0])

            
#Dado una lista(linea del wurfl) extrae la informacion del Tag grupo(el name). En forma iterativa
def extraerInfoGrupo2 (l,ini):
    detalle=""
    if (l==[] or l==""):
        return detalle

    for i in range(ini,len(l)):
        if (l[i]=='>'):
            return detalle
        else:
            detalle = detalle + l[i]
            
    return detalle  
            
            


#Dado una lista(linea del wurfl) extrae la informacion del Tag device(el id, user_agent y fallback). En forma recursiva
def extraerInfoDevice (l,ini,i,detalle):
    if (l==[] or l==""):
        return detalle
    if i < ini: 
        return extraerInfoDevice (l[1:],ini,i+1,detalle)
    else:
        if l[0]=='>':
            return detalle
        else:
            return extraerInfoDevice (l[1:],ini,i+1,detalle+l[0])    


#Dado una lista(linea del wurfl) extrae la informacion del Tag device(el id, user_agent y fallback). En forma iterativa
def extraerInfoDevice2 (l,ini):
    detalle=""
    if (l==[] or l==""):
        return detalle
    for i in range(ini,len(l)):
        if (l[i]=='>'):
            return detalle
        else:
            detalle=detalle + l[i]

    return detalle


#Dado una lista(linea del wurfl) extrae la informacion del Tag Capability(el name y value. En forma iterativa
def extraerDetalleCapab (l,ini):
    detalle=""
    for i in range(ini,len(l)):
        if l[0]=='/':
            return detalle
        else:
            detalle= detalle+l[i]
    return detalle


        


#Dado una lista de lineas-Strings(wurfl.xml), un String (Group) y un name especifico
#Retorna 1 si el device pertenece a dicho grupo; caso contrario 0
def buscarGrupo (l, buscar,name):
    if (l==[] or l==""):
        return 0
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0);
        c = obtenerChar (item, pos+1);
        
        if c != '/':
            nom = extraerNombre (item,pos+1);
            if nom == buscar:
                det = extraerInfoGrupo2 (item,pos + 7)
                if det == "id=\""+name+"\"" :
                    return 1
            else:
                if nom == "device" :
                    return 0
                
        
                    

##--Función buscarCapacidad: Dado una lista (wurfl), el tag capability y sus atributos name y value
##--Retorna 1 si lo encontró, caso contrario 0
#--Además también se valida que si el parametro es false, y en el archivo wurfl no lo encuentra, retorna 1
def buscarCapacidad (l, buscar,name,value):
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0);
        c = obtenerChar (item, pos+1);
        if (c != '/'):
            nom = extraerNombre (item,pos+1);
            if (nom == buscar):
                det = extraerDetalleCapab (item,pos + 12)
                ini=buscarHasta (det, '\"', 0);
                fin = buscarHasta (det, '\"', ini+1);
                nCap= extraerInfo(det, ini+1, fin)
                ini=buscarHasta (det, '\"', fin+1);
                fin = buscarHasta (det, '\"', ini+1);
                vCap= extraerInfo(det, ini+1, fin)
                if ((name in nCap) and (value in vCap)):
                    return 1
            else:
                if (nom == "device"):
                    if(value=="false" or value=="none"):
                        return 1
                    return 0  ##condición si encuentra otro device retorna 0
    return 0                    

                    

#Dado una lista de lineas-Strings(wurfl.xml), un String(Capability)
#Retorna cuántos y cuáles son las capacidades de un device espefico.
def presentarCapacidades (l, buscar):
    cont=0
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0);
        c = obtenerChar (item, pos+1);
    
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == buscar):
                print (item)
                cont=cont+1
            else:
                if(nom=="device"):
                    break;
    print (" Capacidades: ", cont)
    return cont




#Dado una lista(wurfl), un String(Group)
#Retorna los grupos de un device
def presentarGrupos (l, buscar):
    cont=0
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0);
        c = obtenerChar (item, pos+1);
    
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == buscar):
                print (item)
                cont=cont+1
            else:
                if(nom=="device"):
                    break;
    print (" Grupos: ", cont)
    return cont

##--Función recorrerCapacidadDevice: Dado una lista de lineas(strings), 1 String(device), 1 contador i y una capacidad específica(name y value)
##--Imprime todos los devices que tienen dicha capacidad y también imprime cuántos encontró            
def recorrerCapacidadDevice(l, buscar,name,value,fall):
    cont=0
    lIds=[]
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0)
        c = obtenerChar (item, pos+1)
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == buscar):
                id = extraerId(item)#Para todos los que hacen fall_back de el dispositivo
                if(existeEnLista(lIds,id)==False):
                    if ((buscarCapacidad (l[i+1:], "capability",name,value))==1):
                        print (i,id)
                        lIds.append(id)
                        if (value=="false" or value=="none"):
                            cantF=0#No busca en sus hijos la caracteristica
                        else:
                            lIds = buscarFallBack(fall, id,0,lIds)
                        print ("LEN: ",len(lIds))
                    
    print ("Cantidad de devices: ",len(lIds))            
                

#Dado el archivo fallback, id de un device, un nivel de profundidad, y una lista de ids de devices
#Retorna una lista de Ids de devices (el padre-idB más sus hijos). Además, esta función se hace recursiva ya que llama al metodo presentar Fallacks quien llama a esta función
def buscarFallBack(fall, idB,nivel,lIds):
    for (i, item) in enumerate(fall):
        pos = buscarHasta (item, '<', 0)
        c = obtenerChar (item, pos+1)
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == "fallback"):
                id = extraerId(item)
                if (id==idB):
                    lIds = presentarFallBacks (fall[i+1:],fall,nivel+1,lIds)
                    break
    
    return lIds
                

#Verifica si el ID enviado está en la lista
def existeEnLista(lista, id):
    for (i, item) in enumerate(lista):
        if(id==item):
            return True
        
    return False


#Dado el archivo fallback 2 veces como parametro(fall y fallComp), un nivel de profundidad y una lista de Ids
#Retorna una lista de Ids (el id Padre más sus hijos)
def presentarFallBacks (fall,fallComp,nivel,lIds):
    for (i, item) in enumerate(fall):
        pos = buscarHasta (item, '<', 0);
        c = obtenerChar (item, pos+1);
    
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == "device"):
                id = extraerId(item)#Para todos los que hacen fall_back de el dispositivo
                lIds.append(id)
                esp=""
                for i in range(0,nivel):
                    esp=esp+"\t"
                print (esp,nivel," - ",id)
                lIds = buscarFallBack(fallComp, id,nivel,lIds)
            else:
                if(nom=="fallback"):
                    break;
    return lIds


    
#Funcion recorrerLineas: Dado una lista(wurfl), y un tag especifico(Device, Group, Capability)
#Imprime todos los devices, groups, o capabilities que encuentre
def recorrerLineas (l, buscar):
    cont=0
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0)
        c = obtenerChar (item, pos+1)
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == buscar):
                print (i,item)
                cont=cont+1
    
    print ("Cantidad de devices: ",cont)


#Función que recibe una lista(archivo wurfl), un String (Tag Device)
#Crea un nuevo archivo con todos los devices, cada device con sus respectivos devices que le hacen referencia(fallbacks)        
def generarFallBacks(l, buscar):
    f = open('fallbacks.xml', 'w')
    cont=0
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0)
        c = obtenerChar (item, pos+1)
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == buscar):
                print (cont)
                #if (cont==10):
                #    break
                id = extraerId(item)#Para todos los que hacen fall_back de el dispositivo
                f.write('<fallback id=\"'+id+"\">\n")
                buscarFallBack2(l, id,f)
                cont=cont+1
    f.close()


#Dado una lista(wurfl), un id de un device específico, y el archivo fallback.xml
#Retorna el id especifico(Padre)con todos los devices que hacen referencia a este (fallback) en el archivo fallback.xml
def buscarFallBack2(l, id,f):
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0)
        c = obtenerChar (item, pos+1)
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == "device"):
                if ("fall_back=\""+id+"\"" in item):
                    f.write(item)
    
          



##--Función recorrerDevices: Dado una lista(archivo wurfl), 1 String(tag device), y el id de un device en especifico
##--Imprime todas las capacidades de ese device y cuántas encontró            
def recorrerDevices (l, buscar,id):
    cont=0;
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0)
        c = obtenerChar (item, pos+1)
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == buscar):
                idB = extraerId(item)
                if (id == idB):
                    presentarCapacidades(l[i+1:],"capability")
                    break
                        
                        

#Dado lista(archivo wurfl), un tag(Group), un name de grupo específico, y el archivo fallback.xml
#Retorna todos los devices que pertenecen a dicho grupo incluyendo los fallbacks
def recorrerGroupDevice (l, buscar,name,fall):
    lIds=[]
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0);
        c = obtenerChar(item, pos+1);
        nom = extraerNombre (item,pos+1)
    
        if (c != '/'):
            if (nom == buscar):
                id = extraerId(item)#Para todos los que hacen fall_back de el dispositivo
                if(existeEnLista(lIds,id)==False):
                    if ((buscarGrupo(l[i+1:], "group",name))==1):
                        print (i,id)
                        lIds.append(id)
                        lIds = buscarFallBack(fall, id,0,lIds)
                        print ("LEN: ",len(lIds))
                
    print ("Cantidad de devices: ",len(lIds))         
                    
    
        

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
    if(parseo()[0]==1):
        print("El archivo xml esta bien escrito")
    else :
        print("Esta mal formado el archivo xml")
    
def main(1):
    f = open('wurfl-2.3.xml', 'r+')
    l=f.readlines()
    f2 = open('fallbacks.xml', 'r+')
    fall=f2.readlines()
#    recorrerGroupDevice (l, "device","ajax",fall)
#    recorrerDevices(l, "device","generic_mobile")
    recorrerCapacidadDevice(l, "device","built_in_camera","false",fall)


#Generar archivo de FallBacks    
def main2():
    f = open('wurfl-2.3.xml', 'r+')
    l=f.readlines()
    generarFallBacks (l, "device")



main()
