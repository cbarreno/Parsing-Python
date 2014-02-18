import sys
import fileinput

sys.setrecursionlimit(2146900000)

def imprimirXml (a):
    l=len(a)
    for i in range(l):
        print (a[i],)
        

def imprimirXml2 (a):
    if(a==[] or a==""):
        print ("FIN")
    else:
        print (a[0])
        imprimirXml2 (a[1:])
    

def obtenerChar (l, pos):
    if(pos>=len(l)):
        return ' '
    return l[pos]



def buscarHasta (l, bus, ini):
    for i in range(ini,len(l)):
        if (l[i]==bus): 
            return i
    return -1

    

def obtenerCapability (l, nom1, nom2, i):
    if (l==[] or l==""):
        print ("FIN")
        return
    
    if(nom1 in l[0]):
        if(nom2 in l[0]):
            print (l[0])
            obtenerCapability(l[1:], nom1, nom2, i+1)
    else:
        obtenerCapability(l[1:], nom1, nom2, i)
        


def extraerId(linea):
    ini=buscarHasta (linea, '\"', 0);
    fin = buscarHasta (linea, '\"', ini+1);
    return extraerInfo(linea, ini+1, fin)
        


def extraerInfo (l,ini,fin):
    info=""
    for i in range(ini,fin):
        if (i>=len(l)):
            return info
        else:
            info=info+l[i]
    return info



def extraerNombre (l,ini):
    nombre=""
    for i in range(ini,len(l)):
        if (l[i]==' ' or l[i]=='>'):
            return nombre
        else:
            nombre = nombre+l[i]        
    return nombre


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



def extraerDetalleCapab (l,ini):
    detalle=""
    for i in range(ini,len(l)):
        if l[0]=='/':
            return detalle
        else:
            detalle= detalle+l[i]
    return detalle

def buscarDevice (l, buscar,id):
    if (l==[] or l==""):
        return 0
    
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0);
        c = obtenerChar (item, pos+1);
        if c != '/':
            nom = extraerNombre (item,pos+1);
            if (nom == buscar):
                id = extraerId(item)
                det = extraerInfoDevice (item,pos + 8,0,"");
                if ("id=\""+id+"\"" in det):
                    return 1
                 
#             else:
#                 if (nom == "device"):
#                     return 0
#                 
        


##buscarGrupo :: ([String] , String , String) -> Integer
##buscarGrupo ([], buscar,name) = 0
def buscarGrupo (l, buscar,name):
    if (l==[] or l==""):
        return 0
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0);
        c = obtenerChar (item, pos+1);
        
        if c != '/':
            nom = extraerNombre (item,pos+1);
            if nom == buscar:
                det = extraerInfoGrupo (item,pos + 7,0,"")
                if det == "id=\""+name+"\"" :
                    return 1
            else:
                if nom == "device" :
                    return 0
                
        
                    


##--Función buscarCapacidad: Dado    una lista de lineas, el tag capability y sus atributos name y value
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
                    if(value=="false"):
                        return 1
                    return 0  ##condición si encuentra otro device retorna 0
    return 0                    

                    
##--Función buscarCapacidad2: Dado una lista de lineas, el tag capability y sus atributos name y value, imprime todos las capacidades de un device en específico        
##buscarCapacidad2 :: ([String] , String , Integer) -> IO()            
##buscarCapacidad2 ([], buscar ,i) = print (" Fin "  ++ show i)
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
    print (" Fin total %d", cont)
    

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
                        if(value=="false"):
                            cantF=0#No busca en sus hijos la caracteristica
                        else:
                            lIds = buscarFallBack(fall, id,0,lIds)
                        print ("LEN: ",len(lIds))
                    
    print ("Cantidad de devices: ",len(lIds))            
                
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
                
def existeEnLista(lista, id):
    for (i, item) in enumerate(lista):
        if(id==item):
            return True
        
    return False

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

def buscarFallBack2(l, id,f):
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0)
        c = obtenerChar (item, pos+1)
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == "device"):
                if ("fall_back=\""+id+"\"" in item):
                    f.write(item)
    
          



##--Función recorrerDevices2: Dado una lista de lineas(strings), 1 String(device), 1 contador i y los atributos específicos de 1 device(id,user_agent,fall_back)
##--Si lo encuentra imprime todas las capacidades de ese device y cuántas encontró            
##recorrerDevices2 :: ([String] , String , Integer,String,String,String) -> IO()
##recorrerDevices2 ([], buscar ,i,id,user_agent,fall_back) = print (i)
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
                        
                        
def recorrerFallbackSubStr(l, buscar, id):
    cont=0
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0)
        c = obtenerChar (item, pos+1)
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == buscar):
                if ("fall_back=\""+id in item):
                    print (i, item)
                    cont=cont+1
    
    print ("Cantidad de Fall Back Substring: ",cont)


def recorrerDeviceSubStr (l, buscar,id):
    cont=0
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0)
        c = obtenerChar (item, pos+1)
        if (c != '/'):
            nom = extraerNombre (item,pos+1)
            if (nom == buscar):
                if ("id=\""+id in item):
                    print (i, item)
                    cont=cont+1
    
    print ("Cantidad de Devices Substring: ",cont)


def recorrerGroupDevice (l, buscar,i,name,fall):
    cont=0
    lIds=[]
    if(l==[] or l==""):
        print (i)
        return
    for (i, item) in enumerate(l):
        pos = buscarHasta (item, '<', 0);
        c = obtenerChar(item, pos+1);
        nom = extraerNombre (item,pos+1)
    
        if (c != '/'):
            if (nom == buscar):
                if ((buscarGrupo(l[i+1:], "group",name))==1):
                    print (i,id)
                    lIds.append(id)
                    if(value=="false"):
                        cantF=0#No busca en sus hijos la caracteristica
                    else:
                        lIds = buscarFallBack(fall, id,0,lIds)
                    print ("LEN: ",len(lIds))
                
    print ("Cantidad de devices: ",len(lIds))         
                    
    
        
def main():
    f = open('copiawurfl.xml', 'r+')
    l=f.readlines()
    f2 = open('fallbacks.xml', 'r+')
    fall=f2.readlines()
#    recorrerGroupDevice (l, "device", 0,"ajax",fall)
#    recorrerDevices(l, "device","generic_mobile")
#    recorrerLineas (l, "device")
    recorrerCapacidadDevice(l, "device","built_in_camera","true",fall)
#    recorrerCapacidadDevice(l, "device","mobile_browser","Nokia",fall)
#    recorrerCapacidadDevice(l, "device","playback_mp4","true",fall)

#Generar archivo de FallBacks    
def main2():
    f = open('copiawurfl.xml', 'r+')
    l=f.readlines()
    generarFallBacks (l, "device")

##    print(l)

if __name__ == "__main__":
    main()
        


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
