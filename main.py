from tkinter import *
from tkinter import messagebox
from random import *
import time
import os

# Declaraciones

# Variable global
# Para que sea mas facil y legible el codigo
PATH = os.path.dirname(os.path.abspath(__file__))+"/"

# Ventana inicial y sus propiedades
master = Tk()
master.geometry("570x555")
master.title("Master Mind")
master.resizable(0,0)
master.configure(background = 'black')

# Clase de botones
class Botones():
    # Permite que el codigo bajo la funcion sea ejecutado
    # al instanciar la clase
        def __init__(self,i,w,tablero,lista):
                img = PhotoImage(file=PATH+str(lista)+".gif")
                self.button = Label(tablero, image=img)
                self.button.img = img
                self.button.number = lista
                self.button.place(x=20+90*i,y=360+tablero.relPos-60*w)
                self.button.bind ("<Button-1>",changeColor)

# Clase de CodeBreaker
class CodeBreaker():
    turno = 0                       #Turno actual
    intento = []                    #Intento actual

# Clse de juego
class Juego():
    rondasMaximas = 0               #Rondas maximas
    rondaActual = 1                 #Ronda actual
    faseActual = 0                  #Fase actual
    dificultad = 0                  #Dificultad
    nombreUsuario = ""              #Nombre del usuario
    codemaker = 0                   #Quien es codemaker
    ganador = ""                    #Ganador de la partida
    puntosUsu = 0                   #Puntos usuario
    puntosMaq = 0                   #Puntos maquina
    claveActual = []                #Clave del codeMaker actual
    intentosAnteriores = []         #Intentos jugados anteriormente
    ultimaResolucionUsuario = 0     #Turnos en los que gana el usurio
    ultimaResolucionMaquina = 0     #Turnos en los que gana la maquina

# EVENTO Cambia el color de los botones al hacer click
def changeColor(event):
    # Pre: True
    # Post: El boton cambia de color

        # Permite que continue ciclo colores
        if event.widget.number >= 7:
                event.widget.number = 0
        event.widget.number = event.widget.number +1
        
        # Cambia la imagen
        new = PhotoImage(file=PATH+str(event.widget.number)+".gif")
        event.widget.configure(image=new)
        event.widget.img = new

def crearBotones(largo,TURNO,tablero,lista = [1,1,1,1,1]):
    # Pre: True
    # Post: Se crea una lista de botones, de la clase botones, y binded
    botones=[Botones(i,TURNO,tablero,lista[i]) for i in range(0,largo)]
    return botones

def crearColor(coorx,coory,spacex,numero,i,tablero):
    # Pre: True
    # Post: Permite crear una ficha especificando numero y posicion
    new = PhotoImage(file=PATH+str(numero)+".gif")
    boton = Label(tablero,image=new)
    boton.img = new
    boton.place(x=coorx+spacex*i,y=coory,)

def revelarSecreto(x,y,spacex,lista,tablero):
    # Pre: True
    # Post:  Crea una lista ordenada de 5 botones  
    for i in range(0,len(lista)):
                crearColor(x,y,spacex,lista[i],i,tablero)   

# Ventana para inicializar
def Inicializar(master):
    #Pre: True
    #Post: Se obtienen los valores para inicializar el juego
    
    #Declaraciones
    dificultades=["Rápido","Relajado","Lento"]
    dificultadesTurnos= [5,10,15]
    v = IntVar()        #Declaraciones de Tkinter
    rondas = IntVar()   #Declaraciones de Tkinter
    rondas.set("5")     #Inicializacion Tkinter
    v.set("0")          #Inicializacion Tkinter
    juego = Juego()     #Declaracion de juego nuevo
    
    #Desaparece ventana principal
    master.withdraw()

    #Genera una nueva ventana
    seleccion = Toplevel()
    seleccion.title("Master Mind - Dificultad")
    seleccion.geometry("570x555")
    

    #Interfaz grafica
    e = Entry(seleccion,justify=CENTER)
    e.place(x=200,y=175)
    e.focus_set()
    Label(seleccion,text="Nombre").place(x=255,y=150)
    Label(seleccion,text="Rondas").place(x=255,y=200)
    
    #Boton para empezar
    medio = Button(seleccion,text="Empezar", \
    command = lambda: crearJuego(juego,dificultadesTurnos[v.get()],\
    rondas.get(),e.get(),seleccion))
    medio.place(x=240,y=300)
    
    #Coloca las dificultades
    for i in range(0,len(dificultades)):
        Radiobutton(seleccion, text=dificultades[i], variable=v, \
                value=i).place(x=130+100*i,y=250)
    
    #Coloca las rondas
    for i in range(1,11):
        Radiobutton(seleccion, text=i, variable=rondas, \
                value=i).place(x=20+40*i,y=220)

