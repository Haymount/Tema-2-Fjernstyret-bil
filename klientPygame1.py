import socket
import pygame

#Koden her har ikke noget grafisk, bare så det ikke fucker op

pygame.init()
screen = pygame.display.set_mode((320, 240))
pygame.display.set_caption("Motorstyring")

gameLoop = True

print("Kører klienten\n")

skt = socket.socket()

host = "192.168.1.249" #Ip-addressen for Raspberry Pi
port = 4200

skt.connect((host, port))

while gameLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed() #Den her siger hvad der skal gøres, finds forskellige taster bliver trykket på
    
                if keys[pygame.K_w] and keys[pygame.K_d]: 
                    data = "1,100,60"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    
                elif keys[pygame.K_w] and keys[pygame.K_a]:
                    data = "1,80,100"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    
                elif keys[pygame.K_w]: #Fuldskrue frem ad
                    data = "1,100,75" #V sendes først også H muligvis den anden vej rundt
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

                elif keys[pygame.K_a]: #Her burde den dreje til venstre
                    data = "1,0,100"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    
                elif keys[pygame.K_s]: #Fuldstop ind til videre -tror jeg
                    data = "0,100,55"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

                elif keys[pygame.K_d]: #Her dreje til højre man gør
                    data = "1,100,0"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

                else:
                    data = "0,0,0" #Her stopper bilen hvis vi ikke bruger nogle knapper
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

pygame.display.flip()
skt.close()