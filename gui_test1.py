from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication([]) # necessary to create **one* QApp per file
label = QLabel('Hello World!')
label.show()

app.exec_() # Run until closed
