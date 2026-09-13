"""
    Groupe 3
    Projet UFO catcher 
    Joelly Huin Sylvie Zhang Lisa Larive
    Le code se decompose en plusieure partie:
        => importation des modules/bibliothèques
        => Gestion du grove lcd 
        => Gestion du Joystick
        => importation des assets
        => boucle du jeu

"""
import pygame
import sys
import time
import random
import pygame.mixer
import sqlite3
import RPi.GPIO as GPIO
from grove.adc import ADC

connection = sqlite3.connect('UFO-Catcher.db')
cursor = connection.cursor()
 
# Drop tables 
#!cursor.execute("DROP TABLE IF EXISTS utilisateur;")
cursor.execute("DROP TABLE IF EXISTS peluche;")
cursor.execute("DROP TABLE IF EXISTS rare;")
cursor.execute("DROP TABLE IF EXISTS intermediaire;")

# Create the tables
command1 = """CREATE TABLE IF NOT EXISTS 
utilisateur(id_utilisateur INTEGER PRIMARY KEY, nom_utilisateur TEXT, 
password TEXT, score INTEGER, nbr_peluche INTEGER );"""
cursor.execute(command1)

command2 = """CREATE TABLE IF NOT EXISTS 
peluche(id_peluche INTEGER PRIMARY KEY, nom_peluche TEXT, rarete TEXT, 
FOREIGN KEY(rarete) REFERENCES rare(rarete));"""
cursor.execute(command2)

command3 = """CREATE TABLE IF NOT EXISTS rare(rarete TEXT PRIMARY KEY, point INTEGER);"""
cursor.execute(command3)

# Create the intermediary table
command4 = """CREATE TABLE IF NOT EXISTS 
intermediaire(id_utilisateur INTEGER, 
Sapicher BOOLEAN, Capybara BOOLEAN, Kirby BOOLEAN, 
Toby BOOLEAN, Etoile BOOLEAN, Mewo BOOLEAN, 
R2D2 BOOLEAN, Grogu BOOLEAN, Stich BOOLEAN, 
Freddy BOOLEAN, Rien BOOLEAN,
FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur));"""

cursor.execute(command4)

#? Insert data into the 'rare' table
command5 = """
INSERT INTO rare(rarete, point) VALUES('S', 1000), ('A', 500), ('B', 250), ('C', 100), ('R', 1);"""
cursor.execute(command5)

#? Insert data into the 'peluche' table
command6 = """
INSERT INTO peluche(id_peluche, nom_peluche, rarete) 
VALUES
(1, 'Sapicher', 'S'),
(2, 'Capybara', 'A'),
(3, 'Kirby', 'A'),
(4, 'Toby', 'B'),
(5, 'Etoile', 'B'),
(6, 'Mewo', 'B'),
(7, 'R2D2', 'C'),
(8, 'Grogu', 'C'),
(9, 'Stich', 'C'),
(10, 'Freddy', 'C'),
(11, 'Rien', 'R');
"""
cursor.execute(command6)
 
def add_new_user():
    while True:
        # Demander à l'utilisateur son nom d'utilisateur, son mot de passe et son adresse e-mail
        nom_utilisateur = str(input('Nom utilisateur : '))
        password = str(input('Mot de passe : '))

        # Vérifier si le nom d'utilisateur est déjà pris
        cursor.execute("SELECT * FROM utilisateur WHERE nom_utilisateur = ?", (nom_utilisateur,))
        if cursor.fetchone() is None:
            break
        print("Erreur : nom d'utilisateur déjà pris")

    # Récupérer l'ID utilisateur maximum
    cursor.execute("SELECT MAX(id_utilisateur) FROM utilisateur;")
    max_id = cursor.fetchone()[0]

    # Si la table est vide, commencer à partir de 0, sinon incrémenter
    if max_id is None:
        new_id = 0
    else:
        new_id = max_id + 1

    # Insérer le nouvel utilisateur avec un score de 0 et nbr_peluche de 0
    cursor.execute("INSERT INTO utilisateur(id_utilisateur, nom_utilisateur, password, score, nbr_peluche) VALUES (?, ?, ?, 0, 0)", (new_id, nom_utilisateur, password))

    # Insérer une nouvelle entrée pour l'utilisateur dans la table intermédiaire avec toutes les peluches définies sur False
    cursor.execute("INSERT INTO intermediaire(id_utilisateur, Sapicher, Capybara, Kirby, Toby, Etoile, Mewo, R2D2, Grogu, Stich, Freddy, Rien) VALUES (?, False, False, False, False, False, False, False, False, False, False, False)", (new_id,))

    # Valider les modifications
    connection.commit()
    return nom_utilisateur

