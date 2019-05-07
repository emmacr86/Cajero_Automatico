import os
import sys
import datetime
import time
#Funcion devolver cliente
#Parametros : usuario string
#Retorna : Devuelve la informacion de la fila mediante la verificacion del usuario
def devolver_cliente(usuario):
    for cliente in lista_clientes:
        if cliente [0]==usuario:
            return cliente
#Funcion para remplazar un cliente por otro
#Parametros : Cambios en los usuarios/Usuarios Strings
#Retorna : Devuelve todos los datos que han sido modificados segun el usuario y agrega los datos anteriores que no han sido modificados 
def reemplazar_cliente(cliente_nuevo):
    for indice, cliente in enumerate(lista_clientes):
        if cliente[0]==cliente_nuevo[0]:
            lista_clientes[indice]=cliente_nuevo
#Funcion para escribir clientes
#Parametros : base de datos de clientes + el ingreso de las modificaciones
#Retorna : Hace que escriba en la base de datos de clientes con los cambios 
def escribir_clientes_bd():
    target = open(clientes_filename, "w")
    target.truncate()
    clientes_str = ""
    for cliente in lista_clientes:
        cliente_str=cliente[0]+","+cliente[1]+","+cliente[2]+","+str(cliente[3])
        clientes_str=clientes_str+cliente_str+"\n"
    target.write(clientes_str)
    target.close()
#Funcion para retirar efectivo
#Parametros : monto/usuario string
#Retorna : segun el monto digitado por el usuario, la funcion rebaja del cajero el monto digitado por el usuario si este esta disponible 
def retirar_efectivo_cajero_bd(monto):
    cajero_bd=open(cajero_filename, "r")
    cajero_monto_lines= cajero_bd.readlines()
    cajero_monto_str= cajero_monto_lines[0]
    cajero_bd.close()
    if cajero_monto_str.isdigit():
        cajero_monto=int(cajero_monto_str)
        if cajero_monto>monto:
            cajero_monto = cajero_monto-monto
            cajero_bd= open(cajero_filename, "w")
            cajero_bd.truncate()
            cajero_bd.write(str(cajero_monto))
            return True
        else:
            return False
    else: 
        print "Archivo Invalido"
        return False
#Funcion para escribir transacciones 
#Parametros : usuario strings/cliente tipo de transaccion saldo anterior y monto
#Retorna : Devuelve toda la informacion de haora, fecha, cliente, tipo de transaccion, saldos y lo guarda en la base de datos de transacciones 
def escribir_transaccion(cliente, tipo_transaccion,saldo_anterior,monto):
    transaccionesbd=open(transacciones_filename, "a")
    ts = time.time()
    linea_transaccion = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d,%H:%M:%S")
    linea_transaccion= linea_transaccion+","+cliente[0]+","+tipo_transaccion+","+saldo_anterior+","+str(cliente[3])
    transaccionesbd.write(linea_transaccion+"\n")
#Estas funciones abren o leen las bases de datos 
clientes_filename = "clientes.bd"
clientesbd = open(clientes_filename, "r")
transacciones_filename = "transacciones.bd"
cajero_filename = "cajero.bd"
lista_clientes = []
menu=0
lineas_cliente = clientesbd.readlines()
nombre= ""
for estalinea in lineas_cliente:
    datos = estalinea.strip().split(",")
    cliente = (datos[0],datos[1],datos[2],int(datos[3]))
    lista_clientes.append(cliente)
#Menu principal con opciones fueron incluidas al finalizar cada opcion del usuario  
opciones = "**********************************\n\n\tMenu Principal\n\n**********************************\n1-Consultar el saldo\n2-Depositar efectivo\n3-Retiro de efectivo\n4-Transferencia\n5-Cambiar el pin\n6-Salir"

####################################################################

print "\n"
print "          Bienvenido\n"
print "*************.*********************"
print "CAJERO AUTOMATICO BANCO CENTRAL"
print "**********************************\n"
usuario_string = str(raw_input("Favor digite su usuario: "))
contrasena_string = str(raw_input("Favor digite su PIN: "))
#Funcion que valida lo digitado por el usuario y lo acepta o lo rechaza
cliente = devolver_cliente(usuario_string)
if cliente and cliente[1]==contrasena_string:
    nombre = cliente[2]
else:
    print "Usuario o contrasena incorrecta"
    sys.exit(0)
