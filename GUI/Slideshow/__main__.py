from PyQt5.QtWidgets import QApplication

from GUI.slideshow import Slideshow

Qapp = QApplication([])

app = Slideshow()

Qapp.exec_()