def update_score(nom_utilisateur, id_peluche):
    # Récupérer l'ID de l'utilisateur
    cursor.execute("SELECT id_utilisateur FROM utilisateur WHERE nom_utilisateur = ?", (nom_utilisateur,))
    id_utilisateur = cursor.fetchone()[0]

    # Récupérer la rareté de la peluche attrapée
    cursor.execute("SELECT rarete FROM peluche WHERE id_peluche = ?", (id_peluche,))
    rarete = cursor.fetchone()[0]

    # Récupérer les points associés à la rareté
    cursor.execute("SELECT point FROM rare WHERE rarete = ?", (rarete,))
    point = cursor.fetchone()[0]

    # Mettre à jour le score de l'utilisateur
    cursor.execute("UPDATE utilisateur SET score = score + ? WHERE id_utilisateur = ?", (point, id_utilisateur))

    # Mettre à jour le nombre de peluches de l'utilisateur
    cursor.execute("UPDATE utilisateur SET nbr_peluche = nbr_peluche + 1 WHERE id_utilisateur = ?", (id_utilisateur,))

    # Récupérer le nom de la peluche attrapée
    cursor.execute("SELECT nom_peluche FROM peluche WHERE id_peluche = ?", (id_peluche,))
    nom_peluche = cursor.fetchone()[0]

    # Mettre à jour la table intermédiaire
    cursor.execute(f"UPDATE intermediaire SET {nom_peluche} = True WHERE id_utilisateur = ?", (id_utilisateur,))

    # Valider les modifications
    connection.commit()

def delete_user():
    # Ask the user for their username
    nom_utilisateur = str(input('Entrez votre nom d\'utilisateur : '))

    # Ask the user if they want to delete their account
    confirmation = str(input('Voulez-vous supprimer votre compte ? Si oui, tapez "oui". Sinon, tapez "Non". '))

    if confirmation.lower() == 'oui':
        # Get the user's id
        cursor.execute("SELECT id_utilisateur FROM utilisateur WHERE nom_utilisateur = ?", (nom_utilisateur,))
        id_utilisateur = cursor.fetchone()[0]

        if id_utilisateur is not None:
            # Delete the user from the 'utilisateur' table
            cursor.execute("DELETE FROM utilisateur WHERE id_utilisateur = ?", (id_utilisateur,))

            # Delete the user's entries from the 'intermediaire' table
            cursor.execute("DELETE FROM intermediaire WHERE id_utilisateur = ?", (id_utilisateur,))

            # Commit the changes
            connection.commit()

            print("Votre compte a été supprimé avec succès.")
        else:
            print("Aucun utilisateur trouvé avec ce nom.")
    else:
        print("Suppression de compte annulée.")

def login():
    while True:
        # Demander à l'utilisateur son nom d'utilisateur et son mot de passe
        nom_utilisateur = str(input('Nom utilisateur : '))
        password = str(input('Mot de passe : '))

        # Vérifier si le nom d'utilisateur existe dans la base de données
        cursor.execute("SELECT * FROM utilisateur WHERE nom_utilisateur = ?", (nom_utilisateur,))
        user = cursor.fetchone()

        if user is not None:
            # Si le nom d'utilisateur existe, vérifier le mot de passe
            if user[2] == password:
                print("Connexion réussie!")
                return nom_utilisateur
            else:
                print("Mot de passe incorrect")
        else:
            print("Nom d'utilisateur incorrect")

def start():
    # Demander à l'utilisateur s'il veut se connecter ou créer un compte
    choice = str(input('Voulez-vous vous connecter ou créer un compte? Tapez "connecter" ou "creer": '))

    if choice.lower() == 'connecter':
        # Si l'utilisateur veut se connecter, appeler la fonction login
        return login()
    elif choice.lower() == 'creer':
        # Si l'utilisateur veut créer un compte, appeler la fonction add_new_user
        return add_new_user()
    else:
        print("Choix non valide. Veuillez taper 'connecter' ou 'creer'.")
        return None

