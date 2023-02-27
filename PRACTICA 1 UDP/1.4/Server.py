# PRACTICA 1.4 SERVIDOR

from sys import argv
import socket
import pickle

# Mensajes reservados
# - wakeup: mensaje enviado por el cliente al inicio
# de la comunicacion para comprobar el estado del servidor
# - exit: mensaje enviado por el cliente para finalizar
# la comunicacion. Finaliza ambos scripts (servidor y cliente)
wakeup = "WAKEUP"
exit = "EXIT"

try:
    #Comprobacion de argumentos en la linea de comando
    if len(argv) < 3:
        print("Simple UDP Server")
        print("Usage: Server.py <IP> <PORT>")
    else:
        # Mapeo de esos argumentos a variables
        address = str(argv[1])
        port = int(argv[2])
        
        # Comprobacion numero de puerto
        if (port < 0) or (port > 65535):
            print("Port number must be between 0 and 65535")
        else:
            # Si todo ok, preparacion del socket para
            # arrancar el servidor
            server_address = (address,port)
            s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            s.bind(server_address)
            
            # Arranca el servidor
            print("UDP Server up and listening on " + str(address) + ":" + str(port))
            
            while True:
                #  Queda a la espera de conexiones de clientes
                bytes_rx = s.recvfrom(1024)
                
                # En caso de recibir un mensaje, se mapea este
                # en variables para su manipulacion
                client_id = pickle.loads(bytes_rx[0])[0]
                message = pickle.loads(bytes_rx[0])[1]
                address = bytes_rx[1]
                
                if (message == exit):
                    # En caso de recibir mensaje EXIT de finalizacion
                    print("Received EXIT Command from Client " + str(client_id) + " from " + str(address))
                    s.sendto(pickle.dumps("Bye Client " + str(client_id)),address)
                    break 
                elif (message == wakeup):
                    # El mensaje WAKEUP es usado por el cliente para
                    # comprobar el estado del servidor (vivo / muerto)
                    print("Received WAKEUP Command from Client " + str(client_id) + " from " + str(address))
                    s.sendto(pickle.dumps("Hello Client " + str(client_id)),address)    
                else:
                    # Tratamiento de los mensajes de usuario, en este
                    # caso solamente se ontiene y devuelve al cliente
                    # la longitud del mensaje
                    print("Message received from Client " + str(client_id) + " from " + str(address))
                    print("Number of characters in message: " + str(len(str(message))))
                    s.sendto(pickle.dumps("Received " + str(len(message)) + " characters."),address)
                    
            s.close()
            
except ValueError:
    # En caso de error de mapeo en el puerto
    print("Invalid port number")
except:
    # En caso de fallo, se entiende como fallo mas comun y el unico no
    # recogido una direccion IP cuyo formato sea incorrecto
    print("An error has occurred. Please check your input (malformed IP address?)")
        