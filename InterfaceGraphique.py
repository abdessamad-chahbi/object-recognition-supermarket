import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QDesktopWidget, QFileDialog, QWidget ,QLineEdit
from PyQt5.QtGui import QPixmap, QFont,QIcon
from PyQt5.QtCore import Qt,QSize
import Prediction,dataBase


class HoverButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setStyleSheet(
            "border:none; background-color:transparent; padding: 5px;"
        )  # Style de base sans bordure et fond transparent
        self.iconSizeNormal = QSize(70, 70)
        self.iconSizeHover = QSize(80, 80)
        self.setIconSize(self.iconSizeNormal)  # Taille de l'icône par défaut

    def enterEvent(self, event):
        self.setIconSize(self.iconSizeHover)  # Augmenter la taille de l'icône lors du survol
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setIconSize(self.iconSizeNormal)  # Rétablir la taille de l'icône lorsqu'il n'est pas survolé
        super().leaveEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reconnaissance de Produits")
        self.resize_to_screen()  # Appel de la fonction pour redimensionner la fenêtre
        self.set_background_image("./icones/store.jpg")  # Appel de la fonction pour définir l'image de fond

        # Ajouter un cadre avec un bouton "plus" au milieu
        self.add_frame()

        # Ajouter un label avec un texte attrayant
        self.add_main_label()
        
        self.add_buttons()
        
        self.add_product_info()
        self.cnx=dataBase.Connexion()

    def resize_to_screen(self):
        desktop = QDesktopWidget().screenGeometry()  # Obtenir la géométrie de l'écran
        self.setGeometry(0, 0, desktop.width(), desktop.height())  # Définir la taille de la fenêtre à la taille de l'écran

    def set_background_image(self, image_path):
        # Charger l'image de fond
        pixmap = QPixmap(image_path).scaled(self.width(), self.height())

        # Créer un label pour afficher l'image de fond
        background_label = QLabel(self)
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())

        # Ajouter une superposition sombre et transparente
        overlay = QWidget(self)
        overlay.setGeometry(0, 0, self.width(), self.height())
        overlay.setStyleSheet("background-color: rgba(0, 0, 0, 170);")  # Ajuster l'alpha pour plus de transparence

    def add_frame(self):
       # Créer un cadre pour afficher la photo téléchargée
       self.frame = QLabel(self)
       self.frame.setGeometry(130, self.height() // 2 - 250, 600, 600)  # Taille fixe pour le cadre
       self.frame.setStyleSheet("background-color: rgba(213, 210, 210, 100); border: 2px solid #000000;")
       self.frame.setAlignment(Qt.AlignCenter)



    def add_main_label(self):
        main_label = QLabel("Bienvenue dans l'application de reconnaissance de produits !", self)
        main_label.setFont(QFont("Arial", 28, QFont.Bold))  # Définir la police et la taille du texte
        main_label.setStyleSheet("color: white;")  # Définir la couleur du texte
        main_label.setAlignment(Qt.AlignCenter)  # Centrer le texte dans le label
        main_label.setGeometry(100, 20, self.width() - 200, 200)  # Ajuster la position et la taille selon vos besoins
        
    
    def add_buttons(self):
        # Créer les boutons "Upload" et "Reset" avec les images correspondantes
        upload_button = HoverButton(self)
        upload_button.setIcon(QIcon("./icones/upload.png"))
        upload_button.setGeometry(740, 400, 80, 80)
        upload_button.clicked.connect(self.import_photo)

        reset_button = HoverButton(self)
        reset_button.setIcon(QIcon("./icones/reset.png"))
        reset_button.setGeometry(740, 700, 80, 80)
        reset_button.clicked.connect(self.reset_frame)
    

    def import_photo(self):
      file_dialog = QFileDialog(self)
      file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
      file_dialog.setViewMode(QFileDialog.List)
      file_dialog.setFileMode(QFileDialog.ExistingFiles)
      if file_dialog.exec_():
        file_paths = file_dialog.selectedFiles()

        for file_path in file_paths:
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(self.frame.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.frame.setPixmap(pixmap)
        self.imgPath=file_path
        self.produitLabelPredit=Prediction.predict_image_class(self.imgPath)
        self.infoProduit=self.cnx.getProduit(self.produitLabelPredit)
        self.product_name_field.setText(self.infoProduit[0])
        self.product_quantity_field.setText(str(self.infoProduit[1]))
        self.product_price_field.setText(str(self.infoProduit[2]))     
    def reset_frame(self):
        # Réinitialiser le cadre en supprimant la photo affichée
        self.frame.clear()
        self.product_name_field.setText("")
        self.product_quantity_field.setText("")
        self.product_price_field.setText("")    
    def add_product_info(self):
        # Créer la frame pour afficher les informations du produit
       self.frame1 = QLabel(self)
       self.frame1.setGeometry(1100, self.height() // 2 - 250, 600, 600)
       self.frame1.setStyleSheet("background-color: rgba(213, 210, 210, 100); border: 2px solid #000000;")
       self.frame1.setAlignment(Qt.AlignCenter)

       # Ajouter une icône à la frame
       icon_label1 = QLabel(self.frame1)
       icon_label1.setGeometry(20, 40, 100, 100)  # Position et taille de l'icône
       icon_pixmap = QPixmap("./icones/produit.png")
       icon_pixmap_resized = icon_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Redimensionner l'icône
       icon_label1.setPixmap(icon_pixmap_resized)
       icon_label1.setStyleSheet("border: none; background-color: transparent;") 
       
       # Ajouter un champ de texte pour afficher le nom du produit
       self.product_name_field = QLineEdit(self.frame1)
       self.product_name_field.setReadOnly(True)
       self.product_name_field.setGeometry(200, 70, 200, 40)  # Position et taille du champ de texte
       self.product_name_field.setStyleSheet("background-color: rgba(213, 210, 210, 100); border: 2px solid #000000;")  # Style du champ de texte
       
       # Ajouter une icône à la frame
       icon_label2 = QLabel(self.frame1)
       icon_label2.setGeometry(20, 220, 100, 100)  # Position et taille de l'icône
       icon_pixmap = QPixmap("./icones/quantite.png")
       icon_pixmap_resized = icon_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Redimensionner l'icône
       icon_label2.setPixmap(icon_pixmap_resized)
       icon_label2.setStyleSheet("border: none; background-color: transparent;") 
       
       # Ajouter un champ de texte pour afficher le nom du produit
       self.product_quantity_field = QLineEdit(self.frame1)
       self.product_quantity_field.setReadOnly(True)
       self.product_quantity_field.setGeometry(200, 260, 200, 40)  # Position et taille du champ de texte
       self.product_quantity_field.setStyleSheet("background-color: rgba(213, 210, 210, 100); border: 2px solid #000000;")
       
       # Ajouter une icône à la frame
       icon_label3 = QLabel(self.frame1)
       icon_label3.setGeometry(20, 400, 100, 100)  # Position et taille de l'icône
       icon_pixmap = QPixmap("./icones/prix.png")
       icon_pixmap_resized = icon_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Redimensionner l'icône
       icon_label3.setPixmap(icon_pixmap_resized)
       icon_label3.setStyleSheet("border: none; background-color: transparent;") 
       
       # Ajouter un champ de texte pour afficher le nom du produit
       self.product_price_field = QLineEdit(self.frame1)
       self.product_price_field.setReadOnly(True)
       self.product_price_field.setGeometry(200, 450, 200, 40)  # Position et taille du champ de texte
       self.product_price_field.setStyleSheet("background-color: rgba(213, 210, 210, 100); border: 2px solid #000000;")

        
        

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
