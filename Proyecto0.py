from io import TextIOWrapper


comandos = ["MOVE",
            "RIGHT",
            "LEFT",
            "ROTATE",
            "LOOK",
            "DROP",
            "FREE",
            "PICK",
            "POP",
            "CHECK",
            "BLOCKEDP",
            "NOP",
            "(REPEAT",
            "IF",
            "DEFINE",
            "TO",
            "END",
            "OUTPUT",
            "(BLOCK"]

comandosNum = ["MOVE",
               "RIGHT",
               "LEFT",
               "ROTATE",
               "DROP",
               "FREE",
               "PICK",
               "POP",
               "REPEAT"]

global_vars = {} # variables locales en formato {nombre: ""}
global_fun = {} # funciones guardadas como texto !o.isnumber : {nombre: cantidad}


def revisar_linea(text: str) -> bool:
    funciona = True
    # print(text)
    palabras = text.strip().split(" ")
    i = 0

    while i < len(palabras):
        palabra = palabras[i]

        if palabra == "IF":
            palabraSig = palabras[i + 1]
            if palabraSig != "BLOCKEDP" and palabraSig != "!BLOCKEDP":
                funciona = False
                break
            palabraSig = palabras[i + 2]
            palabras[i + 2] = palabras[i + 2].replace("[", "")
            if "[" not in palabraSig:
                funciona = False
                break
            else:
                i+=3


        elif palabra not in comandos and palabra.isupper():
            funciona = False
            print(palabras, "-" + palabra, funciona)
            break

        elif (palabra in comandosNum):
            palabraSig = palabras[i + 1]
            esNum = palabraSig.isdigit()
            esVariable = (global_vars.keys().__contains__(palabraSig))
            if not (esNum or esVariable):
                # print(palabra, palabraSig)
                funciona = False
                break
            i += 2
        elif palabra == "LOOK":
            palabraSig = palabras[i + 1]
            if palabraSig not in ["N", "E", "W", "S"]:
                funciona = False
                break
            i += 2
        elif palabra == "CHECK":
            palabraSig = palabras[i + 1]
            if palabraSig not in ["C", "B"]:
                funciona = False
                break
            palabraSig = palabras[i + 2]
            esNum = palabraSig.isdigit()
            esVariable = (global_vars.keys().__contains__(palabraSig))
            if not (esNum or esVariable):
                # print(palabra, palabraSig)
                funciona = False
                break
            i+= 2

        elif palabra == "DEFINE":
            palabraSig = palabras[i + 2]
            print("111")
            if not (palabras[i + 2].isdigit() and palabras[i + 1].islower()):
                funciona = False
                break
            else:
                global_vars[palabras[i + 1]] = ""
                i += len(palabras)
        else:
            i += 1

    return funciona


def revisar_funcion(text: list, data: list) -> bool:
    param = data[2:]
    for p in param:
        print(p)
        global_vars[p] = ""
    if(revisar_bloque(text)):
        for p in param:
            global_vars.pop(p)
        global_fun[data[1]] =len(param)
        return True
    return False


# def revisar_bloque_funcion(lista):


def revisar_bloque(lista: list) -> bool:
    funciona = True
    contParen = 0
    contCorch = 0
    i = 0
    while i < len(lista):
        linea = lista[i]
        linea = linea.replace("\n", "")

        if linea.count("TO") == 1:
            datos = linea.split(" ")
            # print(i, datos)
            for j in range(i + 1, len(lista)):
                linea2 = lista[j]
                if linea2 == "END":
                    funcion = lista[i+1:j+1]
            funciona = revisar_funcion(funcion, datos)
            i = j+1
        else:
            i+= 1

        if linea.count("(") != 0:
            contParen += 1
        elif linea.count(")") != 0:
            linea = linea.replace(")", "")
            contParen -= 1
        elif linea.count("[") != 0:
            contParen += 1
        elif linea.count("]") != 0:
            linea = linea.replace("]", "")
            contParen -= 1

        funciona = funciona and revisar_linea(linea)

    if (contCorch != 0) or (contParen != 0):
        funciona = False


    return funciona

def main(nombre:str):

    funciona = True
    file = open(nombre, "r")
    lineas = file.readlines()

    if not revisar_bloque(lineas):
        funciona = False

    print(funciona)

main("input.txt")
