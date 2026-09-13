Mise en place de classes pour les objets player et ghost, ceux ci contiennent desormais un renderer et un controller, permettant de separer les roles
classe pacgum au lieu d'avoir une liste de coordonnees
class game gere desormais toute la logique du jeu, et se fait appeler par la GameScene, qui gere les inputs et mets a jour le jeu a chaque tick avec les fonctions update()
menu de game over (on doit encore mettre des sprites et des boutons)
methods de reinitialisation de la position du joueur et des fantomes apres un kill
nouvel etat de joueur et de ghost pour modifier les sprites (sens pour le joueur, mode vulenrable pour les fantomes, et mode 'end' clignotant quand les fantomes ne sont bientot plus vulnerables)
ajout de la classe UISprite pour mettre un sprite statique. methods a modifier (facile) pour les rendre animables. pour l'instant statique
deplacement fluide des fantomes a l'aide d'un lerp

a faire :
centering des sprites dans les menus, et positionnement de tout en general
gerer le vitesse de deplacement du joueur avec update() (pac man ne doit pas aller a la meme vitesse que les fantomes (!!!) il doit etre un peu plus rapide, et avoir une gestion de deplacements differents)
AI des fantomes
deplacement fluide du joueur a la place des teleportations
affichage score et vie
GROS MORCEAU : generer les differents niveau et gerer le changement entre les scenes, puis stocker le high score, gerer l'entree de noms de joueurs
mode invincible
polish des assets et des visuels du jeu
retirer les variables globales
