---
marp: true
theme: gaia
paginate: true
backgroundImage: url('images/background.png')
style: |
  /* IMPORT POLICES */
  @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Montserrat:wght@600;800&display=swap');
  
  /* VARIABLES */
  :root {
    --color-bg: #fdfbf7;
    --color-text: #2d3436;
    --color-primary: #2c3e50; /* Bleu Foncé */
    --color-accent: #6c5ce7;
    --color-orange: #E65100;  /* Orange */
  }
  
  /* CONFIGURATION GENERALE */
  section {
    font-family: 'Lato', sans-serif;
    font-size: 24px;
    color: var(--color-text);
    background-color: var(--color-bg);
  }
  
  /* --- TYPOGRAPHIE --- */
  h1, h2, h3, h4 {
    font-family: 'Montserrat', sans-serif;
    text-align: center;
    width: 100%;
  }
  
  h1, h2, h3 {
    text-transform: uppercase;
    letter-spacing: -1px;
  }
  
  /* H1 STANDARD (Toutes les slides sauf la 1ère) */
  section:not(.lead) h1 {
    font-size: 1.3em;
    color: var(--color-primary);
    border-bottom: 3px solid var(--color-accent);
    padding-bottom: 10px;
    margin-bottom: 40px;
    margin-top: 0;
  }
  
  /* H1 SPÉCIAL SLIDE 1 */
  section.lead h1 {
    font-size: 2.5em;
    color: var(--color-primary);
    border: none;
    margin-bottom: 10px;
    line-height: 1.1;
  }
  
  /* H2 (Sous-titres) */
  h2 {
    font-size: 0.9em;
    color: var(--color-orange);
    margin-top: 0;
    margin-bottom: 20px;
  }
  
  /* H3 (Titres de blocs) */
  h3 {
    font-size: 0.9em;
    color: var(--color-primary);
    margin-bottom: 15px;
  }

  /* H4 (PHRASES HIGHLIGHTS) */
  h4 {
    font-size: 1.05em;
    color: var(--color-primary); /* Reste de la phrase en bleu foncé */
    font-weight: 600;
    margin-top: 0;
    margin-bottom: 30px;
  }
  
  h4 strong {
    color: var(--color-orange); /* Partie en gras en orange */
    font-weight: 800;
  }
  
  /* LOGO (Coin haut gauche) */
  section::before {
    content: ' ';
    position: absolute;
    top: 10px;
    left: 10px;
    width: 90px;
    height: 90px;
    background-image: url('images/logo_projet.png');
    background-size: contain;
    background-repeat: no-repeat;
    opacity: 0.8;
  }
  
  /* --- SPECIFIQUE SLIDE 1 --- */
  .intro-text-left {
    position: absolute; 
    bottom: 40px;       
    left: 70px;         
    text-align: left;
    font-size: 0.9em;
    color: var(--color-text);
    z-index: 10; 
  }
  
  /* --- STRUCTURES --- */
  .columns {
    display: grid;
    grid-template-columns: 40% 60%;
    gap: 0;
    width: 100%;
  }
  .columns div {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0 30px;
  }
  .columns div:last-child {
    border-left: 2px solid #dcdde1;
  }
  
  /* Staff Grid */
  .staff-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    margin-bottom: 30px;
    width: 100%;
  }
  .staff-list {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .staff-item {
    margin-bottom: 12px;
    display: flex;
    align-items: center;
  }
  
  /* Icones */
  .ico {
    font-size: 28px;
    margin-right: 12px;
    display: inline-block;
  }
  .ico-gold {
    filter: sepia(100%) saturate(1000%) hue-rotate(20deg) brightness(90%);
  }
  
  /* UTILITAIRES */
  .center-img {
    display: block;
    margin: 0 auto;
    text-align: center;
  }
  .center-img img {
    max-height: 250px; /* Limite la taille de l'image pour éviter de déborder */
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  }
  
  /* Tech Comparison */
  .tech-comparison {
    display: grid;
    grid-template-columns: 1fr 1fr;
    width: 100%;
    margin-top: 20px;
  }
  .tech-header {
    padding: 15px;
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: 1.1em;
    text-align: center;
  }
  .header-a {
    background-color: #d1e8e2;
    color: #2c3e50;
    border-right: 2px solid #2d3436;
  }
  .header-b {
    background-color: #bdc3c7;
    color: #2c3e50;
  }
  .tech-body {
    padding: 30px;
    display: flex;
    flex-direction: column;
    gap: 25px;
  }
  .tech-item {
    display: flex;
    align-items: center;
    gap: 15px;
  }
  .tech-item span {
    font-size: 0.9em;
    line-height: 1.2;
  }
  .border-right {
    border-right: 2px solid #2d3436;
  }
  
  /* --- STYLE RGPD --- */
  .rgpd-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 30px;
    margin-top: 40px;
    margin-bottom: 40px;
    text-align: center;
  }
  .rgpd-col {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .rgpd-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 1.1em;
    font-weight: 800;
    margin-bottom: 15px;
    color: var(--color-orange);
  }
  .rgpd-text {
    font-size: 0.9em;
    line-height: 1.3;
    color: #2d3436;
  }
  
  /* --- STYLE CONCLUSION --- */
  .check-item {
    display: flex;
    align-items: center;
    margin-bottom: 30px;
    text-align: left;
  }
  .check-icon {
    width: 55px;
    height: auto;
    margin-right: 20px;
    flex-shrink: 0;
  }
  .check-text {
    font-size: 1em;
    line-height: 1.2;
    color: #000;
  }
  
  /* Boîte de Validation */
  .validation-box {
    border: 4px solid #ff8a65;
    background: linear-gradient(to bottom right, #ffffff, #fbe9e7);
    padding: 30px 20px;
    box-shadow: 0 10px 25px rgba(255, 138, 101, 0.3);
    text-align: center;
    color: #000;
    margin-bottom: 30px;
  }
  
  /* Logo de fin */
  .footer-logo-block {
    margin-top: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .logo-fin {
    width: 280px;
    margin-bottom: 10px;
  }
  .brand-text {
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-size: 0.8em;
    color: #2c3e50;
  }
---

<!-- _class: lead -->

# BrainScanAI
## Labellisation d’images médicales à grande échelle

<div class="center-img" style="margin-top: 30px; margin-bottom: 40px;">
  <!-- L'image HTML s'affichera correctement -->
  <img src="images/intro.png" alt="Illustration BrainScanAI">
</div>

<div class="intro-text-left">
  <strong>Damien GUESDON</strong><br>
  Data Scientist Junior - Computer Vision<br>
  CurelyticsIA<br>
  Mars 2026
</div>

<!-- 
[Durée estimée : 1 minute]

(Sourire, ton confiant et professionnel)
Bonjour, je suis ravi de vous présenter aujourd'hui la première phase du projet "BrainScanAI" pour la startup CurelyticsIA. 

La mission est d'assister les médecins en automatisant la détection de tumeurs cérébrales sur des IRM grâce à l'Intelligence Artificielle. 
Au-delà de la technique, il y a un défi d'envergure, un vrai défi "Business" : nous devons à terme analyser et labelliser 4 millions d'images, avec un budget extrêmement restreint de seulement 5 000 euros. 
-->

---

# 1. Le Défi Métier

#### **Le Problème :** Automatiser la détection de tumeurs sur 4 millions d'images avec un budget limité.

<div class="center-img" style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px; margin-top: 15px;">
  
  <img src="images//irm_budget.png" alt="Illustration métier" height="180">
  <br>
  <img src="images/objective.png" alt="Pipeline du projet" height="180" style="border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">

</div>

<!-- 

Pour y parvenir, j'ai appliqué un pipeline complet de Machine Learning, pour allier précision médicale et rentabilité financière.

Prétraitemetn des images, extraction des features et réduction de dimenstion, clustering (regroupement), génération d'étiquettes (weak labelling), et entrainement du modèle, pour ensuite faire la classification.

-->

---

# 2. La Répartition des Données

#### **Le Constat :** Sur 1506 images, seules 100 sont annotées, imposant une stratégie semi-supervisée.

<div class="center-img">
  <img src="images/data_problem.png" alt="Répartition des données">
</div>

<!-- 
[Durée estimée : 1 minute]

(Ton analytique, on pose le problème)
Pour ce POC, on part d'un échantillon de 1 506 images.
Avant toute chose, j'ai appliqué un prétraitement standardisé : j'ai redimensionné les images en 224x224 et appliqué une normalisation spécifique pour qu'elles soient parfaitement prêtes pour l'analyse.

La vraie difficulté de ce projet, c'est la répartition de nos données : sur ces 1 506 images, nous n'en avons que 100 qui ont été annotées par les médecins. Les 1 406 autres n'ont aucune étiquette. 
Face à ce déséquilibre, il est impossible d'entraîner un modèle supervisé classique à grande échelle.

C'est cette contrainte forte qui nous oriente sur une stratégie "semi-supervisée".

-->

---

# 3. Extraction de Caractéristiques

#### **Zéro Entraînement :** ResNet50 transforme chaque image brute en un vecteur riche de 2048 caractéristiques.

<div class="center-img">
  <img src="images/resnet_pipeline.png" alt="Schéma ResNet50">
</div>

<!-- 
[Durée estimée : 1 minute 15]

(Ton pédagogique, on explique un concept complexe avec des mots simples)
La toute première étape a été d'extraire des informations de ces images brutes.
Entraîner un réseau de neurones convolutif, un CNN, en partant de zéro, demande des millions d'images et une puissance de calcul colossale que nous n'avons pas. 

On doit va donc utiliser le modèle ResNet50.
C'est un modèle qui a déjà été entrainé sur des millions d'images, pour les classifier en différentes classes génériques (chien, chat, avion,...)

Notre objectif étant de différencier des cerveaux comportant des tumeurs, de cerveaux sains, on va retirer la dernière couche de classification qui ne correspond pas à notre contexte.
On ne lui demande pas de classer l'IRM, on l'utilise comme un simple extracteur visuel. 

C'est ce qu'on appelle le Transfert Learning. (utiliser l'entraineemnt existant d'un modèle pour un autre besoin)

Grâce à ça, chaque image radiographique a été transformée en un vecteur mathématique dense de 2 048 dimensions, qui résume parfaitement ses textures, ses contrastes et ses formes.


**Expliquer Comment CNN marche.
Si je dois résumer, un CNN est un réseau de neurones qui applique une série de filtres glissants sur l'image pour y repérer des contrastes, puis des textures de plus en plus complexes. Ici on récupére le résultat mathématique de cette observation visuelle à la sortie de ses filtres : un vecteur de 2 048 dimensions qui résume parfaitement l'IRM.

** Réseau de Neurones
Un réseau de neurones est un modèle mathématique, inspiré du fonctionnement du cerveau humain, qui fait passer l'information à travers des dizaines de couches de calculs successives pour apprendre, par l'exemple, à reconnaître des schémas complexes dans les données. Ici Resnet50 a 50 couches successives.
on apprend des erreurs avec la retropropagation de gradient. Chaque neurone a un poids (une valeur + une formule d'activation)
-->

---

# 4. L'absence de groupes denses évidents

#### **Information diffuse :** La PCA révèle une variance répartie sans variable dominante, et l'algorithme DBSCAN ne détecte que du bruit, confirmant l'absence de densité locale.

<div class="staff-grid" style="align-items: center; margin-bottom: 0;">
  <div class="center-img">
    <h3>Cercle des Corrélations</h3>
    <img src="images/cercle_correlations.png" alt="Cercle de corrélations" style="max-height: 280px; margin-top: 15px;">
  </div>
  <div class="center-img">
    <h3>Clustering DBSCAN (100% Bruit)</h3>
    <img src="images/dbscan_3d.png" alt="Visualisation 3D DBSCAN" style="max-height: 280px; margin-top: 15px;">
  </div>
</div>

<!-- 
[Durée estimée : 1 minute 30]

(Ton explicatif pour anticiper la question du mentor sur DBSCAN et la PCA)
Cependant, travailler sur 2 048 dimensions, c'est trop lourd, trop bruité.
On applique donc une PCA, une Analyse en Composantes Principales, pour compresser ces données à 50 dimensions, tout en conservant l'information mathématique utile.

** Expliquer PCA

On voit sur le cercle des corrélations généré par la PCA que l'information est très diffuse. Les flèches pointent dans toutes les directions. Il n'y a pas de variable dominante. 
C'est ce qui explique parfaitement pourquoi l'algorithme de clustering DBSCAN testé a échoué juste après.
DBSCAN est conçu pour chercher des « nuages de points denses ».

Ici, l'information visuelle étant extrêmement diffuse, DBSCAN n'a trouvé aucun groupe et a classé 100% de nos images comme du "bruit" !
Son score ARI a d'ailleurs été impossible à calculer. Il a donc fallu changer d'approche.


Cercle de corrélation : On obtient le cercle de corrélation en réalisant une Analyse en Composantes Principales (PCA) projetée sur deux dimensions afin de visualiser la contribution des variables d'origine aux deux axes principaux
.
DBSCAN : L'algorithme DBSCAN effectue son regroupement en recherchant des zones présentant une forte densité locale (des nuages de points très rapprochés), et classe les points isolés restants comme du bruit (ça marche par proximité)

-->

---

# 5. Le choix du nombre de clusters (K)

#### **Évaluation des métriques :** L'inertie et la silhouette orientent vers K=2, tandis que le **dendrogramme** confirme l'existence de regroupements naturels.

<div class="center-img" style="display: flex; flex-direction: column; align-items: center; gap: 15px; margin-top: 10px;">
  
  <img src="images/choix_k.png" alt="Inertie et Silhouette" height="220">
  <br> 
  <img src="images/dendrogramme.png" alt="Dendrogramme" height="220">

</div>

<!-- 
[Durée estimée : 1 minute 15]

(Ton enthousiaste, on a trouvé une solution)
Je me suis donc tourné vers d'autres algorithmes. J'ai d'abord généré un dendrogramme via un clustering hiérarchique. Ce dernier a l'avantage de relier les images par similarité (par paires), et il m'a confirmé visuellement que des regroupements naturels existaient bien dans nos données.

Ici plus les branches verticales sont hautes, plus les différences sont élevées, donc plus il y a un écart vertical important, plus les groupes sont marqués.

Je suis ensuite passé sur un algorithme KMeans. Il fallait choisir le bon nombre de groupes, qu'on appelle K.

Il y a plusieurs méthodes pour le définir.
Par exemple la méthode du coude, où là on n'observe pas vraiment d'irrégularité,
Et le Score de Silhouette pour différentes valeurs (de 2 à 15), où le score était maximal pour K=2, on voit également des pics potentiellement intéressants pour k=10 ou k=11. 

Comme les chiffres convergent vers k=2 et que ça répond à notre logique métier (cerveau sain vs malade), je m'oriente vers cette option.




La méthode du coude : Elle consiste à tracer la courbe de l'inertie (c'est-à-dire la dispersion des points au sein de leurs groupes) en fonction du nombre de clusters (K), et à choisir l'endroit où la courbe se casse nettement (le fameux "coude"), ce qui indique mathématiquement qu'ajouter davantage de groupes n'améliore plus vraiment la séparation des données
.
Le score de Silhouette : Il évalue la qualité de ces groupes en mesurant si chaque image est très proche des membres de sa propre famille et, à l'inverse, bien éloignée des familles voisines

-->

---

# 6. L'organisation non supervisée

#### **Séparation métier :** Le KMeans (K=2) offre le regroupement binaire (Cancer vs Normal) le plus pertinent.

<div class="rgpd-grid" style="margin-top: 10px; margin-bottom: 0; gap: 15px;">
  <div class="rgpd-col">
    <h3>K = 2</h3>
    <img src="images/kmeans_k2.png" alt="KMeans K=2" height="220" style="border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
  </div>
  <div class="rgpd-col">
    <h3>K = 10</h3>
    <img src="images/kmeans_k10.png" alt="KMeans K=10" height="220" style="border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
  </div>
  <div class="rgpd-col">
    <h3>K = 11</h3>
    <img src="images/kmeans_k11.png" alt="KMeans K=11" height="220" style="border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
  </div>
</div>

<!-- 
[Durée estimée : 1 minute]

(Ton de la preuve scientifique)
Voici la modélisation en 3D de notre algorithme KMeans avec K=2. On voit que les deux groupes se dégagent.
Mais comme le modèle a fait ses regroupements à l'aveugle, il faut en vérifier mathématiquement la correspondance.

Pour le vérifier, j'ai calculé le score ARI (Adjusted Rand Index). C'est une métrique qui compare les groupes déterminés par le modèle, avec les 100 vrais labels des médecins.
Un score ARI de 0 équivaut à un regroupement fait totalement au hasard. Notre modèle a obtenu 0.485.

Cela prouve de manière irréfutable que l'algorithme a trouvé une séparation logique et pertinente, bien au-dessus de la chance, justifiant la suite du projet !





Le KMeans : L'algorithme place initialement de manière aléatoire un nombre défini de centres de gravité (ici K=2) dans l'espace de vos données, puis rattache chaque image au centre le plus proche en réajustant la position de ces centres en boucle jusqu'à obtenir des groupes géométriquement stables
.
Le score ARI : La formule simplifiée consiste à calculer le taux de correspondance exact entre les groupes créés par la machine et les vraies étiquettes de vos médecins, puis à lui soustraire mathématiquement le score de réussite qu'aurait obtenu un regroupement fait totalement au hasard

-->

---

# 7. Stratégie du "Weak Labeling"

#### **Aucune fuite de données :** Une séparation stricte Train/Test permet d'associer logiquement un label au cluster.

<div class="tech-comparison">
  <div class="tech-header header-a">Cluster 0 (Label Normal)</div>
  <div class="tech-header header-b">Cluster 1 (Label Cancer)</div>
  <div class="tech-body border-right">
    <div class="tech-item"><span class="ico ico-gold">✔</span><span><strong>Images totales :</strong> 675</span></div>
    <div class="tech-item"><span><strong>Taux de confiance :</strong> 75%</span></div>
  </div>
  <div class="tech-body">
    <div class="tech-item"><span class="ico ico-gold">✔</span><span><strong>Images totales :</strong> 831</span></div>
    <div class="tech-item"><span><strong>Taux de confiance :</strong> 94%</span></div>
  </div>
</div>

<!-- 
[Durée estimée : 1 minute 30]

(Ton sérieux, on parle de la rigueur de la méthode)
C'est ici que commence le cœur de l'approche semi-supervisée : le "Weak Labeling", ou l'étiquetage faible. 
L'objectif est d'associer nos 1 406 images non labellisées à leur groupe (Cancer ou Normal), tout en évitant le piège du Data Leakage, la fuite de données ! 

J'ai splitté les données en 2 groupes, un premier pour l'entraînement, et un second qui ne sera utilisé que pour le test final, pour l'évaluation des résultats. Le modèle ne les a jamais vues.

Compte tenu du faible volume, j'ai opté pour 50% des données, pour avoir sufisament d'infos et pour l'entrainement et pour le test (donc 25 images saines, 25 images avec cancer pour chacun des deux jeu (train et test)), 

En regardant uniquement nos 50 données d'entraînement, il ressort que le Cluster 1 contient 94% de cancers. C'est donc cette étiquette (Weak Label) qui sera attribuée à toutes les images qui tombent dans ce cluster.
-->

---

# 8. Filtrage des Labels Faibles

#### **Exigence de fiabilité :** Seules les images avec une confiance au cluster très élevée sont retenues.

<div class="rgpd-grid">
  <div class="rgpd-col">
    <div style="font-size: 80px; margin-bottom: 20px; line-height: 1;">🗂️</div>
    <div class="rgpd-title">1 406</div>
    <div class="rgpd-text">Images brutes non labellisées attribuées à un cluster.</div>
  </div>
  <div class="rgpd-col">
    <div style="font-size: 80px; margin-bottom: 20px; line-height: 1;">🎯</div>
    <div class="rgpd-title">Seuil > 80%</div>
    <div class="rgpd-text">Application stricte d'un filtre de confiance algorithmique.</div>
  </div>
  <div class="rgpd-col">
    <div style="font-size: 80px; margin-bottom: 20px; line-height: 1;">✅</div>
    <div class="rgpd-title">792</div>
    <div class="rgpd-text">"Labels Faibles" fiables et retenus pour l'entraînement.</div>
  </div>
</div>

<!-- 
[Durée estimée : 1 minute]

(Montrer de l'esprit critique)
Cependant, pour le cluster « Normal », le modèle n'était sûr qu'à 75% (seuls 75% des images étaient des radios de cerveaux sains). 
Si j'avais donné ces 1 406 images brutes directement à la machine pour s'entraîner, elle aurait appris sur beaucoup d'erreurs potentielles, ce qui aurait généré du bruit et dégradé le modèle.

J'ai donc appliqué un filtre algorithmique très strict, pour ne garder que les images avec plus de 80% de confiance au sein de leur cluster.
Résultat : sur les 1 406 images, nous n'en avons conservé que 792. Ce sont 792 images extrêmement fiables qui ont enrichi notre jeu d'entraînement.





On calcule la proportion de la classe majoritaire parmi nos quelques données labellisées d'entraînement au sein de chaque cluster, et on ne conserve pour la suite de l'apprentissage que les images appartenant à un groupe dont cette "pureté" statistique atteint au moins 80%
-->

---

# 9. Le Choix de la Métrique

#### **Enjeu médical vital :** Ne rater aucune tumeur (Faux Négatif). La métrique reine est donc le Recall (Rappel).

<div class="center-img">
  <img src="images/matrice_confusion.png" alt="Matrice de Confusion">
</div>

<!-- 
[Durée estimée : 1 minute]

(Ton plus grave et insistant, on parle de vie humaine)
Avant de regarder les résultats de notre modèle, il faut définir notre "juge de paix". Quelle métrique regarder ? 
En médecine, "l'Accuracy" (le pourcentage global de bonnes réponses) est un piège. 

Notre enjeu vital, c'est de ne rater aucune tumeur. On préfère largement déclencher une fausse alerte et faire des examens supplémentaires, plutôt que de renvoyer un patient chez lui avec une tumeur non détectée : c'est ce qu'on appelle un Faux Négatif, et c'est dramatique. 
La métrique reine absolue que j'ai choisi de surveiller et d'optimiser, c'est donc le Recall, le Rappel en français, qui mesure notre capacité à détecter tous les vrais malades.

** Expliquer la matrice de confusion
-->

---

# 10. Supervisé VS Semi-Supervisé

#### **Évaluation des performances :** L'ajout brut de données dégrade le Recall, prouvant la nécessité du filtre pour dépasser la baseline.

<div class="rgpd-grid" style="margin-top: 10px; gap: 0; border: 2px solid #2d3436; border-radius: 8px; overflow: hidden; background-color: var(--color-bg);">

  <div style="display: flex; flex-direction: column; border-right: 2px solid #2d3436;">
    <div class="tech-header header-b" style="border-bottom: 2px solid #2d3436;">Supervisé Pur<br><span style="font-size: 0.75em; font-weight: normal;">(Baseline)</span></div>
    <div class="tech-body" style="padding: 20px;">
      <div class="tech-item" style="justify-content: center;"><span><strong>Accuracy globale :</strong> 0.90</span></div>
      <div class="tech-item" style="justify-content: center;"><span><strong>F1-Macro :</strong> 0.90</span></div>
      <div class="tech-item" style="justify-content: center;"><span><strong>Recall (Cancer) :</strong> 0.92</span></div>
    </div>
  </div>

  <div style="display: flex; flex-direction: column; border-right: 2px solid #2d3436;">
    <div class="tech-header" style="background-color: #ffeaa7; color: #2c3e50; border-bottom: 2px solid #2d3436;">Semi-Sup. Brut<br><span style="font-size: 0.75em; font-weight: normal;">(+ 1406 labels)</span></div>
    <div class="tech-body" style="padding: 20px;">
      <div class="tech-item" style="justify-content: center;"><span><strong>Accuracy globale :</strong> 0.88</span></div>
      <div class="tech-item" style="justify-content: center;"><span><strong>F1-Macro :</strong> 0.88</span></div>
      <div class="tech-item" style="justify-content: center;"><span style="color: #c0392b;"><strong>Recall (Cancer) : 0.80 ⚠️</strong></span></div>
    </div>
  </div>

  <div style="display: flex; flex-direction: column;">
    <div class="tech-header header-a" style="border-right: none; border-bottom: 2px solid #2d3436;">Semi-Sup. Filtré<br><span style="font-size: 0.75em; font-weight: normal;">(+ 792 labels)</span></div>
    <div class="tech-body" style="padding: 20px;">
      <div class="tech-item" style="justify-content: center;"><span><strong>Accuracy globale :</strong> 0.92</span></div>
      <div class="tech-item" style="justify-content: center;"><span><strong>F1-Macro :</strong> 0.92</span></div>
      <div class="tech-item" style="justify-content: center;"><span style="color: #27ae60;"><strong>Recall (Cancer) : 0.92 ✅</strong></span></div>
    </div>
  </div>

</div>

<!-- 
[Durée estimée : 1 minute 15]

(Ton dynamique, c'est l'heure du bilan technique)
Voici les résultats finaux, validés sur notre jeu de test qui est resté totalement imperméable. 

Notre "modèle supervisé pur", qui est notre point de départ entraîné uniquement sur 50 images, avait un Recall de 0.92. 
Avec les 1 406 labels faibles sans les filtrer, le modèle apprend sur du bruit, et le Recall s'effondre à 0.80. Autrement dit, le modèle est moins efficace que le supervisé et rate des cancers !
Grâce à notre "Weak Labeling filtré", le modèle semi-supervisé cible a fait remonter la précision (l'Accuracy) globale, tout en maintenant le Recall maximal à 0.92. La stratégie de filtrage est donc un succès total.
On est aussi pertinents que le supervisé pur sur le recall, et en plus on gagne en précision (moins de fausses alertes)
-->

---

# 11. Analyse des Incertitudes

#### **Active Learning :** La prédiction cible précisément les cas "ambigus" nécessitant l'expertise du radiologue.

<div class="staff-grid">
  
  <div class="rgpd-col">
    <center>
      <div style="font-size: 60px; margin-bottom: 20px;">🤖 ➡️ 🧑‍⚕️</div>
      <div class="rgpd-title">Score de confiance ~ 50%</div>
      <div class="rgpd-text">Au lieu de tout labelliser, le modèle isole uniquement les cas où il "hésite" pour les envoyer à un expert.</div>
    </center>
  </div>

  <div class="rgpd-col">
    <center>
      <h3>Extrait des prédictions</h3>
      <img src="images/table_incertitudes.png" alt="Tableau des incertitudes" width="100%">
    </center>
  </div>

</div>

<!-- 
[Durée estimée : 1 minute]

(Ton complice, on dévoile l'astuce pour la suite)
On va maintenant s'appuyer sur l'analyse des probabilités pour améliorer l'ensemble. 
Le modèle ne se contente pas de dire simplement « Cancer » ou « Normal ». Il dit par exemple « C'est un cancern et j'en suis sûr à 99% ». 

Ce pourcentage de certitude est les predict proba.

Comme vous le voyez sur ce tableau extrait de mes tests, la machine est capable d'isoler mathématiquement les cas où elle « hésite » fortement, c'est-à-dire quand la probabilité tourne autour de 50%. Ce concept, c'est ce qu'on appelle l'Active Learning (l'Apprentissage Actif). Et c'est exactement la réponse budgétaire pour notre passage à l'échelle.

** Expliquer comment on calcule le predict proba.

Y a un truc avec la courbe sigmoïde, mais je ne sasi plus exactement commetn ça marche. 
-->

---

# 12. Passage à l'échelle & Recommandations

#### **Optimisation Budget :** Les 5 000€ seront exclusivement dédiés à la labellisation par les experts des 10% de cas incertains.

<br>
<div class="check-item">
  <div class="check-icon">⚡</div>
  <div class="check-text"><strong>Automatisation :</strong> La pipeline attribue automatiquement un label à ~90% des 4 Millions d'images.</div>
</div>
<div class="check-item">
  <div class="check-icon">🩺</div>
  <div class="check-text"><strong>Focalisation :</strong> Les probabilités proches de 0.5 déclenchent l'expertise humaine, divisant radicalement les coûts d'annotation.</div>
</div>

<!-- 
[Durée estimée : 1 minute 30]

(Ton "Chef de Projet", très convaincant, on termine en beauté)
C'est grâce à ça qu'on va pouvoir traiter 4 millions d'images avec seulement 5 000 euros ?

L'annotation humaine a coûté 300 euros pour nos 100 premières images, soit 3 euros par image. Avec un budget de 5 000 euros, et en conservant ce barème, on peut donc payer des médecins pour relire 1 666 images (4998€). 
On est encore loin des 4 millions.

Mais on peut procéder ainsi :
Notre modèle semi-supervisé va d'abord auto-labelliser "quasi gratuitement" les 4 millions d'images (je ne compte pas les coûts électrique d'exploiration des serveurs et de calcul, car on n'a pas l'information dans la mission, je suppose donc que ça ne fait pas partie de l'équation).
Ensuite, l'algorithme va extraire de cette masse gigantesque *précisément* les 1 666 cas les plus incertains (ceux proches de 50%).
Nous sanctuariserons donc les 5 000 euros pour faire trancher uniquement ces 1 666 cas très difficiles par des experts, puis nous ré-entraînerons le modèle avec ce nouveau savoir humain, ce qui devrait améliorer significativement les résultats, et on relabellise l'ensemble avec ce modèle réentrainé.
C'est ce qu'on appelle l'Active Learning (on cible sur quelles données on réentraine le modèle, au lieu de le faire en full automatique).

-->

---

<br><br>
<div class="validation-box">
  <h3 style="text-transform:none; color:var(--color-primary); margin:0;">
    Preuve de concept validée : l'intégration d'une boucle semi-supervisée stricte fiabilise et massifie les données tout en respectant l'enveloppe budgétaire.
  </h3>
</div>

<div class="footer-logo-block">
  <img src="images/logo_projet.png" class="logo-fin" alt="Logo CurelyticsIA">
  <div class="brand-text">CurelyticsIA - Innovation e-Santé</div>
</div>

<!-- 
Grâce à cette boucle d'Active Learning, nous obtenons une IA performante à l'échelle industrielle, sans perte de qualité médicale, et tout en respectant notre enveloppe budgétaire au centime près ! 

Je vous remercie de votre attention et je suis à votre disposition pour vos questions !
-->
