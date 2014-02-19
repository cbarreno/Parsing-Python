import sys
import fileinput
from pickle import APPEND



#Imprime archivoXml
def imprimirXml (a):
    l=len(a)
    for i in range(l):
        print (a[i],)
        
#Imprime archivoXml
def imprimirXml2 (a):
    if(a==[] or a==""):
        print ("FIN")
    else:
        print (a[0])
        imprimirXml2 (a[1:])
    
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


#Dado una lista de Strings(cada linea del xml)
def extraerNombre (l,ini):
    nombre=""
    for i in range(ini,len(l)):
        if (l[i]==' ' or l[i]=='>'):
            return nombre
        else:
            nombre = nombre+l[i]        
    return nombre

#Dado una lista(linea del wurfl) extrae la informacion del Tag grupo(el name). En forma recursiva
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
                
        
                    

##--Función buscarCapacidad: Dado una lista de lineas, el tag capability y sus atributos name y value
##--Retorna 1 si lo encontró, caso contrario 0
##--Observación: La función recorrerCapacidadDevice encuentra un Tag Device en una línea específica, luego le envia a buscarCapacidad la cola(las demas líneas del xml a partir de ese tag device)
##--Y si encuentra otro tag device retorna 0; quiere decir que buscarCapacidad solo va buscar solo las capacidades de ese tag device
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

                    

#Dado una lista de lines(Wurfl), un String(Capability)
#Retorna cuántos y cuáles son las capacidades de un device espefico
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




#Dado una lista, un String(Group)
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
                

#Dado el archivo fallback, id de un device, un nivel de profundidad, y una lista de devices
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
#Crea un nuevo archivo con todos los devices, cada device con sus respectivos que le hacen referencia(fallbacks)        
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
#Retorna el id espcifico con todos los devices que hacen referencia a este (fallback)
def buscarFallBack2(l, id,f):
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0)
        c = obtenerChar (item, pos+1)
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == "device"):
                if ("fall_back=\""+id+"\"" in item):
                    f.write(item)
    
          



##--Función recorrerDevices: Dado una lista de lineas(strings), 1 String(tag device), y el id de un device en especifico
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
                        
                        

#Dado una lista(lineas), un tag(Grupo), un name de grupo específico, y el archivo fallbacl.xml
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
                    
    
        
def main():
    f = open('copiawurfl.xml', 'r+')
    l=f.readlines()
    f2 = open('fallbacks.xml', 'r+')
    fall=f2.readlines()
#    recorrerGroupDevice (l, "device","ajax",fall)
#    recorrerDevices(l, "device","generic_mobile")
#    recorrerCapacidadDevice(l, "device","built_in_camera","false",fall)


#Generar archivo de FallBacks    
def main2():
    f = open('copiawurfl.xml', 'r+')
    l=f.readlines()
    generarFallBacks (l, "device")

##    print(l)

if __name__ == "__main__":
    main()
