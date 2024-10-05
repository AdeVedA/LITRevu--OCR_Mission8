# <p align="center"><bold>LITRevu - OCR_Mission[8]</bold></p>
<p align="center">=========================================================================</p>
<p align="center">
  <br/>
  <picture> 
    <img alt="logo de LITRevu" src="weblog/static/images/LITrevu.png" width="300">
  </picture>
  <br/>
  <br/>
</p>

### <p align="center">- Application Web de critique littéraire -</p>

# <p align="center"> I. Description du Projet</p>

Cette application Web de type "revue littéraire" permet aux abonnés de LITRevu de : 
- publier sur le site des demandes de critiques (billets)
- des critiques en réponse à ces demandes
- de publier les deux en un seul formulaire (une critique autonome avec billet intégré)
- de parcourir ses propres publications et de les modifier ou de les supprimer
- de s'abonner aux publications d'autres utilisateurs
- de se désabonner d'un utilisateur ou d'en bloquer un
- de visualiser le flux des publications (siennes ou d'utilisateurs suivis) par ordre antéchronologique

Les **"billets"** ont un *titre* et une *description* et peuvent être assortis d'une *image* (à défaut, une image de livre à couverture vierge en prendra la place)

Les **"critiques"** ont un *titre*, une *évaluation* (de 0 à 5 étoiles) et un *commentaire*.

Billets et critiques sont, lors de leur publication, automatiquement *datés* et *"signés"* par l'utilisateur.

Une **page d'accueil** *visiteur* permet d'accéder à la page d'inscription ou de se connecter avec son nom d'utilisateur et son mot de passe.

Une **page d'inscription** permet au visiteur d'inscrire son nom d'utilisateur, son email et son mot de passe (double champ de formulaire pour vérification) et des messages l'informent en temps réel de la validité de chaque champ.

Une fois **authentifié**, l'utilisateur à accès par boutons à 4 pages principales de navigation :

- le **Flux**, lui permettant de visualiser par ordre antéchronologique toute publication (sienne ou d'utilisateurs suivis), de publier un billet ou une critique autonome (incluant le billet) ou de répondre par critique aux billets des utilisateurs suivis
- les **Posts**, lui permettant de visualiser ses propres publications et de les modifier ou de les supprimer
- les **Abonnements**, lui permettant de s'abonner à un autre utilisateur, de voir et résilier ses abonnements aux utilisateurs suivis et de voir et bloquer les utilisateurs qui le suivent.
- **Se déconnecter**, pour... se déconnecter et redevenir un simple visiteur !
    
Le design est responsive (mobile, tablette et desktop) et valide les critères d'accessibilité
  
Elle est la première application WEB django que je développe et, si j'ai utilisé Bootstrap5 pour me familiariser avec l'utilisation de framework front-end, j'ai tout de même customisé l'apparence et l'interactivité avec du css et du javascript vanillas.

j'ai utilisé **django 5.1.1** et **bootstrap 5.3.3**

------------------------------------------

## <p align="center">I - Setup windows</p>

#### ( si [Git](https://github.com/git-for-windows/git/releases/download/v2.46.2.windows.1/Git-2.46.2-64-bit.exe) et [python 3.12+](https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe) ne sont pas installés, commencez par l'annexe 1 !)
------------------------------------------
  #### A - Créez un répertoire pour le programme
Lancez votre explorateur windows (WIN+E) 
Créez un répertoire (CTRL+MAJ+N) pour le programme où vous le souhaitez et **nommez-le**
ex. : vous pouvez l'appeler **LITRevu** dans d:\chemin\vers\mon\dossier\LITRevu
**double-cliquez** sur le répertoire créé pour aller dedans.

  #### B - lancez l'interpréteur de commande windows
Clic gauche dans la barre d'adresse de l'explorateur, écrivez **"cmd"** (à la place de l'adresse)
et appuyez sur **"entrée"** (comme à chaque instruction en ligne future):

	cmd
	
  #### C - clonez le repo Github du projet dans ce répertoire
dans le terminal (l'invite de commande) qui indique bien que vous êtes à l'adresse du dossier créé, écrivez tour à tour:

	git init

puis : 

	git pull https://github.com/AdeVedA/LITRevu--OCR_Mission8 -t main

  #### D - installez un environnement virtuel dans un dossier 'env' du projet, toujours par l'invite de commande :
	
	python -m venv env
 
  #### E - activez l'environnement virtuel créé précédemment :
	
	env\Scripts\activate.bat
 
  #### F - installez les librairies requises :
	
	pip install -r requirements.txt

  #### G - mettez-vous dans le répertoire du projet et lancez le serveur (l'environnement virtuel doit avoir été activé avant):

  cd weblog

puis

	python3 manage.py runserver

  #### H - démarrez l'application Web LITRevu dans votre navigateur web en inscrivant l'adresse :

	http://127.0.0.1:8000/

  #### I - fermez le serveur et désactivez l'environnement virtuel quand vous avez fini dans le terminal :

	ctrl +c

puis

	deactivate
-------------------------
-------------------------

## <p align="center">II - Setup Linux/Mac</p>

#### ( si **[Git](https://sourceforge.net/projects/git-osx-installer/files/git-2.23.0-intel-universal-mavericks.dmg/download?use_mirror=autoselect)** et **[python](https://www.python.org/ftp/python/3.12.6/python-3.12.6-macos11.pkg)** ne sont pas installés, commencez par l'annexe 1 !)

-------------------------
	
  #### A- lancez un terminal

clic sur loupe/recherche lancez

	terminal
	
  #### B - Créez un répertoire pour le programme et placez-vous dedans
  par exemple si vous souhaitez appeler ce dossier "LITRevu" :

	mkdir LITRevu

puis :

	cd LITRevu

  #### C - clonez le repo Github du projet dans ce répertoire
dans le terminal (l'invite de commande) qui indique bien que vous êtes à l'adresse du dossier créé, écrivez tour à tour:

	git init

puis : 

	git pull https://github.com/AdeVedA/LITRevu--OCR_Mission8 -t main

  #### D - installez un environnement virtuel dans un dossier 'env' du projet, toujours par le terminal :
	
	python3 -m venv env

  #### E - activez l'environnement virtuel créé précédemment :
	
	source env/bin/activate
 
  #### F - installez les librairies requises :
	
	pip install -r requirements.txt

  #### G - mettez-vous dans le répertoire du projet et lancez le serveur (l'environnement virtuel doit avoir été activé avant):

  cd weblog

puis

	python3 manage.py runserver

  #### H - démarrez l'application Web LITRevu dans votre navigateur web en inscrivant l'adresse :

	http://127.0.0.1:8000/

  #### I - fermez le serveur et désactivez l'environnement virtuel quand vous avez fini dans le terminal :

	ctrl +c

puis

	deactivate


-------------------------
# <p align="center">Annexe 1 - installation de Python & Git</p>
=======================================================================

pour Windows 64bits :
--------------------

installez **[Git](https://github.com/git-for-windows/git/releases/download/v2.46.2.windows.1/Git-2.46.2-64-bit.exe)** 
verifiez en tapant "cmd" dans le menu démarrer puis "git version" dans le terminal

installez **[python](https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe)** en vous assurant que ***"Add to PATH"*** est coché (laissez les autres choix par défaut)
verifiez en tapant "cmd" dans le menu démarrer puis "python --version" dans le terminal

pour Mac/Linux :
--------------------
**Git**
cliquez sur l'icone de recherche (loupe), écrivez "terminal" (on vérifie si git est déjà présent)

	git version

si ok, passez à python. 
sinon, installez ce qu'il vous propose d'installer ("command line developer tools") puis recommencez "git version" en terminal,
sinon : installez **[Git](https://sourceforge.net/projects/git-osx-installer/files/git-2.33.0-intel-universal-mavericks.dmg/download?use_mirror=autoselect)**
puis revérifiez git version dans le terminal

**Python**
installez **[python](https://www.python.org/ftp/python/3.12.6/python-3.12.6-macos11.pkg)**

-------------------------
-------------------------
