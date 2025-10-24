import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from sklearn.metrics import confusion_matrix
import seaborn as sns
import joblib



# Chemin vers les répertoires d'entraînement et de test
train_path = './dataset/train'
test_path = './dataset/test'

#Liste des catégories de produits
categories = os.listdir(train_path)

# Charger un modèle CNN pré-entraîné (VGG16)
base_model = VGG16(  # Instancie le modèle VGG16
    weights='imagenet',  # Précise que les poids pré-entraînés sur le jeu de données ImageNet doivent être utilisés
    include_top=False,  # Indique que la couche fully connected (top) du modèle VGG16 ne doit pas être incluse
    input_shape=(100, 100, 3)  # Spécifie la forme des images en entrée du modèle (hauteur, largeur, nombre de canaux)
)

# Extraire les caractéristiques des images à partir du modèle CNN pré-entraîné
def extract_features(img_path):
    img = image.load_img(img_path, target_size=(100, 100)) # Charge l'image depuis le chemin d'accès spécifié et redimensionne à la taille attendue par le modèle (100x100 pixels)
    x = image.img_to_array(img)# Convertit l'image en tableau numpy
    x = np.expand_dims(x, axis=0)  # Ajoute une dimension supplémentaire pour correspondre à la forme attendue par le modèle
    x = preprocess_input(x) # Prétraite l'image pour la rendre compatible avec le modèle VGG16 (normalisation)
    features = base_model.predict(x) # Utilise le modèle VGG16 pour prédire les caractéristiques de l'image
    return features.flatten()  # Aplati le tensor de caractéristiques pour obtenir un vecteur de caractéristiques unidimensionnel

# Prétraitement et extraction des caractéristiques des images d'entraînement
train_features = []
train_labels = []

for category_id, category in enumerate(categories):  # Boucle à travers chaque catégorie avec son identifiant
    category_train_path = os.path.join(train_path, category) # Chemin d'accès au dossier d'entraînement pour la catégorie actuelle
    images = os.listdir(category_train_path) # Liste des noms de fichiers d'images dans le dossier d'entraînement de la catégorie
    for image_name in images:  # Boucle à travers chaque image dans la catégorie
        image_path = os.path.join(category_train_path, image_name) # Chemin d'accès complet de l'image
        features = extract_features(image_path)  # Extraction des caractéristiques de l'image à l'aide de la fonction extract_features
        train_features.append(features)  # Ajout des caractéristiques extraites à la liste des caractéristiques d'entraînement
        train_labels.append(category_id) # Ajout de l'identifiant de catégorie à la liste des étiquettes d'entraînement

# Prétraitement et extraction des caractéristiques des images de test
test_features = []
test_labels = []

for category_id, category in enumerate(categories):
    category_test_path = os.path.join(test_path, category)
    images = os.listdir(category_test_path)
    for image_name in images:
        image_path = os.path.join(category_test_path, image_name)
        features = extract_features(image_path)
        test_features.append(features)
        test_labels.append(category_id)

# Convertir les listes d'images en tableaux numpy
train_features = np.array(train_features)  # Convertit la liste des caractéristiques d'entraînement en un tableau numpy
test_features = np.array(test_features) # Convertit la liste des caractéristiques de test en un tableau numpy
train_labels = np.array(train_labels)  # Convertit la liste des étiquettes d'entraînement en un tableau numpy
test_labels = np.array(test_labels) # Convertit la liste des étiquettes de test en un tableau numpy

# Entraîner un classificateur de forêts aléatoires
random_forest = RandomForestClassifier(n_estimators=100, random_state=42) # Crée un classificateur de forêts aléatoires avec 100 estimateurs et une graine aléatoire fixée à 42
random_forest.fit(train_features, train_labels) # Entraîne le classificateur de forêts aléatoires sur les caractéristiques d'entraînement et les étiquettes correspondantes

# Prédire les étiquettes des données de test
predictions = random_forest.predict(test_features) # Utilise le modèle entraîné pour prédire les étiquettes des données de test

# Calculer l'exactitude du classificateur
accuracy = accuracy_score(test_labels, predictions) # Calcule l'exactitude du modèle en comparant les étiquettes prédites avec les étiquettes réelles des données de test
print("Précision du modèle RandomForest:", accuracy)

# Calculer la matrice de confusion
conf_matrix = confusion_matrix(test_labels, predictions) # Calcule la matrice de confusion en comparant les étiquettes réelles avec les étiquettes prédites

# Afficher la matrice de confusion sous forme de heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='g', xticklabels=categories, yticklabels=categories)
plt.xlabel('Classe prédite')
plt.ylabel('Classe réelle')
plt.title('Matrice de confusion')
plt.show()

model_path="model_rf.pkl" # Définit le chemin de sauvegarde du modèle RandomForest
joblib.dump(random_forest,model_path) # Enregistre le modèle RandomForest dans un fichier pkl à l'emplacement spécifié
print("Avec succes")
