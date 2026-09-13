
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#import / Setup

from flask import Flask, render_template, request, url_for,session
import sqlite3
app = Flask(__name__)
# Connect to the database

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#queries
utilisateur_global = None
@app.route("/")
def pagecouverture():
    return render_template('pagecouverture.html')

@app.route("/connexion", methods=['POST','GET'])

def valider():
    global utilisateur_global
    if request.method == 'POST':
        print("oui")
        connection = sqlite3.connect("UFO-Catcher.db")
        cursor = connection.cursor()
        name = request.form.get('nom_utilisateur', '')
        password = request.form.get('password','')
        connexion = "SELECT nom_utilisateur,password FROM utilisateur WHERE nom_utilisateur = '"+name+"' and password='"+password+"'"
        cursor.execute(connexion)
        results_co = cursor.fetchall()

        if len(results_co) == 0:
            print("Mot de passe ou pseudo est invalide")
        else:
            utilisateur_global = name
            return render_template('accueil.html')
        
        

    return render_template('valider.html')
@app.route("/accueil",methods=['POST','GET'])
def accueil():
    return render_template('accueil.html')


@app.route("/profil",methods=['POST','GET'])
def profil():
    connection = sqlite3.connect("UFO-Catcher.db")
    cursor = connection.cursor()
    score = "SELECT score FROM utilisateur WHERE nom_utilisateur = '"+utilisateur_global+"'"    
    cursor.execute(score)
    results_score = cursor.fetchall()
    score_user = results_score[0][0]
    nbpeluche = "SELECT nbr_peluche FROM utilisateur WHERE nom_utilisateur = '"+utilisateur_global+"'"
    cursor.execute(nbpeluche)
    peluche = cursor.fetchall()
    peluche_user = peluche[0][0]

    return render_template('compte.html',user = utilisateur_global, point = score_user, peluches =peluche_user)

@app.route('/regle',methods=['POST','GET'])
def regle():
    return render_template('regle.html')

@app.route('/leaderboard',methods=['POST','GET'])
def leaderboard():
    return render_template('Leardboard.html')

@app.route('/galerie',methods=['POST', 'GET'])
def galerie():
    return render_template('galerie.html')

@app.route('/commentjouer',methods=['POST', 'GET'])
def commentjouer():
    return render_template('CommentJouer.html')

'''

    #connection = sqlite3.connect("UFO-Catcher.db")
    #cursor = connection.cursor()
    

    name = request.form['nom_utilisateur']
    password = request.form['password']

    print(name, password)
    score = "SELECT score FROM utilisateur WHERE nom_utilisateur = '"+name+"'"
    cursor.execute(score)
    results_score = cursor.fetchall()
    score_user = results_score[0][0]
    
    print(results_score)
    

    #connexion = "SELECT nom_utilisateur,password FROM utilisateur WHERE nom_utilisateur = '"+name+"' and password='"+password+"'"
    #cursor.execute(connexion)
    #results_co = cursor.fetchall()
    #print(results_co)

    if len(name) == 0:
        print("Mot de passe ou pseudo est invalide")
    else:
        return render_template('accueil.html')
'''

#,username = name, results_score = score_user