# Se establecen los parametros
def crearJuego(juego,dificultad,rondas,nombre,seleccion):
    #Pre: True
    #Post: Se inicia el juego
    establecerParametros(juego,dificultad,rondas,nombre)
    iniciar(juego,seleccion)

def establecerParametros(juego,dificultad,rondas,nombre):
    #Pre: True
    #Post: juego.dificultad != 0 and juego.rondasMaximas != 0 and
    #   juego.nombreUsuario != ""
    juego.dificultad = dificultad
    juego.rondasMaximas = rondas
    if nombre == "":
        juego.nombreUsuario = "Default"
    else:
        juego.nombreUsuario = nombre

def iniciar(juego,seleccion,opcion='nuevo'):
    #Pre: True
    #Post: Sirve para ocultar una pantalla y crear un tablero
    seleccion.withdraw()
    crearTablero(juego,opcion)

def generarLista(numero):
    #Pre: True
    #Post: Genera una lista de numeros random
    lista = []
    for i in range(0,numero):
        lista = lista + [randint(1,7)]  
    return lista

def desactivarBotones(botones):
    #Pre: True
    #Post: Desactiva el click de los botones
        for i in range(0,5):
                botones[i].button.unbind("<Button-1>")

def verificar(usuario,tablero,boton,juego):
    #Pre: True
    #Post: Se obtiene el intento actual del codeBreaker, se compara con 
    #       la clave secreta, se grafica el intento y el resultado y 
    #           se evalua si debe jugarse nuevamente, o ya acabo la fase
        
        #Genera el intento
        B = []
        for i in range(0,5):
               B = B + [usuario.intento[i].button.number]
        A = list(B)
        juego.intentosAnteriores = juego.intentosAnteriores + [A]
        
        #Compara la clave y el intento 
        resultado = probar(B,juego.claveActual)
        print("Hay: "+str(resultado[0])+" , \
                perfectos: "+str(resultado[1]))
        
        #Grafica resultado
        revelarSecreto(75,370-60*usuario.turno+tablero.relPos,90,resultado[3],tablero)
    
        #Verifica si termino la fase
        if usuario.turno >= juego.dificultad-1 or resultado[2]:
                revelarSecreto(45,20,75,juego.claveActual,tablero)
                boton.config(state = DISABLED)
                if usuario.turno-1 != 0:
                    juego.ultimaResolucionUsuario = usuario.turno
                    nuevo = Button(tablero,text="Continuar",command=lambda: finRonda(juego,tablero))
                    nuevo.place(x=485,y=320+tablero.relPos)
                    
        usuario.turno = usuario.turno + 1
        desactivarBotones(usuario.intento)
        print(juego.intentosAnteriores)
        if usuario.turno <= juego.dificultad-1 and not(resultado[2]):
                usuario.intento = crearBotones(5,usuario.turno,tablero,A)
        return B

