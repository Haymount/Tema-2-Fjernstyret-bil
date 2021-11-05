import time
import pygame
import socket

tar = pygame.image.load("Opgave/test socket/sjovTing.png") #Sejt sådan impoterer man et billede

#Det er længden og højden på winduet som popper op når programet køre
WIDTH, HEIGHT = 900, 743

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Motorstyring") #Det er navnet på programet

#siger lidt sig selv, men det er baggrundsfarven på vores windue(farven står i RGB)
skærmfarve = (0, 255, 185)

print("Kører klienten\n")
print("5\n")

FPS = 60 #bestemmer maks fps. bare så det ikke ender med at lagge noget ud.

skt = socket.socket() #Forbinder til Rasp... Husk at tjekke om ip'en og porten er den rigtige

host = "192.168.1.249" #Ip-addressen for Raspberry Pi
port = 4200

skt.connect((host, port))

def draw_windue(styr): #Her er noget styring til skærmen
    WIN.fill(skærmfarve) #Det her er baggrundsfarven
    WIN.blit(tar, (styr.x, styr.y)) #Bare et billede af et rat 
    pygame.display.update()

def main(): #Det vigtige kode er her
    styr = pygame.Rect(0, 0, 507, 676)

    clock = pygame.time.Clock()
    gameLoop = True
    while gameLoop:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed() #Den her siger hvad der skal gøres, finds forskellige taster bliver trykket på
                if keys[pygame.K_w]: #Fuldskrue frem ad -tror jeg
                    data = "100,100"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

                elif keys[pygame.K_q]: #Hvis vi skal have blink lys eller bare bruge q og e til noget
                    data = "lysV"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                elif keys[pygame.K_e]:
                    data = "lysH"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

                elif keys[pygame.K_a]: #Her burde den dreje til venstre
                    data = "0,100"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                elif keys[pygame.K_w and pygame.K_a]:
                    data = "80,100"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

                elif keys[pygame.K_s]: #Fuldstop ind til videre -tror jeg
                    data = "0,0"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

                elif keys[pygame.K_d]: #Her dreje til højre man gør
                    data = "100,0"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                elif keys[pygame.K_w and pygame.K_d]:
                    data = "100,80"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

        draw_windue(styr)
    pygame.quit()


if __name__ == "__main__":
    main()