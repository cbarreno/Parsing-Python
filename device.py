import sys
import fileinput

sys.setrecursionlimit(2146000000)

PyObject *res;
buf = PyMem_New(char, BUFSIZ); 

if (buf == None):
    return PyErr_NoMemory();

res = PyString_FromString(buf);
PyMem_Del(buf); 
return res;

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

    
def buscarHastaStr (l, ini, i, nombre):
    if (l==[] or l==""):
        return -1
    if (i < ini): 
        return buscarHastaStr (l[1:],ini,i+1,nombre)
    else:
        if (l[0]==' ' or l[0]=='>'):
            return i
        else:
            return buscarHastaStr (l[1:],ini,i+1,nombre+l[0])
    

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



def extraerInfoGrupo (l,ini,i,detalle):
    if (l==[] or l==""):
        return nombre
    if i < ini :
        return extraerInfoGrupo (l[1:],ini,i+1,detalle)
    else:
        if l[0]=='>':
            return detalle
        else:
            return extraerInfoGrupo (l[1:],ini,i+1,detalle+l[0])

            

def extraerInfoDevice (l,ini,i,detalle):
    if (l==[] or l==""):
        return nombre
    if i < ini: 
        return extraerInfoDevice (l[1:],ini,i+1,detalle)
    else:
        if l[0]=='>':
            return detalle
        else:
            return extraerInfoDevice (l[1:],ini,i+1,detalle+l[0])    




def extraerDetalleCapab (l,ini,i,detalle):
    if (l==[] or l==""):
        return detalle
    if i < ini:
        return extraerDetalleCapab (l[1:],ini,i+1,detalle)
    else:
        if l[0]=='/':
            return detalle
        else:
            return extraerDetalleCapab (l[1:],ini,i+1,detalle+l[0])



def buscarDevice (l, buscar,id,user_agent, fall_back):
    if (l==[] or l==""):
        return nombre
    
    pos = buscarHasta (l[0], '<', 0, 0);
    c = obtenerChar (l[0], pos+1, 0);
    nom = extraerNombre (l[0],pos+1,0,[]);
    det = extraerInfoDevice (l[0],pos + 8,0,[])
    if c != '/':
        if (nom == buscar):
            if (det == "id=\""+id+"\" user_agent=\""+user_agent++"\" fall_back=\""+fall_back+"\""):
                return 1
            else:
                return buscarDevice (l[1:], buscar,id,user_agent,fall_back) ##busca demas lineas
        else:
            if (nom == "device"):
                return 0
            else:
                buscarDevice (l[1:], buscar,id,user_agent,fall_back)
    else:
        buscarDevice(l[1:], buscar,id,user_agent,fall_back)
        


##buscarGrupo :: ([String] , String , String) -> Integer
##buscarGrupo ([], buscar,name) = 0
def buscarGrupo (l, buscar,name):
    if (l==[] or l==""):
        return 0
    
    pos = buscarHasta (l[0], '<', 0, 0);
    c = obtenerChar (l[0], pos+1, 0);
    nom = extraerNombre (l[0],pos+1,0,"");
    det = extraerInfoGrupo (l[0],pos + 7,0,"")

    if c != '/':
        if nom == buscar:
            if det == "id=\""++name++"\"" :
                return 1
            else:
                buscarGrupo (l[1:], buscar,name) ##--busca demás lineas
        else:
            if nom == "device" :
                return 0
            else:
                buscarGrupo (l[1:], buscar,name)
    else:
        buscarGrupo (l[1:], buscar,name)
                    


##--Función buscarCapacidad: Dado    una lista de lineas, el tag capability y sus atributos name y value
##--Retorna 1 si lo encontró, caso contrario 0
##--Observación: La función recorrerCapacidadDevice encuentra un Tag Device en una línea específica, luego le envia a buscarCapacidad la cola(las demas líneas del xml a partir de ese tag device)
##--Y si encuentra otro tag device retorna 0; quiere decir que buscarCapacidad solo va buscar solo las capacidades de ese tag device
def buscarCapacidad (l, buscar,name,value):
    if (l==[] or l==""):
        return 0
    
    pos = buscarHasta (l[0], '<', 0, 0);
    c = obtenerChar (l[0], pos+1, 0);
    nom = extraerNombre (l[0],pos+1,0,"");
    det = extraerDetalleCapab (l[0],pos + 12,0,"")
    if (c != '/'):
        if (nom == buscar):
            if (det == "name=\""+name+"\" value=\""+value+"\""):
                return 1
            else:
                return buscarCapacidad (l[1:], buscar,name,value) ##--busca demas lineas
        else:
            if (nom == "device"):
                return 0  ##condición si encuentra otro device retorna 0
            else:
                return buscarCapacidad (l[1:], buscar,name,value)
    else:
        return buscarCapacidad (l[1:], buscar,name,value)
                    

                    
##--Función buscarCapacidad2: Dado una lista de lineas, el tag capability y sus atributos name y value, imprime todos las capacidades de un device en específico        
##buscarCapacidad2 :: ([String] , String , Integer) -> IO()            
##buscarCapacidad2 ([], buscar ,i) = print (" Fin "  ++ show i)
def buscarCapacidad2 (l, buscar,i):
    if (l==[] or l==""):
        print (" Fin total %d", i)
    
    pos = buscarHasta (l[0], '<', 0, 0);
    c = obtenerChar (l[0], pos+1, 0);
    nom = extraerNombre (l[0],pos+1,0,"")

    if (c != '/'):
        if (nom == buscar):
            print (l[0])
            buscarCapacidad2 (l[1:], buscar, i+1)
        else:
            if(nom=="device"):
                print ("")
            else:
                buscarCapacidad2 (l[1:], buscar, i)    
    else:
        buscarCapacidad2 (l[1:], buscar, i)        