def ganador(juego,tablero):
    #Pre: True
    #Post: Hay un ganador en pantalla
    
    #Desaparece la ventana que lo llamo
    tablero.withdraw()
    
    # Genera una nueva venana
    ganador = Toplevel()
    ganador.title("Ganador")
    ganador.geometry("570x555")
    
    # Interfaz
    Button(ganador, text="Volver a jugar", command=lambda: Inicializar(ganador)).place(x=250,y=300)
    Label(ganador,text = "Puntos Maquina: "+str(juego.puntosMaq)).place(x=240,y=45)
    Label(ganador,text = "Puntos Usuario: "+str(juego.puntosUsu)).place(x=243,y=65)
   
    # Gana la maquina
    if juego.puntosMaq > juego.puntosUsu:
        Label(ganador,text = "Gana la maquina").place(x=245,y=90)  
    
    # Hay empate
    elif juego.puntosMaq == juego.puntosUsu:
        Label(ganador,text = "EMPATE").place(x=245,y=90)
    
    # Gana el usuario
    else:
        Label(ganador,text = "Gana el usuario").place(x=245,y=90)

def finRonda(juego,tablero):
        #Pre: True
        #Post: juego.ultimaResolucionUsuario == juego.ultimaResolucionMaquina and 
        #      juego.puntosUsu += 1 and juego.puntosMaq += 1 or
        #      juego.ultimaResolucionUsuario > juego.ultimaResolucionMaquina and
        #      juego.puntosMaq +=3 or
        #      juego.ultimaResolucionUsuario < juego.ultimaResolucionMaquina and
        #      juego.puntosUsu +=3
        #      Calcula las fases y el proximo codemaker

        if juego.faseActual == 1:
                juego.faseActual = 0
                juego.rondaActual = juego.rondaActual+1
                if juego.ultimaResolucionUsuario == juego.ultimaResolucionMaquina:
                    juego.puntosUsu += 1
                    juego.puntosMaq += 1
                elif juego.ultimaResolucionUsuario > juego.ultimaResolucionMaquina:
                    juego.puntosMaq +=3
                else:
                    juego.puntosUsu +=3

        elif juego.faseActual == 0:
               juego.faseActual = 1

        if juego.codemaker == 1:
                juego.codemaker = 2
        elif juego.codemaker == 2:
                juego.codemaker = 1

        
        if juego.rondaActual <= juego.rondasMaximas:
            print("El codemaker "+str(juego.codemaker))
            iniciar(juego,tablero)
        else:
            ganador(juego,tablero)

def probar(intento,jefe):
        #Pre: True
        #Post: Genera una lista con el resultado de comparar clave e intento      

        resultado = ["N" for i in range(0,5)]
        encontraste = 0
        perfect = 0
        ganador = 0
        aux = list(jefe)
        
        # P Perfecto , E esta , N No esta
        # Quito todos los perfectos
        
        for i in range(0,len(intento)):
                if intento[i] == aux[i]:
                        resultado[i] = "P"
                        perfect = perfect + 1
                        aux.pop(i)
                        aux.insert(i,0)
                        intento.pop(i)
                        intento.insert(i,-1)
        
        # Veo cuales estan en otra posicion

        for i in range(0,len(intento)):
                if aux[i] != intento[i]:
                    if  any(x for x in aux if x == intento[i]):
                            resultado[i]="E"
                            encontraste = encontraste + 1
                            pos = aux.index(intento[i])
                            aux.remove(intento[i])
                            aux.insert(pos,0)
        
        # Veo si la persona gana
        if perfect == 5:
                ganador = 1

        return encontraste,perfect,ganador,resultado

def jugar(jefe,tablero,maquina,clave,intentoAnterior=[]):
    #Pre: True
    #Post: Permite que la maquina juegue y se grafique el turno y resultado
    
    intento = list(intentoAnterior)
    
    #Graficar Turno
    revelarSecreto(20,360+tablero.relPos-60*maquina.turno,90,intentoAnterior,tablero)
    
    #Resultado del turno
    resultado = probar(intentoAnterior,clave)[3]
    revelarSecreto(75,370-60*maquina.turno+tablero.relPos,90,resultado,tablero)
    
    #Actualiza la interfaz
    tablero.update()
    
    #Actualiza los turnos
    maquina.turno = maquina.turno +1
    return resultado,intento
    
