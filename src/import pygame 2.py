import pygame
import sys
import time
import random                               

# Initialisation de Pygame
pygame.init()

# Initialisation de la surface
surface = pygame.display.set_mode((900, 700), pygame.RESIZABLE)

# Chargement des images
box = pygame.image.load(r"C:\Users\lisa2\OneDrive\Documents\Sorbonne\S1\info\Projet\images\box.png")
image1 = pygame.image.load(r"C:\Users\lisa2\OneDrive\Documents\Sorbonne\S1\info\Projet\images\pince_initiale.png")
taylor = pygame.image.load(r"C:\Users\lisa2\OneDrive\Documents\Sorbonne\S1\info\Projet\images\2023_11_09_0jb_Kleki.png") 
ariana = pygame.image.load(r"C:\Users\lisa2\Downloads\ariana.webp")
freddy = pygame.image.load(r"C:\Users\lisa2\OneDrive\Documents\Sorbonne\S1\info\Projet\images\freddy.png")  

# Redimensionnement des images
box = pygame.transform.scale(box, (704.4, 704.4))  # Remplacez par les dimensions souhaitées
#taylor = pygame.transform.scale(image1, (200,400)) 

# Initialisation des coordonnées de l'image
x = 400
y = -60

# Initialisation de la vitesse de déplacement
speed = 5

# Initialisation des variables de mouvement
move_left = move_right = False

#Poucentage de chance d'obtenir les éléments
elements = [(taylor, "taylor"), (ariana, "ariana"), (freddy, "freddy")]
poids = [5, 5, 90]
                                                          
# Initialisation de la police
font = pygame.font.Font(None, 36)

# Initialisation des couleurs
couleur_rectangle = (255, 255, 255) # Blanc
couleur_texte = (255, 105, 180) # Rose

# Boucle principale
while True:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True

            elif event.key == pygame.K_SPACE:
                while y < 150:
                    y += speed
                    surface.fill((0, 0, 0))
                    surface.blit(image1, (x, y))
                    surface.blit(box, (100, 0))  # Ajout de l'image box
                    pygame.display.flip()
                    pygame.time.wait(10)
                time.sleep(3)
                image_choisie, nom = random.choices(elements, weights=poids, k=1)[0]
                print(image_choisie, nom)
                surface.blit(image_choisie, (x, y))  # Affichage de la deuxième image
                pygame.display.flip()

                while y > -80:
                    y -= speed
                    surface.fill((0, 0, 0))
                    surface.blit(image_choisie, (x, y))
                    surface.blit(box, (100, 0))  # Ajout de l'mage box
                    pygame.display.flip()
                    pygame.time.wait(10)
                time.sleep(1)
                text = font.render("Bravo, tu as obtenu " + nom + " !", True, couleur_texte)
                text_rect = text.get_rect(center=(x+50, 150+50))  # Centrer le texte dans le rectangle
                pygame.draw.rect(surface, couleur_rectangle, (x/2, 150, 500, 100))  # Dessiner le rectangle
                surface.blit(text, text_rect)  # Afficher le texte dans le rectangle
                pygame.display.flip()
                time.sleep(1)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False

    if move_left and x > 180:  # Modification de la limite gauche
        x -= speed
    if move_right and x < 30 + box.get_width() - image1.get_width():  # Modification de la limite droite
        x += speed

    # Effacement de la surface
    surface.fill((0, 0, 0))

    # Affichage de l'image
    surface.blit(image1, (x, -60))
    surface.blit(box, (100, 0))  # Ajout de l'image box

    # Mise à jour de l'affichage
    pygame.display.flip()