##--Función recorrerCapacidadDevice: Dado una lista de lineas(strings), 1 String(device), 1 contador i y una capacidad específica(name y value)
##--Imprime todos los devices que tienen dicha capacidad y también imprime cuántos encontró            
def recorrerCapacidadDevice(l, buscar,i,name,value):
    if(l==[] or l==""):
        print (i)
        return
    
    pos = buscarHasta (l[0], '<', 0, 0);
    c = obtenerChar (l[0], pos+1, 0);
    nom = extraerNombre (l[0],pos+1,0,"")
    if (c != '/'):
        if (nom == buscar):
            if ((buscarCapacidad (l[1:], "capability",name,value))==1):
                print (l[0])
                recorrerCapacidadDevice(l[1:], buscar, i+1,name,value)
            else:
                recorrerCapacidadDevice(l[1:], buscar, i,name,value)
        else:
            recorrerCapacidadDevice(l[1:], buscar, i,name,value)
    else:
        recorrerCapacidadDevice(l[1:], buscar, i,name,value)
            
                

def recorrerLineas (l, buscar,i):
    if(l==[] or l==""):
        print (i)
        return
        
    pos = buscarHasta (l[0], '<', 0, 0)
    c = obtenerChar (l[0], pos+1, 0)
    nom = extraerNombre (l[0],pos+1,0,"")


    if (c != '/'):
        if (nom == buscar):
            print (l[0])
            recorrerLineas (l[1:], buscar, i+1)
        else:
            recorrerLineas (l[1:], buscar, i)            
    else:
        recorrerLineas (l[1:], buscar, i)



##--Función recorrerDevices: Dado una lista de lineas(strings), 1 String(device), 1 contador i y los atributos específicos de 1 device(id,user_agent,fall_back)
##--Si lo encuentra gracias a la funcion BuscarDevice, lo imprime indicando 1 si lo encontró y 0 si no lo encontró                    
##recorrerDevices :: ([String] , String , Integer,String,String,String) -> IO()
##recorrerDevices ([], buscar ,i,id,user_agent,fall_back) = print (i)
def recorrerDevices (l, buscar,i,id,user_agent,fall_back):  
    if(l==[] or l==""):
        print (i)
        return

    pos = buscarHasta (l[0], '<', 0, 0)
    c = obtenerChar (l[0], pos+1, 0)
    nom = extraerNombre (l[0],pos+1,0,[])
    
    if (c != '/'):
        if (nom == buscar):
            if (buscarDevice (l[0], "device",id,user_agent,fall_back)==1):
                print (l[0])
                recorrerDevices (l[1:], buscar, i+1,id,user_agent,fall_back)
            else:
                recorrerDevices (l[1:], buscar, i,id,user_agent,fall_back)
        else:
            recorrerDevices (l[1:], buscar, i,id,user_agent,fall_back)
    else:
        recorrerDevices (l[1:], buscar, i,id,user_agent,fall_back)            

            



##--Función recorrerDevices2: Dado una lista de lineas(strings), 1 String(device), 1 contador i y los atributos específicos de 1 device(id,user_agent,fall_back)
##--Si lo encuentra imprime todas las capacidades de ese device y cuántas encontró            
##recorrerDevices2 :: ([String] , String , Integer,String,String,String) -> IO()
##recorrerDevices2 ([], buscar ,i,id,user_agent,fall_back) = print (i)
def recorrerDevices2 (l, buscar,i,id,user_agent,fall_back):
    if(l==[] or l==""):
        print (i)
        return
    
    pos = buscarHasta (l[0], '<', 0, 0)
    c = obtenerChar (l[0], pos+1, 0)
    nom = extraerNombre (x,pos+1,0,[])

    if (c != '/'):
        if (nom == buscar):
            if (buscarDevice (l[0], "device",id,user_agent,fall_back)==1):
                buscarCapacidad2(l[1:],"capability",0)
            else:
                recorrerDevices2 (l[1:], buscar, i,id,user_agent,fall_back)
        else:
            recorrerDevices2 (l[1:], buscar, i,id,user_agent,fall_back)
    else:
        recorrerDevices2 (l[1:], buscar, i,id,user_agent,fall_back)    
                


##--Función recorrerGroupDevice: Dado una lista de lineas(strings), 1 String(device), 1 contador i y un String(grupo en específico)
##--Retorna los devices que pertenecen al grupo indicado y cuántos encontró
##recorrerGroupDevice :: ([String] , String , Integer,String) -> IO()
##recorrerGroupDevice ([], buscar ,i,name) = print (buscar++" soportan ("++name++"): "  ++ show i)
def recorrerGroupDevice (l, buscar,i,name):
    if(l==[] or l==""):
        print (i)
        return
    
    pos = buscarHasta (l[0], '<', 0, 0);
    c = obtenerChar (l[0], pos+1, 0);
    nom = extraerNombre (l[0],pos+1,0,"")

    if (c != '/'):
        if (nom == buscar):
            if ((buscarGrupo(l[1:], "group",name))==1):
                print (l[0])
                recorrerGroupDevice (l[1:], buscar, i+1,name)
            else:
                recorrerGroupDevice (l[1:], buscar, i,name)
        else:
            recorrerGroupDevice (l[1:], buscar, i,name)
    else:
        recorrerGroupDevice (l[1:], buscar, i,name)    
    
        
def main():
    f = open('copiawurfl.xml', 'r+')
    l=f.readlines()
    ##recorrerLineas (l, "device", 0)
    obtenerCapability(l,"built_in_camera", "true", 0)
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
