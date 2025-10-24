# 🛒 Object Recognition for Supermarkets

> 📌 This project is a desktop application designed for **automatic product recognition in supermarkets**. Built with **Python, PyQt5 GUI and integrated CNN backbones (MobileNetV2, VGG16) for feature extraction and classification**.        
> The app links to **MySQL** to store and retrieve product information and supports classical ML baselines **(SVM, KNN, Random Forest)** as well as **deep feature extraction**.

---

## 📘 Table of Contents

- Project Overview  
- Key Features  
- Dataset  
- Machine Learning Approaches  
- Tech Stack & Tools  
- Application Functionalities  
- System Architecture  
- How to Run  
- Results 
- Future Work  

---

## 🧩 Project Overview

This project implements a desktop image recognition system tailored to supermarket products. It allows capture and recognition of product images, displays extracted features and product metadata, and supports training/evaluation workflows. The goal is to provide a usable prototype that combines classical ML and deep learning feature extraction for robust product classification.

---

## ✨ Key Features

- GUI application implemented with PyQt5 for easy image capture, preview, and management.  
- Image preprocessing and augmentation helpers (resize, normalization, flattening).  
- CNN-based feature extraction using pre-trained architectures (VGG16, MobileNetV2).  
- Classical classifiers: SVM (linear kernel), KNN, Random Forest for final classification.  
- Persistent product metadata stored and retrieved via MySQL.  
- Training, validation and test pipeline with reproducible splits.  
- Save / load models and feature vectors for later prediction.  

---

## 🗂️ Dataset

The dataset used is **GroceryStoreDataset**, organized into:

* `train/`
* `test/`
* `validation/`

Each contains subcategories:

* Fruits
* Vegetables
* Packaged items

📌 For this project, only **Packaged Items (épiceries)** category was used:

| Split      | Images Count |
| ---------- | ------------ |
| Train      | 289          |
| Test       | 67           |
| Validation | 27           |

Images include different angles and lighting conditions for better generalization.

---

## 🧠 Machine Learning Approaches

### 🔹 1️⃣ Model without feature extraction → SVM

* Image resizing + flattening
* Hyperparameter tuning using `GridSearchCV`
* **Accuracy: 89%**

---

### 🔹 2️⃣ Feature Extraction using CNN (VGG16)

We used a pre-trained **VGG16** model (ImageNet) to extract deep visual features:

* Removed fully connected layers (`include_top=False`)
* Input size: **100 × 100 × 3 (RGB)**

Extracted features were used with:

| Classifier    | Accuracy   |
| ------------- | ---------- |
| SVM (Linear)  | 97% ✅      |
| KNN (k=3)     | 79% ⚠️     |
| Random Forest | **98% 🏆** |

👉 Best performance achieved using **Random Forest + VGG16** features.

---

## 🛠️ Tech Stack & Tools

| Category      | Tools                           |
| ------------- | ------------------------------- |
| Programming   | Python                          |
| GUI           | PyQt5                           |
| ML/DL         | TensorFlow, Keras, Scikit-Learn |
| CV            | OpenCV                          |
| Database      | MySQL                           |
| Data Handling | Pandas, NumPy                   |
| Visualization | Matplotlib                      |

---

## 📸 Application Functionalities

* Load product image
* Display predicted product class
* Fetch product details from MySQL
* Add/remove/update product entries in database
* Retrain model with newly labeled data

---

## 📊 System Architecture

```
Dataset → Feature Extraction (VGG16) → Classifier (SVM / RF) → Prediction
                     ↓
                 MySQL Database → Product Info Display
                     ↓
                    GUI (PyQt5)
```

---

## ▶️ How to Run

1️⃣ Clone the project:

```bash
git clone https://github.com/abdessamad-chahbi/object-recognition-supermarket.git
cd object-recognition-supermarket
```

2️⃣ (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

3️⃣ Install dependencies:

```bash
pip install -r requirements.txt
```

4️⃣ Configure MySQL database connection

5️⃣ Launch the application:

```bash
python InterfaceGraphique.py
```

---

## ✅ Results

* ✔︎ High-performance classification
* ✔︎ Real-time recognition
* ✔︎ Easy UI for supermarket operations automation

---

## 🔮 Future Work

- Expand dataset to include fruits & vegetables classes for full supermarket coverage.  
- Add real-time camera integration with barcode scanning.  
- Add object detection (YOLO/Faster-R-CNN) 
- Deploy a lightweight REST API to serve model predictions and integrate with point-of-sale systems.  
- Add unit tests and CI pipeline for reproducibility.

---
