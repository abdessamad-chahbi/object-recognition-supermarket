import joblib
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications import VGG16
import os

# Charger le modèle Random Forest à partir du fichier model_rf.pkl
random_forest = joblib.load('model_rf.pkl')
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(100, 100, 3))

categories=[
            'Arla-Ecological-Medium-Fat-Milk', 
            'Arla-Medium-Fat-Milk', 
            'Arla-Standard-Milk', 
            'Bravo-Apple-Juice', 
            'Bravo-Orange-Juice', 
            'God-Morgon-Red-Grapefruit-Juice'
            ]

# Extraire les caractéristiques des images à partir du modèle CNN pré-entraîné
def extract_features(img_path):
    img = image.load_img(img_path, target_size=(100, 100))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = base_model.predict(x)
    return features.flatten()

def predict_image_class(image_path):
    # Extraire les caractéristiques de l'image
    features = extract_features(image_path)
    # Prédire la classe de l'image à l'aide du classificateur Random Forest
    predicted_label = random_forest.predict([features])[0]
    # Récupérer le nom de la classe prédite
    predicted_class = categories[predicted_label]
    return predicted_class

# # Exemple d'utilisation de la fonction pour prédire la classe d'une image spécifique
# p="/dataset/train/God-Morgon-Red-Grapefruit-Juice/God-Morgon-Red-Grapefruit-Juice_024.jpg"
# predicted_class = predict_image_class(p)
# print("Classe prédite de l'image :", predicted_class)
