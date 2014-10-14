import os, sys

BC = []
LargoBC = 0

global l_vars

##### V A L I D A C I O N E S ################################################################################

def verificaciones(resp,tamanno):
    if resp[tamanno-1] != ".":
        return 1
    inicio = 0
    while tamanno > inicio:
        if resp[inicio] == ".":
            if resp[inicio-1] == "," or resp[inicio-1] == ":" or resp[inicio-1] == ";":
                return 1
        if resp[inicio] == "(":
            avance = 1
            while resp[inicio+avance] != ")":
                if inicio+avance != tamanno:
                    break
                if resp[inicio+avance] == "(":
                    return 1
                avance = avance + 1
        if resp[inicio] == ")":
            avance = -1
            while resp[inicio+avance] != "(":
                if inicio+avance == tamanno:
                    return 1
                if resp[inicio+avance] == ")":
                    return 1
                avance = avance - 1
        inicio = inicio + 1    
    return 0

# Funcion que verifica las reglas
def regla(resp,tamanno):
    if (':-' not in resp):
        return "Error de estructura de predicado"
    bandera = verificaciones(resp,tamanno)
    if bandera == 1 and False:
        return"Error Regla"
    if resp[tamanno-1] != "." and False:
        return "Error en la regla22"
    inicio = 0
    if resp[inicio].islower() != True and False:
        return "Error en la regla4"
    while tamanno == inicio:
        if resp[inicio] == ":":
            atras = inicio -1
            while resp[atras] !="(":
                atras = atras - 1
                aux = atras
            while aux < inicio or aux < (inicio+1):
                if resp[aux+1].islower() != False and resp[aux+1] != ")":
                    return "Error en la regla"
                aux = aux + 1
            if resp[inicio+2].islower() != True and resp[inicio+2] != "!":
                return "Error en la regla"
        if resp[inicio]=="(":
            if resp[inicio-1] ==",":
                return "Error en la regla"
            aux = 1
            while resp[inicio+aux] != " ":
                if resp[inicio+aux] == ")":
                    break
                if resp[inicio+aux] == ".":
                    return "Error en la regla"
                aux = aux + 1
        inicio = inicio + 1
    return "Corecto"

# Funcion que verifica los hechos que con variables estaticas
def hechoMay(resp,tamanno):
    inicio = 0
    while tamanno > inicio:
        if resp[inicio] == ",":
            if resp[inicio+1] == "[":
                if resp[inicio+2].islower() != False or resp[inicio+4].islower() != False or resp[inicio+5] != "]" or resp[inicio+3] != "|":
                    return 1
        inicio = inicio + 1
    return 0

# Funcion que verifica los hechos que con variables dinamicas
def V_hecho(resp,tamanno):
    inicio = 0
    if resp.find(";") != -1:
        return "Error"
    error = hechoMay(resp,tamanno)
    if error == 1:
        return "Error"
    if resp[inicio].islower() != True:
        return "Error en el hecho3"
    bandera = verificaciones(resp,tamanno)
    if bandera == 1:
        return "Error punto"        
    return "Correcto"

#Funcion inicial, define si la entrada es una regla o hecho, ENTRADA PRINCIPAL DE REGLAS Y HECHOS
def inicio_verificaciones(entrada): 
    resp = entrada.replace(" ","")
    if (')' not in resp) or ('(' not in resp) or resp[0].isupper() or ('.' not in resp):
        solu = 'Error de estructura'
    tamanno = len(entrada)
    letra = 0
    while tamanno > letra:
        if resp[letra] == ":":
            if resp[letra-1] != ")":
                return "Error"
            if resp[letra+1] == "-":
                solu = regla(resp,tamanno)
                return solu
        letra= letra + 1
    solu = V_hecho(resp, tamanno)
    return solu

### F I N   V A L I D A C I O N E S ##########################################################################


############################## C L A S E S ####################################################
class hecho:
    def __init__(self, funtor, datos): #String funtor, lista datos.
        self.funtor = funtor #string[0]
        self.aridad = len(datos)#len(string[1])
        self.datos = datos#string[1]
        
    def agregarHecho(self): #agrega hecho a listaHechos
        global LargoBC
        BC.append(self)
        LargoBC+=1            