def logout():
    # Réinitialiser le nom d'utilisateur à None pour indiquer que l'utilisateur est déconnecté
    nom_utilisateur = None
    print("Vous avez été déconnecté.")
    return nom_utilisateur

def classement():
    # Récupérer tous les utilisateurs en ordre décroissant de leur score
    cursor.execute("SELECT nom_utilisateur, score, nbr_peluche FROM utilisateur ORDER BY score DESC")
    users = cursor.fetchall()

    # Afficher le classement
    print("Classement des utilisateurs par score :")
    for i, user in enumerate(users, start=1):
        nom_utilisateur, score, nbr_peluche = user
        print(f"{i}. {nom_utilisateur} - Score : {score}, Peluches attrapées : {nbr_peluche}")

if sys.platform == "uwp":
    import winrt_smbus as smbus

    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO

    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3E


# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r, g, b):
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0, 0)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 1, 0)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0x08, 0xAA)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 4, r)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 3, g)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 2, b)


# send command to display (no need for external use)
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x80, cmd)


# set display text \n for second line(or auto wrap)
def setText(text):
    textCommand(0x01)  # clear display
    time.sleep(0.05)
    textCommand(0x08 | 0x04)  # display on, no cursor
    textCommand(0x28)  # 2 lines
    time.sleep(0.05)
    count = 0
    row = 0
    for c in text:
        if c == "\n" or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xC0)
            if c == "\n":
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x40, ord(c))


# Update the display without erasing the display
def setText_norefresh(text):
    textCommand(0x02)  # return home
    time.sleep(0.05)
    textCommand(0x08 | 0x04)  # display on, no cursor
    textCommand(0x28)  # 2 lines
    time.sleep(0.05)
    count = 0
    row = 0
    while len(text) < 32:  # clears the rest of the screen
        text += " "
    for c in text:
        if c == "\n" or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xC0)
            if c == "\n":
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x40, ord(c))


def affichage(r, g, b, peluche, pts):
    setRGB(r, g, b)
    espace_peluche = (16 - len(peluche)) // 2
    texte_peluche = espace_peluche * " " + peluche
    espace_pts = (16 - len(pts)) // 2
    texte_pts = espace_pts * " " + pts
    for i in range(2):
        setText("  Tu as obtenu\n" + texte_peluche)
        time.sleep(2)
        setText("  Tu as obtenu\n" + texte_pts)
        time.sleep(2)


class GroveThumbJoystick:
    def __init__(self, channelX, channelY):
        self.channelX = channelX
        self.channelY = channelY
        self.adc = ADC()

    @property
    def value(self):
        return self.adc.read(self.channelX), self.adc.read(self.channelY)


Grove = GroveThumbJoystick



# Initialisation de Pygame
pygame.init()

# Initialisation du mixer
pygame.mixer.init()

# Initialisation de la surface
surface = pygame.display.set_mode((900, 700), pygame.RESIZABLE)

# Chargement des images
box = pygame.image.load(r"./game/images/box.png")
# I => 38%
image1 = pygame.image.load(
    r"./game/images/pince_initiale.png"
)
# S => 1%
sapicher = pygame.image.load(
    r"./game/images/sapicher.png"
)
# A => 3%
capybara = pygame.image.load(
    r"./game/images/Capybara.png"
)
kirby = pygame.image.load(r"./game/images/kirby.png")
# B => 5%
toby = pygame.image.load(r"./game/images/toby.png")
mewo = pygame.image.load(r"./game/images/mewo.png")
etoile = pygame.image.load(r"./game/images/etoile.png")
# C => 10%
stitch = pygame.image.load(r"./game/images/stich.png")
r2d2 = pygame.image.load(r"./game/images/r2d2.png")
freddy = pygame.image.load(r"./game/images/freddy.png")
grogu = pygame.image.load(r"./game/images/grogu.png")


# Chargement de la musique

musique_sapicher = pygame.mixer.Sound(
    r"./game/Musiques/Musique_sapicher.mp3"
)

musique_capybara = pygame.mixer.Sound(
    r"./game/Musiques/Musique_capybara.mp3"
)
musique_kirby = pygame.mixer.Sound(
    r"./game/Musiques/Musique_kirby.mp3"
)

musique_toby = pygame.mixer.Sound(
    r"./game/Musiques/Musique_toby.mp3"
)
musique_mewo = pygame.mixer.Sound(
    r"./game/Musiques/Musique_Mewo.mp3"
)
musique_etoile = pygame.mixer.Sound(
    r"./game/Musiques/Musique_etoile.mp3"
)