print "Hola "+ nombre
raw_input("Digite enter para continuar ")
os.system('clear')
#El menu es de 6 opciones si el usuario digita un numero mayor o letras le devolvera datos invalidos
print opciones
while menu <= 6:
    user_input = raw_input("Favor digite una de las opciones\n")
    if not user_input:
        print "Opcion no es valida"
    elif not user_input.isdigit():
        print "Opcion no es valida"
    else:
        menu =int(user_input)
        if menu ==1:
            #Utiliza funcion para que segun el usuario que ingreso devuelva su dato de saldo
            cliente = devolver_cliente(usuario_string)
            saldo = cliente[3]
            print "Su saldo es: "+ str(saldo)
            raw_input("Digite enter para continuar ")
            os.system('clear')
            print opciones
            menu
        elif menu ==2:
            #Utiliza la funcion de devolver cliente para ingresar el nuevo monto, mas la funcion de escribir en base de datos de clientes y transacciones 
            user_input=raw_input("Cual es el monto a depositar? ")
            if user_input.isdigit():
                monto = int(user_input)
                cliente = devolver_cliente(usuario_string)
                cliente_nuevo = (cliente[0], cliente[1], cliente[2], cliente[3]+monto) 
                reemplazar_cliente(cliente_nuevo)
                escribir_clientes_bd()
                print "Transaccion exitosa, su nuevo monto es: "+str(cliente_nuevo[3])
                escribir_transaccion(cliente_nuevo,"Deposito",str(cliente_nuevo[3]),str(monto))
            else:
                print "Monto invalido"
            raw_input("Digite enter para continuar ")
            os.system('clear')
            print opciones
            menu
        elif menu ==3:
            #Utiliza la funcion de devolver cliente para ingresar el nuevo monto, mas la funcion de escribir en base de datos de clientes y transacciones 
            cliente = devolver_cliente(usuario_string)
            disponible_cliente = cliente[3]
            print "Su disponible es: "+str(disponible_cliente)
            user_input = raw_input("Digite el monto y enter para continuar ")
            if user_input.isdigit():
                monto = int(user_input)
                if monto < disponible_cliente :
                    if retirar_efectivo_cajero_bd(monto):
                        cliente_nuevo = (cliente[0],cliente[1],cliente[2],disponible_cliente-monto)
                        reemplazar_cliente(cliente_nuevo)
                        escribir_clientes_bd()
                        print "Transaccion exitosa, su nuevo monto es: "+str(cliente_nuevo[3])
                        escribir_transaccion(cliente_nuevo, "Retiro",str(cliente[3]),str(monto))
                    else:
                        print "No hay efectivo en el cajero"
                else: 
                    print "No hay efectivo disponible"
            else:
                print "El monto especificado no es un numero"
            raw_input("Digite enter para continuar ")
            os.system('clear')
            print opciones
            menu
        elif menu ==4:
            #Utiliza la funcion de devolver cliente para revisar el saldo, utliza reemplazar cliente para realizar los cambios segun las transacciones, ademas la funcion de escribir en base de datos de clientes y transacciones 
            cliente = devolver_cliente(usuario_string)
            saldo_disponible = cliente[3]
            print "Su saldo disponible es: "+str(saldo_disponible)
            cliente_destino_string = raw_input("Digite el correo del usuario de destino: " )
            user_input = raw_input("Digite el monto que desea transferir: ")
            if user_input.isdigit():
                cliente_destino = devolver_cliente(cliente_destino_string)
                monto = int(user_input)
                if cliente_destino:
                    if saldo_disponible > monto:
                        cliente_destino_nuevo = (cliente_destino[0],cliente_destino[1],cliente_destino[2],cliente_destino[3]+monto)
                        cliente_nuevo = (cliente[0],cliente[1],cliente[2],cliente[3]-monto )
                        reemplazar_cliente(cliente_nuevo)
                        reemplazar_cliente(cliente_destino_nuevo)
                        escribir_clientes_bd()
                        print "Su nuevo saldo es: "+str(cliente_nuevo[3])
                        escribir_transaccion(cliente_nuevo, "Transaccion Saliente",str(cliente[3]),str(monto))
                        escribir_transaccion(cliente_destino_nuevo, "Transaccion Entrante",str(cliente_destino[3]),str(monto))
                    else:
                        print "No hay saldo disponible para la transferencia"
                else:
                    print "El cliente de destino no existe en el sistema"
            raw_input("Digite enter para continuar ")
            os.system('clear')
            print opciones
            menu
        elif menu ==5:
            #Utiliza la funcion de devolver cliente para ingresar la nueva contrasena, mas la funcion de escribir en base de datos de clientes para guardar cambios
            nueva_contrasena_string = raw_input("Favor digite su nuevo PIN: ")
            cliente = devolver_cliente(usuario_string)
            contrasena_nueva =str(nueva_contrasena_string)
            cliente_nuevo = (cliente[0], contrasena_nueva, cliente[2], cliente[3])
            reemplazar_cliente(cliente_nuevo)
            escribir_clientes_bd()
            print contrasena_nueva +" Es su nueva clave"
            raw_input("Digite enter para continuar ")
            os.system('clear')
            print opciones 
            menu 
        elif menu ==6:
            print "Gracias por utilizar los cajeros de Ciudad Gotica"
            break
        else:
            print "Opcion Incorrecta"
            menu