class predicado:
    def __init__(self, funtor, datos,reglas): #String funtor, lista datos, lista reglas.
        self.funtor = funtor #string[0]
        self.aridad = len(datos)#len(string[1])
        self.datos = datos#string[1]
        self.reglas = reglas#string[2]
        
    def agregarPredicado(self): #agrega hecho a listaHechos
        global LargoBC
        BC.append(self)
        LargoBC+=1
###############################################################################################


####################### FORMATO DE LOS STRINGS RECIBIDOS ######################################
        
def separaHechos(string): #Recibe string: "amigo(Juan,Carlos),agrada(Carlos,Isa);agrada(Carlos,Miguel)"
    string = string.replace('),',') and ')
    string = string.replace(');',') or ')
    string = string.split() #Lista con este formato: ['amigo(Luis,Carlos)', 'or', 'agrada(Luis,Ana)', 'and', 'agrada(Luis,Stef)']
    largo = len(string)
    cont = 0
    resultado = []
    while(cont<largo):        
        if(cont%2 == 0):
            resultado = resultado + fragmenta(string[cont]) #Utiliza la funcion fragmenta para separa cada hecho.
        else:
            resultado = resultado + [string[cont]]
        cont = cont + 1
    return resultado #Devuelve lista como: ['amigo', ['Luis', 'Carlos'], 'or', 'agrada', ['Luis', 'Ana']]

def quita_espacios(lista): #Quita los espacios de cada elemento de la lista
    i = 0
    while i < len(lista):
        lista[i] = lista[i].replace(" ","")
        i+=1
    return lista

def agarra_nombre(string):
    string = string.split('(')
    return string[0]
    
def agarra_predicado(string):
    string = string.split(":-")
    return string[1].replace(" ","")

def agarra_parentesis(string): #devuelve lista con 1 o n argumentos de string
    string = string.split('(')
    string = string[1]
    string = string.split(')')
    string = string[0]
    string = string.split(',')
    return quita_espacios(string)

def fragmenta(string):  #Devuelve lista con:
                        #l[0] = nombre_hecho
                        #l[1] = lista con argumentos del hecho o predicado
                        #l[2] (Solo si es predicado) = devuelve lo que esta despues del :-                         
    fragmentos = [] + [agarra_nombre(string)]
    fragmentos = fragmentos + [agarra_parentesis(string)]
    if ":-" in string:
        fragmentos = fragmentos + [agarra_predicado(string)]
    return fragmentos

###############################################################################################

########################### MANEJO DE HECHOS / PREDICADOS #####################################

def hecho_o_pre(obj):
    if str(type(obj)) == "<class '__main__.hecho'>":
        return "hecho"
    else:
        return "pre"

def unificar(a,b): #Funcion que unifica variables y verifica si constantes unifican
    global l_vars
    if a[0].islower() and b[0].islower() and a==b:
        return True
    elif a[0].islower() and b[0].islower() and a != b:
        return False
    elif a in l_vars and a[0].isupper():
        if l_vars[a] == b and l_vars[a].islower():
            return True
        elif l_vars[a].isupper():
            l_vars[l_vars[a]] = b
            l_vars[a] = b
            return True
        else:
            return False
    elif b in l_vars and b[0].isupper():
        if l_vars[b] == a and l_vars[b].islower():
            return True
        elif l_vars[b].isupper():
            l_vars[l_vars[b]] = a
            l_vars[b] = a
            return True
        else:
            return False
    else:
        l_vars[a] = b
        l_vars[b] = a
        return True

def comp_datos(l1,l2): #compara los datos de entrada para saber si tiene posibilidad de unificacion
    i = 0
    l = len(l1)
    while i < l:
        if l1[i][0].islower() and l2[i][0].islower() and l1[i] != l2[i]:
            return False
        i += 1
    return True

def hecho_res(i,aridad,hechoCompara,datos): #Verifica que los datos de 2 hechos se puedan unificar, si es asi, los unifica
    while i < aridad:
        if unificar(hechoCompara.datos[i],datos[i]):
            if i == aridad-1:
                return True
            else:
                pass
        else:
            return False
        i += 1
    return True

def imp_dic(datos): #Imprime las unificaciones que va haciendo
    global l_vars
    lista = l_vars.keys()
    for i in lista:
        if i in datos and i[0].isupper():
            print(i + ' = ' + l_vars[i])

