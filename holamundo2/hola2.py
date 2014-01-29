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
    def __init__(self):
        self.iddev=None
        self.useragent=None
        self.fallback=None
        self.lgroups=None
        
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
   generic=Device()
   leerArchivo()
    

main()