def generar(resultado,intentoAnterior,permutar,noesta):
    #Pre: True
    #Post: Genera una nueva clave basandose en el resultado anterior

    nuevoIntento=list(intentoAnterior)
    for i in range(0,len(resultado)):
        if resultado[i] == 'P':
            nuevoIntento[i] = intentoAnterior[i]
        elif resultado[i] == 'N':
            if intentoAnterior[i] not in noesta:
                noesta = noesta+[intentoAnterior[i]]
            #0 Significa que su color cambiara random 
            nuevoIntento[i] = 0
        elif resultado[i] == 'E':
            if intentoAnterior[i] not in permutar:
                permutar = permutar+[intentoAnterior[i]]
            nuevoIntento[i] = 0
    
    for i in noesta:
        if i in permutar:
            noesta.remove(i)

    permutarTemp = list(permutar)

    
    for i in range(0,len(resultado)):
        while nuevoIntento[i]==0:
            if permutarTemp != []:
                intentoAnterior[i] = choice(permutarTemp)
                permutarTemp.remove(intentoAnterior[i]) 
            if permutarTemp == []:
                while nuevoIntento[i] in noesta:
                    nuevoIntento[i] = randint(1,7)  

    return nuevoIntento,noesta,permutar

            
            
def decifrar(tablero,maquina,go,juego):
    #Pre: True
    #Post: La maquina juega su turno

    juego.claveActual = []
    
    #Se obtiene la clave ingresada por el usuario
    for i in maquina.intento:
        juego.claveActual = juego.claveActual + [i.button.number]
        i.button.place_forget()
    
    #Se grafica la clave
    revelarSecreto(45,20,75,juego.claveActual,tablero)
    
    #Crear el primer intento de la maquina
    maquina.intento = generarLista(5)
    go.place_forget()
    primerIntento = list(maquina.intento)
    permutar = []
    noesta = [0]

    #La maquina intenta adivinar la clave
    #Cota: maquina.turno - juego.dificultad-1

    while maquina.turno <= juego.dificultad-1:
        resultado,intentoAnterior = jugar(maquina.intento,tablero,maquina,juego.claveActual,primerIntento)
        if maquina.intento == juego.claveActual:
                break
        primerIntento,noesta,permutar = generar(resultado,intentoAnterior,permutar,noesta)
        maquina.intento = list(primerIntento)
        
    juego.ultimaResolucionMaquina = maquina.turno-1
    nuevo = Button(tablero,text="Continuar",command=lambda: finRonda(juego,tablero))
    nuevo.place(x=485,y=380+tablero.relPos)
    

def ProcedimientoCargar(nombreArchivo,master):
    #Pre: True
    #Post: Se carga un archivo

    try:
        juego,usuario = CargarJuego(nombreArchivo)
    except:
        ventanaCargar(master)
        messagebox.showerror("Error", "Ha ocurrido un error al cargar el fichero")
        return
    iniciar(juego,master,'cargar')

def GuardarJuegoVentana(juego,usuario):
    #Pre: True
    #Post: Se obtiene el nombre del archivo para Guardar

    ventana = Toplevel()
    ventana.title("Guardar Partida") 
    e = Entry(ventana,justify=CENTER)
    e.place(x=20,y=20)
    Label(ventana,text = "Nombre de archivo").place(x=40,y=45)
    a = Button(ventana,text = "Guardar",command = lambda: GuardarJuego(e.get(),juego,ventana))
    a.place(x=60,y=90)
    

