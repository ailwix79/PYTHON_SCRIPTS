# PRACTICA 1.4 CLIENTE

from sys import argv
import socket
import pickle
import time

# Mensajes reservados
# - wakeup: mensaje enviado por el cliente al inicio
# de la comunicacion para comprobar el estado del servidor
# - exit: mensaje enviado por el cliente para finalizar
# la comunicacion. Finaliza ambos scripts (servidor y cliente)
wakeup = "WAKEUP"
exit = "EXIT"

# Parametros para el control de intentos de conexion
# -err_count: numero de intentos de conexion fallidos
# -err_tolerance: maximo numero de intentos fallidos,
# al darse este numero de intentos el cliente desiste.
err_count = 0
err_tolerance = 10

try:
    #Comprobacion de argumentos en la linea de comando
    if len(argv) < 4:
        print("Simple UDP Client")
        print("Usage: Client.py <IP> <PORT> <CLIENT_ID>")
    else:
        # Mapeo de esos argumentos a variables
        address = str(argv[1])
        port = int(argv[2])
        client_id = str(argv[3])
        
        # Comprobacion numero de puerto
        if (port < 0) or (port > 65535):
            print("Port number must be between 0 and 65535")
        else:
            # Si todo ok, se configura el socket del cliente
            # La libreria socket escogera un puerto libre
            server_address = (address,port)
            s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

            while True:
                try:
                    # Se prepara y envia mensaje WAKEUP
                    bytes_tx = pickle.dumps((client_id,wakeup))
                    s.sendto(bytes_tx,server_address)
                    
                    # Se queda a la espera de recibir respuesta del servidor
                    bytes_rx = s.recvfrom(1024)
                    
                    # En caso de recepcion, se muestra en pantalla
                    print("Messsage received from Server: " + str(bytes_rx[1]))
                    print("Message: " + pickle.loads(bytes_rx[0]))
                
                    # Una vez comprobada la conexion, se cede el control al usuario
                    while True:
                        # Se pide, prepara y envia el mensaje del usuario al servidor
                        msg = str(input("Message> "))
                        packet = pickle.dumps((client_id,msg))
                        s.sendto(packet,server_address)

                        # Se queda a la espera de recibir respuesta del servidor
                        bytes_rx = s.recvfrom(1024)
                        
                        # En caso de recepcion, se muestra en pantalla
                        print("Messsage received from Server: " + str(bytes_rx[1]))
                        print("Message: " + pickle.loads(bytes_rx[0]))
                        
                        # Si el cliente decide terminar, solo tiene que romper el bucle
                        # de interaccion con el servidor y ejecutar socket.close()
                        if msg == exit: 
                            break
                    
                    # Finaliza comunicacion del cliente
                    s.close()
                    break

                except ConnectionResetError:
                    # En caso de no conexion, se espera un segundo hasta volverlo a intentar
                    print("Server not responding. Attempting to send WAKEUP message again...")
                    err_count += 1

                    if (err_count >= err_tolerance):
                        # Si no quedan mas intentos, finaliza el programa
                        print("Connection failed.")
                        s.close()
                        break
                    else:
                        # Si no se ha llegado al limite de intentos, se
                        # vuelve a intentar la comunicacion
                        time.sleep(1)
                        continue
            
except ValueError:
    # En caso de error de mapeo en el puerto
    print("Invalid port number")
except:
    # En caso de fallo, se entiende como fallo mas comun y el unico no
    # recogido una direccion IP cuyo formato sea incorrecto
    print("An error has occurred. Please check your input (malformed IP address?)")
    
    