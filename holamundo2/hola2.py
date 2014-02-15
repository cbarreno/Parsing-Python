class Arbol:
    def __init__(self,contenido,lhijos): #constructor
        self.contenido=contenido
        self.lhijos=lhijos  
    def getContenido(self):
        return self.contenido
    def getLhijos(self):
        return self.lhijos
    def setContenido(self,newContenido):
        self.contenido=newContenido
    def setLhijos(self,newLhijo):
        self.lhijos=newLhijos 
    def insertarNodo(self,arbolNew):
        self.lhijos.append(arbolNew)
    def arbolvacio(self):
        if self.contenido==None & self.lhijos==None:
            return 1
        else:
            return 0
     
  
class Devices:
    def __init__(self,ldevice): #constructor
        self.ldevice=ldevice
        self.nivel=0
    def getLdevice(self):
        return self.ldevice
    def setLdevice(self,newLdevice):
        self.ldevice=newLdevice
    def imprimirDevices(self):
        for elemento in self.ldevice:
            elemento.imprimirDevice()
        
class Device:
    def __init__(self,iddev,useragent,fallback,lgroups): #constructor
        self.iddev=iddev
        self.useragent=useragent
        self.fallback=fallback
        self.lgroups=lgroups
        self.nivel=1
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
    def setLgroups(self,newLqroups):
        self.lgroups=newLgroups
    def imprimirDevice(self):
        print ("id="+self.iddev+"user_agent="+self.useragent+"fallback="+self.fallback)
        for elemento in self.lgroups:
            elemento.imprimirGroup()        
    
            
class Group:
    def __init__(self,idgroup,lcapabilities): #constructor
        self.idgroup=idgroup
        self.lcapabilities=lcapabilities
        self.nivel=2
    def getIdgroup(self):
        return self.idgroup
    def setIdgroup(self,newIdgroup):
        self.idgroup=newIdgroup
    def imprimirGroup(self):
        print ("id="+self.idgroup)
        for elemento in self.lcapabilities:
            elemento.imprimirCapability()
                    
class Capability:
    def __init__(self,idcap,name,value): #constructor
        self.idcap=idcap
        self.name=name
        self.value=value
        self.nivel=3
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
    def imprimirCapability(self):
        print ("id="+self.idcap+"name="+self.name+"value="+self.value)
        

def leerArchivo():
    archivo = open('miercoles.xml', 'r+')
    #l=archivo.read()
    print(archivo.read())
    archivo.close()
    

def main():
   # archivo = open('miercoles.xml', 'r+')
    #l=archivo.read()
    #print(archivo.read())
   # archivo.close()
   #print("hola jordy")
    leerArchivo()
    

main()