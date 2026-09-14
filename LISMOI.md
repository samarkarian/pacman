Mise en place de classes pour les objets player et ghost, ceux ci contiennent desormais un renderer et un controller, permettant de separer les roles
classe pacgum au lieu d'avoir une liste de coordonnees
class game gere desormais toute la logique du jeu, et se fait appeler par la GameScene, qui gere les inputs et mets a jour le jeu a chaque tick avec les fonctions update()
menu de game over (on doit encore mettre des sprites et des boutons)
methods de reinitialisation de la position du joueur et des fantomes apres un kill
nouvel etat de joueur et de ghost pour modifier les sprites (sens pour le joueur, mode vulenrable pour les fantomes, et mode 'end' clignotant quand les fantomes ne sont bientot plus vulnerables, mode 'dead' quand les fantomes attendent leur respawn)
ajout de la classe UISprite pour mettre un sprite statique. methods a modifier (facile) pour les rendre animables. pour l'instant statique
deplacement fluide des fantomes a l'aide d'un lerp, pareil pour le joueur

a faire :
centering des sprites dans les menus, et positionnement de tout en general
AI des fantomes
deplacements du joueurs mieux faits. actuellement, le ressenti est etrange, car si la nouvelle directement n'est pas possible, il la garde en cache, et slide en continuant dans la direction precedente jusqu'a pouvoir tourner. c'est malin mais ca donne un ressenti desagreable
affichage score et vie
generer les differents niveau et gerer le changement entre les scenes, le chargement des niveaux avec les fonctions reset()
stocker le high score, gerer l'entree de noms de joueurs
menu pause ?
mode invincible
polish des assets et des visuels du jeu
retirer les variables globales