def comp_hecho_predicado(hecho): #Recibe un objeto de tipo hecho, devuelve true o false si tiene mismo funtor, aridad y datos.
    global l_vars
    res = False
    cont = 0
    funtor = hecho.funtor
    aridad = hecho.aridad
    datos = hecho.datos
    while cont < LargoBC and not res:
        hechoCompara = BC[cont]
        if hechoCompara.funtor == funtor and hechoCompara.aridad == aridad:
            if comp_datos(hechoCompara.datos,datos):
                if hecho_o_pre(hechoCompara) != "pre":
                    res = hecho_res(0,aridad,hechoCompara,datos)
                    imp_dic(datos)
                else:
                    i = 0
                    while i<aridad:
                        unificar(hechoCompara.datos[i],datos[i])
                        i+=1
                    reglas = separaHechos(hechoCompara.reglas)
                    res = evaluar_pre(reglas)
                    imp_dic(datos)
            else:
                res = False
        cont = cont + 1
    return res

def evaluar_pre(lista): #Funcion "recursiva" para evaluar valides de predicados.
    Hecho = hecho(lista[0],lista[1])
    if len(lista) == 2:
        return comp_hecho_predicado(Hecho)
    elif lista[2] == 'or':
        return comp_hecho_predicado(Hecho) or evaluar_pre(lista[3:])
    else:
        return comp_hecho_predicado(Hecho) and evaluar_pre(lista[3:])

def inBC(he_pre): # Devuelve True/False si obj esta en BC
    global BC
    global LargoBC
    lista_res = []
    if hecho_o_pre(he_pre) == "hecho":
        he = he_pre.funtor
        for i in BC:
            if hecho_o_pre(i) == "hecho" and i.funtor == he:
                if i.datos == he_pre.datos:
                    return True
        return False
    else:
        pre = he_pre.funtor
        for i in BC:
            if hecho_o_pre(i) == "pre" and i.funtor == pre:
                if i.reglas == he_pre.reglas:
                    return True
        return False
###############################################################################################

def escribe(string): #Equivalente a funcion write de Prolog
    i = 0
    string = string.replace("write(","")
    string = string.replace(")","")
    lista = string.split(",")
    while lista != []:
        if lista[0] == 'nl':
            print('\n')
        else:
            print(lista[0],end='')
        lista = lista[1:]
    print()

def consulta(): #Modo definicion
    global BC
    global LargoBC
    string = input("Modo Definición: ?- ")
    while string != "</define>":
        val = inicio_verificaciones(string)
        string = fragmenta(string)
        if val[0:5] == "Error":
            print(val)
        elif len(string) == 3: #Si es igual a 3 es predicado y lo evalua
            new_str = predicado(string[0],string[1],string[2])
            if inBC(new_str):
                print("Predicado ya existe en la Base de Conocimientos")
            else:
                new_str.agregarPredicado()
                print("Predicado agregado exitosamente!")
        else: #Sino es hecho y lo agrega a la base de conocimientos
            new_str = hecho(string[0],string[1])
            if inBC(new_str):
                print("Hecho ya existe en la Base de Conocimientos")
            else:
                new_str.agregarHecho()
                print("Hecho agregado exitosamente!")
                print("Tamaño de Base de conocimientos: ",LargoBC)
        string = input("Modo Definición: ?- ")

def inicio(): #Modo consulta (Inicio de programa)
    global l_vars
    estado = 1
    while estado:
        string = input("?- ")
        if string != '':
            val = inicio_verificaciones(string)
        if string == '':
            pass
        elif string == "<define>":
            consulta()
        elif string == "Exit":
            estado = 0
        elif string == "nl":
            print()
        elif string == "<info>":
            print('Hecho por: Fabian Fernandez / Pablo Corrales)')
        elif string == "i_BC":
            print(BC)
        elif val[0:5] == "Error":
            print(val)
        else:
            if "write" in string:
                escribe(string)
            else:
                string = fragmenta(string)
                new_str = hecho(string[0],string[1])
                l_vars = {}
                if comp_hecho_predicado(new_str) == True:
                    print("YES")
                else:
                    print("NO")
    print("Fin de Tarea Programada 2")

inicio()
