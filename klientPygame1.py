import socket
import pygame

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
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            data = "lysV"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            data = "100,75"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            data = "lysH"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            data = "23"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            data = "24"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:    
            data = "100,80"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)        
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            data = "0,0"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            data = "80,100"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)

    pygame.display.flip()
skt.close()