musique_stitch = pygame.mixer.Sound(
    r"./game/Musiques/Musique_stitch.mp3"
)
musique_r2d2 = pygame.mixer.Sound(
    r"./game/Musiques/Musique_r2d2.mp3"
)
musique_freddy = pygame.mixer.Sound(
    r"./game/Musiques/Musique_Freddy.mp3"
)
musique_grogu = pygame.mixer.Sound(
    r"./game/Musiques/Musique_grogu.mp3"
)
musique_rien = pygame.mixer.Sound(
    r"./game/Musiques/Musique_rien.mp3"
)



# Redimensionnement des images
box = pygame.transform.scale(
    box, (704.4, 704.4)
)  # Remplacez par les dimensions souhaitées

# Initialisation des coordonnées de l'image
x = 400
y = -60

# Initialisation de la vitesse de déplacement
speed = 5
compteur = 0

# Initialisation des variables de mouvement
move_left = move_right = False

# Poucentage de chance d'obtenir les éléments
elements = [
    (11, image1, "rien", musique_rien, 12, 48, 125, "1 PTS"),
    (1, sapicher, "WOAW Sapicher", musique_sapicher, 0, 0, 0, "1000 PTS"),
    (2, capybara, "capybara", musique_capybara, 240, 128, 128, "500 PTS"),
    (3, kirby, "kirby", musique_kirby, 240, 128, 128, "500 PTS"),
    (4, toby, "un chien ?!", musique_toby, 175, 101, 203, "250 PTS"),
    (6, mewo, "mewo", musique_mewo, 175, 101, 203, "250 PTS"),
    (5, etoile, "etoile", musique_etoile, 175, 101, 203, "250 PTS"),
    (9, stitch, "stitch", musique_stitch, 87, 207, 181, "100 PTS"),
    (10,freddy, "freddy", musique_freddy, 87, 207, 181, "100 PTS"),
    (7, r2d2, "r2d2", musique_r2d2, 87, 207, 181, "100 PTS"),
    (8, grogu, "grogu", musique_grogu, 87, 207, 181, "100 PTS"),
]
poids = [38, 1, 3, 3, 5, 5, 5, 10, 10, 10, 10]

# Initialisation de la police
font = pygame.font.Font(None, 36)

# Initialisation des couleurs
couleur_rectangle = (255, 255, 255)  # Blanc
couleur_texte = (255, 105, 180)  # Rose
down = 0


# Boucle principale
# Appeler la fonction start pour commencer
nom_utilisateur = start()
print(nom_utilisateur)
#!LANCEMENT

while True:
    sensor = GroveThumbJoystick(int(0), int(0 + 1))
    joystick_x, joystick_y = sensor.value

    button_pressed = False
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Gestion des événements
    if GPIO.input(22):
        if not button_pressed:
            button_pressed = True
            while y < 150:
                y += speed
                surface.fill((0, 0, 0))
                surface.blit(image1, (x, y))
                surface.blit(box, (100, 0))  # Ajout de l'image box
                pygame.display.flip()
                pygame.time.wait(10)
            time.sleep(3)
            id_peluche , image_choisie, nom, musique, r, g, b, points = random.choices(
                elements, weights=poids, k=1
            )[0]

            musique.play()
            update_score(nom_utilisateur, id_peluche)
            while y > -80:
                y -= speed
                surface.fill((0, 0, 0))
                surface.blit(image_choisie, (x, y))
                surface.blit(box, (100, 0))  # Ajout de l'image box
                pygame.display.flip()
                pygame.time.wait(5)
            time.sleep(1)
            pygame.display.flip()
            affichage(r, g, b, nom, points)
            setText("                  \n                  ")


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if joystick_y < 372:
        if x > 277:
            x -= speed
    if joystick_y > 626:
        if x < -57 + box.get_width() - image1.get_width():
            x += speed
    if button_pressed:
        button_pressed = False
    # time.sleep(0.25)

    # Effacement de la surface
    surface.fill((0, 0, 0))

    # Affichage de l'image
    surface.blit(image1, (x, -60))
    surface.blit(box, (100, 0))  # Ajout de l'image box

    # Mise à jour de l'affichage
    pygame.display.flip()


connection.commit()
connection.close()