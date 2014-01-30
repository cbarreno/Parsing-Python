import sys

##print("Hola mundo",'salope',88,'lane soeurs')
##hora=int(input("Ingrese la hora: "))
##if hora>12:
##	print ("Tarde")
##
##fav = 'mundogeek.net'
##if fav == 'mundogeek.net':
##        print ('Tienes buen gusto')
##else:
##        print ('Vaya, que lástima')
##print ('Gracias')
##
##var = 'par' if (7 % 2 == 0) else 'impar'
##
##edad = 0
##while edad < 18:
##        edad = edad + 1
##        print ('Felicidades, tienes ' + str(edad))
##
##
##salir = False
##while not salir:
##        entrada = input()
##        if entrada == 'adios':
##                salir = True
##        else:
##                print (entrada)
##
##edad = 0
##while edad < 18:
##        edad = edad + 1
##        if edad % 2 == 0:
##                continue
##        print ('Felicidades, tienes ' + str(edad))

##secuencia = ['uno', 'dos', 'tres']
##for elemento in secuencia:
##        print (elemento)
##
##def mi_funcion(param1, param2):
##        print (param1)
##        print (param2)

def varios(param1, param2, **otros):
        for i in otros.items():
                print (i)

def varios2(param1, param2, *otros):
        for val in otros:
                print (val)


def f(x, y):
        x = x + 3
        y.append(23)
        print (x, y)

def sumar(x, y):
        return x + y
print (sumar(3, 2))

def f(x, y):
        return x * 2, y * 2
a, b = f(1, 2)


class Terrestre:
        def desplazar(self):
                print ('El animal anda')
class Acuatico:
        def desplazar(self):
                print ('El animal nada')
class Cocodrilo(Terrestre, Acuatico):
        pass

c = Cocodrilo()
c.desplazar()



