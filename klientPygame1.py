import socket
import pygame

pygame.init()
screen = pygame.display.set_mode((320, 240))
pygame.display.set_caption("Motorstyring")

#clock = pygame.time.Clock()

gameLoop = True

print("Kører klienten\n")

skt = socket.socket()

host = "192.168.1.249" # Ip-addressen for Raspberry Pi
port = 4200

skt.connect((host, port))

dataListe = ["Fister", "medister", "poelse", "dit", "lokum"]

while gameLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            data = "17"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            data = "18"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            data = "22"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            data = "23"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)
            skt.sendto(nyt_data, (host, port))
            
        if event.type == pygame.K_q and event.key == pygame.K_t:
            data = "24"
            nyt_data = data.encode("UTF-8")
            skt.sendall(nyt_data)
          
    pygame.display.flip()
skt.close()