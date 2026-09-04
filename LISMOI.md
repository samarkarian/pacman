Creation d'abstractmethod pour les entites et leur systeme de rendu:
dans la boucle principale pygame, on aura donc juste a lire une liste de toutes les entites, et appeler entity.load() et entity.render() par ex

creation du maze avec les sprites
J'ai vlonte a creer une nomenclature pour les sprites, poour avoir une lecture auto;atique des sprites en fonction de la size en pixels choisis
la nomenclature :
sprites/classe/sous-classe/entiteprecise/entiteprecise_taille/entiteprecise_taille_frame_numerofame
ex:
sprites/Entities/Ghost/Ghost_cyan/Ghost_cyan_64/Ghost_cyan_64_frame_0.png