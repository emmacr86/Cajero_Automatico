import os

lista_clientes=[]
#Esta funcion es para leer la base datos de clientes 
clientes_filename = "clientes.bd"
clientesbd = open(clientes_filename, "r")
#Esta funcion es para leer la base datos de transacciones 
transacciones_filename = "transacciones.bd"
transaccionesbd = open(transacciones_filename, "r")
#Esta funcion es para leer la base datos del cajero
cajero_filename = "cajero.bd"
cajerobd = open(cajero_filename, "r")
#El menu principal esta guardado en una variable para simplificar el codigo 
menu=0
opciones = "*******************************\n\n\tMenu Principal\n\n*******************************\n1-Crear usuario nuevo\n2-Reporte de de usuarios y montos de cuentas\n3-Reporte de transacciones\n4-Cargar efectivo al cajero\n5-Salir"
####################################################################

print "\n"
print "          Bienvenido\n"
print "*******************************"
print "SISTEMA ADMINISTRADOR DE CAJERO"
print "*******************************\n"
print opciones
#Las opciones son 5 si el administrador digita un numero mayor o letras le va a devolver mensaje y lo devuelve al menu principal
while menu <= 5:
    user_input = raw_input("Favor digite una de las opciones\n")
    if not user_input:
        print "Opcion no es valida"
    elif not user_input.isdigit():
        print "Opcion no es valida"
    else:
        menu =int(user_input)
        if menu ==1:
            #En esta opcion guarda todos los inputs en variables para luego agregarlas a la base de datos 
            correo=raw_input("Cual es el correo del nuevo usuario? ")
            contrasena=raw_input("Cual es el contrasena desea asignar? ")
            usuario=raw_input("Cual es el nombre del nuevo usuario? ")
            monto=raw_input("Cual es el monto con el que abre la cuenta? ")
            nuevo_usuario=correo.strip(),contrasena.strip(),usuario.strip(),monto.strip()
            target = open(clientes_filename, "a")
            target.write(str(nuevo_usuario))
            target.close()
            raw_input("Digite enter para continuar ")
            os.system('clear')
            print opciones
            menu
        elif menu ==2:
            #Con esta funcion se logra observar cada usuario junto con su repectivo saldo 
            for estaLinea in clientesbd:
                valores = estaLinea.strip().split(",")
                nombre = str(valores[2])
                saldo= int(valores[3])
                print "EL cliente %s tiene un monto disponible de: %d" % (nombre, saldo)
            raw_input("Digite enter para continuar ")
            os.system('clear')
            print opciones
            menu
        elif menu ==3:
            #Esta funcion abre la base de datos de las transacciones para revisar todo el historial
            print "Reporte de transacciones"
            for estalinea in transaccionesbd:
                valores = estalinea.strip().split(",")
                fecha = str(valores[0])
                hora = str(valores[1])
                correo = str(valores[2])
                tipo_transaccion = str(valores[3])
                saldo_anterior = int(valores[4])
                nuevo_saldo = str(valores[5])
                print "La fecha %s en la hora %s el usuario con el correo %s realizo %s el saldo anterior era: %d y el saldo actual es: %r "%(fecha, hora, correo, tipo_transaccion, saldo_anterior, nuevo_saldo)
            raw_input("Digite enter para continuar ")
            os.system('clear')
            print opciones
            menu
        elif menu ==4:
            #Esta opcion permite agregar mas dinero al cajero, primero se digita el monto, luego se abre la base de datos del cajero, suma el monto, guarda el nuevo monto y cierra la base de datos 
            user_input=int(input("Cual es el monto a cargar en el cajero? "))
            for estalinea in cajerobd:
                valores = estalinea.strip().split(",")
                monto_anterior = int(valores[0])
                monto_nuevo =str(int(valores[0])+int(user_input)) 
                target = open(cajero_filename, "w")
                target.truncate()
                str(target.write(monto_nuevo))
                target.close()
            print "Transaccion exitosa, el cajero tiene disponible: "+monto_nuevo
            raw_input("Digite enter para continuar ")
            os.system('clear')
            print opciones
            menu
        elif menu ==5:
            print "Lo esperamos pronto administrador!"
            break
        else:
            print "Opcion Incorrecta"
            menu