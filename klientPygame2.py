import time
import pygame
import socket

tar = pygame.image.load("Opgave/test socket/sjovTing.png") #Sejt sådan impoterer man et billede
angle = 0 #viklen som billedet drejer med

#Det er længden og højden på winduet som popper op når programet køre
WIDTH, HEIGHT = 900, 743
#Her er et par faver til batteri baren
farve1 = (219, 112, 147) #palevioletred
farve2 = (255, 255, 0) #gul
farve3 = (0, 0, 0) #sort
farve4 = (0, 255, 128) #gørn ca.

batLiv = 5.2 #hvor meget strøm der er

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Her tegner vi selve skærmen 
pygame.display.set_caption("Motorstyring") #Det er navnet på programet

#siger lidt sig selv, men det er baggrundsfarven på vores windue(farven står i RGB)
skærmfarve = (0, 255, 185)

print("Kører klienten\n")

FPS = 60 #bestemmer maks fps. bare så det ikke ender med at lagge noget ud.

skt = socket.socket() #Forbinder til Rasp... Husk at tjekke om ip'en og porten er den rigtige

host = "192.168.1.249" #Ip-addressen for Raspberry Pi
port = 4200 #og ja det her er porten

skt.connect((host, port))

#print("Værten med " + str(skt.accept[0]) + " har etableret forbindelse.")
#encodBatLiv = skt.accept.recv(64)
#batLiv = encodBatLiv.decode("UTF-8")

def draw_windue(styr): #Her er noget styring til skærmen
    rotedede = pygame.transform.rotate(tar, angle) #Det her får billedet til at roterer
    WIN.fill(skærmfarve) #Det her er baggrundsfarven
    WIN.blit(rotedede, (styr.x, styr.y)) #Bare et billede af et rat 
    pygame.draw.rect(WIN, farve2, (-315, 723, 500, 20)) #Her tegner vi barrti lingen (ved sku ik om den virker endnu)
    pygame.draw.rect(WIN, farve3, (-315, 723, (batLiv*61), 20))
    pygame.display.update()

def main(): #Det vigtige kode er her
    styr = pygame.Rect(195, 0, 507, 676)

    clock = pygame.time.Clock()
    gameLoop = True
    while gameLoop:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed() #Den her siger hvad der skal gøres, finds forskellige taster bliver trykket på
                global angle

                if keys[pygame.K_w] and keys[pygame.K_d]: 
                    data = "1,100,60,"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    angle += 35
                elif keys[pygame.K_w] and keys[pygame.K_a]:
                    data = "1,60,100,"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    angle -= 35
                    #
                elif keys[pygame.K_w]: #Fuldskrue frem ad
                    data = "1,80,100," #V sendes først også H muligvis den anden vej rundt
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    angle = 0

                elif keys[pygame.K_a]: #Her burde den dreje til venstre
                    data = "1,0,100,"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    angle += 50
                    
                elif keys[pygame.K_s]: #Fuldstop ind til videre -tror jeg
                    data = "0,100,55,"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

                elif keys[pygame.K_d]: #Her dreje til højre man gør
                    data = "1,100,0,"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    angle -= 50

                else:
                    data = "0,0,0," #Her stopper bilen hvis vi ikke bruger nogle knapper
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

        draw_windue(styr)
    pygame.quit()

if __name__ == "__main__":
    main()