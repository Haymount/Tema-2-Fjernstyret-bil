import time
import pygame
import socket

#DEn her kode har grafisk
#Her impotere vi 2 billeder (husk at tjekke om billedernes lokition er rigtige)
tar = pygame.image.load("Opgave/test socket/sjovTing.png") #billedet viser et rat
programIcon = pygame.image.load("Tema 2\Tema-2-Fjernstyret-bil/mette.jpg") #billedet er til iconet i hjørnet

WIDTH, HEIGHT = 900, 743 #Det er længden og højden på winduet som popper op når programet køre
#Her kommmer der et par farver
farve1 = (219, 112, 147) #palevioletred
farve2 = (0, 255, 0) #citron
farve3 = (0, 0, 0) #sort
farve4 = (0, 255, 128) #gørn ca.
skærmfarve = (255, 0, 0) #siger lidt sig selv, men det er baggrundsfarven på vores windue(farven står i RGB)

FPS = 60 #bestemmer maks fps. bare så det ikke ender med at lagge noget ud.
angle = 0 #viklen som billedet drejer med
batLiv = 5.2 #hvor meget strøm der er

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Her tegner vi selve skærmen 
pygame.display.set_caption("HasselHoff") #Det er navnet på programet

print("Kører klienten\n")#Bare for at teste om programmet køre

skt = socket.socket() #Forbinder til Rasp... Husk at tjekke om ip'en og porten er den rigtige
skt.settimeout(0.1)

host = "192.168.1.249" #Ip-addressen for Raspberry Pi
port = 4200 #og ja det her er porten
skt.connect((host, port)) #connecter til serveren med den ip og port oven over

def modbesked(): #Modtager 
    try:
        global batLiv
        mod = skt.recv(64)
        decMod = mod.decode("UTF-8")
        splitMod = decMod.split(",")
        intMod = float(splitMod[0])
        print(intMod)
        batLiv = intMod
        print("Received" + str(batLiv))
    except socket.error: #Burde printe det, hvis noget fucker det op oven over i stedet for et crash
        print("fuck")

def draw_windue(styr): #Alt det grafiske og navnet på porgamet
    pygame.display.set_icon(programIcon) #ændre det lille icon i hjørnet
    pygame.display.set_caption("HasselHoff") #Det er navnet på programet
    rotedede = pygame.transform.rotate(tar, angle) #Det her får billedet til at roterer
    WIN.fill(skærmfarve) #Det her er baggrundsfarven
    WIN.blit(rotedede, (styr.x, styr.y)) #Bare et billede af et rat 
    pygame.draw.rect(WIN, farve3, (-315, 723, 500, 20)) #Her tegner vi barrti lingen (ved sku ik om den virker endnu)
    pygame.draw.rect(WIN, farve2, (-315, 723, (batLiv*61), 20)) #udreningen for at få batteriet til at virke
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
            
                if keys[pygame.K_w] and keys[pygame.K_d]: #Det samme som koden nedenuder bare en anden retning
                    data = "1,100,60,"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    angle += 35
                elif keys[pygame.K_w] and keys[pygame.K_a]: #Burde at dreje imens den kører bagud
                    data = "1,40,100,"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    angle -= 35
                    
                elif keys[pygame.K_w]: #Fuldskrue frem ad
                    data = "1,100,100," #V sendes først også H muligvis den anden vej rundt
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

                elif keys[pygame.K_s] and keys[pygame.K_d]:
                    data = "0,100,60,"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    angle += 35
                elif keys[pygame.K_s] and keys[pygame.K_a]:
                    data = "0,40,100,"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    angle -= 35

                elif keys[pygame.K_s]: #Fuldstop ind til videre -tror jeg
                    data = "0,80,100,"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)

                elif keys[pygame.K_d]: #Her dreje til højre man gør
                    data = "1,100,0,"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    angle -= 50

                elif keys[pygame.K_a]: #Her burde den dreje til venstre
                    data = "1,0,100,"
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    angle += 50

                elif keys[pygame.K_ESCAPE]: #Lukker bare programmet
                    print("Du har stoppet spillet med Esc")
                    pygame.quit()

                else:
                    data = "0,0,0," #Her stopper bilen hvis vi ikke bruger nogle knapper
                    nyt_data = data.encode("UTF-8")
                    skt.sendall(nyt_data)
                    angle = 0
                    print("stop")
                    modbesked()
                    print("BatLiv " + str(batLiv))
        
        draw_windue(styr)
    pygame.quit()

if __name__ == "__main__":
    main()