def GuardarJuego(nombreArchivo,estructura,ventana):
        #Pre: True
        #Post: El archivo nombreArchivo, posee la estructura guardada
        #      Y se cierra la ventana
        if estructura.faseActual == 0:
                ultimaResolucion = 0
        elif estructura.faseActual == 1:
                ultimaResolucion = 1 + int(estructura.ultimaResolucionMaquina)

        with open(nombreArchivo,'w') as f:
                string = str(estructura.dificultad//5)+"\n"
                string = string + estructura.nombreUsuario+"\n"+"\n"
                string = string + str(estructura.puntosMaq)+" "+str(estructura.puntosUsu)+" "
                string = string + str(ultimaResolucion)+"\n"
                string = string + str(estructura.rondaActual) + " "
                string = string + str(estructura.rondasMaximas)+"\n"

                for i in estructura.claveActual:
                        string = string + str(i) + " "
                string = string+"\n"
                for i in estructura.intentosAnteriores:
                        string = string + "\n" 
                        for p in i:
                                string = string + str(p) + " "
                f.write(string)
        f.closed

        ventana.withdraw()


def CargarJuego(nombreArchivo):
        #Pre: nombreArchivo posee una estructura valida
        #Post: Las variables del juego son cargadas

        estructura = Juego()
        usuario = CodeBreaker()

        x = " "
        with open(nombreArchivo) as f:
                estructura.dificultad = int(f.readline().split()[0])*5
                estructura.nombreUsuario = f.readline().split()[0]
                f.readline()
                aux = [int(i) for i in f.readline().split()]
                estructura.puntosMaq = aux[0]
                estructura.puntosUsu = aux[1]
                if aux[2] == 0:
                    pass
                else :
                    estructura.faseActual = 1
                    estructura.ultimaResolucionMaquina = aux[2]
                aux = [int(i) for i in f.readline().split()]
                estructura.rondaActual = aux[0]
                estructura.rondasMaximas = aux[1]
                estructura.claveActual = [int(i) for i in f.readline().split()]
                f.readline()
                while x != "":
                        x = f.readline()
                        if x != "":
                                estructura.intentosAnteriores=estructura.intentosAnteriores + [[int(i) for i in x.split()]]
        f.closed
    
        return estructura,usuario
  
# Crea un tablero con las opciones indicadas
def crearTablero(juego,opcion="nuevo"):
    #Pre: {dificultad == 5 or dificultad == 10 or dificultad == 15 and
    #   any(x for x in range(1,11) if x == rondas)}
    #
    #Post: Crea un tablero con el CodeMaker definido, la dificultad definida, 
    #   las rondas definidas y los puntajes definidos:
    
    # Se crea ventana del tablero
    tablero = Toplevel()
    tablero.title("Master Mind")
    tablero.relPos = 300*(juego.dificultad//5-1)
    tablero.geometry("600x"+str(430+tablero.relPos))
    
    # Se pone la ronda actual y puntaje
    Label(tablero,text = "Usuario: "+str(juego.nombreUsuario)).place(x=470,y=2)
    Label(tablero,text = "Ronda: "+str(juego.rondaActual)).place(x=470,y=20)
    Label(tablero,text = "Puntos Maquina: "+str(juego.puntosMaq)).place(x=470,y=60)
    Label(tablero,text = "Puntos Usuario: "+str(juego.puntosUsu)).place(x=470,y=80)
    
    # 1 CODEMAKER USUARIO
    # 2 CODEMAKER MAQUINA
    # Si no hay CodeMaker lo genera
    
    if opcion != 'cargar':
        juego.intentosAnteriores = []
    if juego.codemaker == 0:
        if opcion == 'cargar':
            juego.codemaker = 2
        else:
            juego.codemaker = randint(1,2)  
        
        if juego.codemaker == 2:
            juego.empiezaFase = juego.nombreUsuario
        elif juego.codemaker == 1:
            juego.empiezaFase = "Maquina"
        print("Seleccionando RANDOM" + str(juego.codemaker))
    
    # Si el CodeMaker es USUARIO:
    if juego.codemaker == 1:
        print("Code Maker Usuario")
        maquina = CodeBreaker()
        maquina.intento = crearBotones(5,5.3,tablero)
        go = Button(tablero, text="Listo!", command= lambda: decifrar(tablero,maquina,go,juego))
        go.place(x=200,y=tablero.relPos+150)
        
    # Si el CodeMaker es MAQUINA:
    if juego.codemaker == 2:
        print("Code Maker Maquina")
        revelarSecreto(45,20,75,["block" for i in range(0,5)],tablero)
        
        usuario = CodeBreaker()
        ultimoResultado = [[0,0,0,0,0],[1,1,1,1,1]]

        if opcion == 'cargar':
                intentos = list(juego.intentosAnteriores)
                for i in range(0,len(juego.intentosAnteriores)):
                    ultimoResultado = jugar(1,tablero,usuario,juego.claveActual,intentos[i])

        else:
            juego.claveActual = generarLista(5)
        
        if usuario.turno < juego.dificultad and ultimoResultado[1]!=juego.claveActual:    
        #HACER TRAMPA
        #revelarSecreto(45,20,75,jefe,tablero)
            if opcion == 'cargar':
                usuario.intento = crearBotones(5,usuario.turno,tablero,ultimoResultado[1])
            else:
                usuario.intento = crearBotones(5,usuario.turno,tablero)
        else:
            revelarSecreto(45,20,75,juego.claveActual,tablero)
            
        #Boton verificar
        enviar2 = Button(tablero,text="Intentar", \
                    command=lambda: verificar(usuario,tablero,enviar2,juego))
        enviar2.place(x=485,y=380+tablero.relPos)
        
        #Boton guardar
        guardar = Button(tablero,text="Guardar", \
                    command=lambda: GuardarJuegoVentana(juego,usuario))
        guardar.place(x=485,y=350+tablero.relPos)
        
        #Boton leyenda
        leyenda = Button(tablero,text="Leyenda", \
                    command=lambda: leyendaVentana())
        leyenda.place(x=485,y=120)
        
        if usuario.turno >= juego.dificultad or ultimoResultado[1]==juego.claveActual:
            enviar2.config(state=DISABLED)
            nuevo = Button(tablero,text = "Continuar",command = lambda: finRonda(juego,tablero))
            nuevo.place(x=485,y=320+tablero.relPos)

def leyendaVentana():
    #Pre: True
    #Post: Muestra la leyenda

    #Ventana
    leyenda = Toplevel()
    leyenda.geometry("400x100")
    
    #Informacion
    Label(leyenda,text="Estrella indica que esta en el lugar perfecto").place(x=50,y=10)
    Label(leyenda,text="El circulo indica que esta en la posicion errada").place(x=50,y=40)
    Label(leyenda,text="La equis indica que ese color no pertenece a la clave").place(x=50,y=70)


def ventanaCargar(master):
    #Pre: True
    #Post: Obtiene el archivo a cargar, y lo carga
    
    # Desaparece la ventana que lo llamo
    master.withdraw()
    
    # Crea una nueva ventana
    cargando = Toplevel()
    cargando.title("Seleccione la partida")
    cargando.geometry("570x555")
        
    Label(cargando,text="Ingrese el nombre del fichero:").place(x=150,y=150)
    
    archivo = Entry(cargando,justify=CENTER)
    archivo.place(x=160,y=175)
    archivo.focus_set()

    boton = Button(cargando,text="Cargar", \
            command = lambda: ProcedimientoCargar(archivo.get(),cargando))
    boton.place(x=200,y=300)




# Animacion del menu principal
def animacion(number):
    #Pre: True
    #Post: La imagen cambia de colores

    holder.delete('Animate')
    if number > 4:
        number = 0
    def change(number):
        holder.create_image(number,0,anchor=NW,image=imagenes[number],tag = 'Animate')
    change(number)
    holder.update_idletasks()
    number = number + 1
    master.update()
    master.after(165,animacion,number)


numero = 1
holder = Canvas(master)
holder.config(background = 'black',borderwidth = 0,highlightthickness=0)
holder.place(x=30,y=150,width=500)
imagenes = []
for i in range(0,5):
    imagenes += [PhotoImage(file=PATH+"M"+str(i)+".gif")]

# Botones de la pantalla inicial
# Juego nuevo / Cargar partida 

imagenNuevo = PhotoImage(file=PATH+"nuevo.png")
imagen = holder.create_image(0,130,anchor=NW,image=imagenNuevo,tag='Juego')
holder.tag_bind(imagen,"<ButtonPress-1>",lambda event:Inicializar(master))

imagenCargar = PhotoImage(file=PATH+"guardar.png")
imagen2 = holder.create_image(220,130,anchor=NW,image=imagenCargar)
holder.tag_bind(imagen2,"<ButtonPress-1>",lambda event: ventanaCargar(master))

master.after(50,animacion,0)

# Mantiene el juego abierto
# Mas facil para cerrar 
int(input(""))
# master.mainloop()
