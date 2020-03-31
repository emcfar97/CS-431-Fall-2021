from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from os.path import exists

from . import *

class Slideshow(QMainWindow):
    
    def __init__(self, parent):
        
        super().__init__()
        self.parent = parent
        self.configure_gui()
        self.create_widgets()
    
    def configure_gui(self):
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        resolution = self.parent.size()

        self.setGeometry(
            0, 0, resolution.width(),  resolution.height()
            )
        self.setStyleSheet('background: black')
          
    def create_widgets(self):
        
        self.label = QLabel(self)
        self.video = videoPlayer(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.stack.addWidget(self.label)
        self.stack.addWidget(self.video)
        
        self.setMouseTracking(True)
        self.label.setMouseTracking(True)
        self.video.setMouseTracking(True)
        
        self.timer = QTimer()
        self.setCursor(Qt.BlankCursor)
        self.timer.timeout.connect(
            lambda: self.setCursor(Qt.BlankCursor)
            )               

    def update(self, gallery, index):

        self.gallery = gallery
        self.index = index
        self.move(0)
        self.showFullScreen()

    def move(self, delta):
        
        self.index = (self.index + delta) % len(self.gallery)
        if not exists(self.gallery[self.index][0]):
            del self.gallery[self.index]
        self.show_image(self.gallery[self.index][0])
    
    def show_image(self, path):
        
        width, height = self.width(), self.height()
        
        if path.endswith(('.jpg', '.jpeg', '.png')):
            
            self.label.setMovie(QMovie())
            pixmap = QPixmap(path).scaled(
                width, height, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation
                )
            self.label.setPixmap(pixmap)
        
        elif path.endswith('.gif'):
            
            self.label.setPixmap(QPixmap())
            wid, hei = Image.open(path).size
            ratio = wid / hei
     
            dimensions = (
                (width, width / ratio) 
                if (width / ratio) <= height else 
                (height * ratio, height)
                )
            
            movie = QMovie(path)
            movie.setScaledSize(QSize(*dimensions))
            self.label.setMovie(movie)
            movie.start()
        
        elif path.endswith(('.webm', '.mp4')):
            
            self.label.setMovie(QMovie())
            self.label.setPixmap(QPixmap())
            self.video.update(path)
            self.stack.setCurrentIndex(1)
        
    def keyPressEvent(self, sender):

        key_press = sender.key()
            
        if key_press == Qt.Key_Right: self.move(+1)
        elif key_press == Qt.Key_Left: self.move(-1)        
        elif key_press == Qt.Key_Escape: 
            
            self.video.player.pause()
            self.video.player.stop()
            self.hide()
            
    def mouseMoveEvent(self, sender):
        
        self.timer.stop()
        self.setCursor(Qt.ArrowCursor)
        self.timer.start(1500)
    
class videoPlayer(QVideoWidget):

    def __init__(self, parent):
        
        super().__init__(parent)
        self.replay = True
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self)
        self.player.stateChanged.connect(self.mediaStatusChanged)
        self.player.setVolume(50) 

    def update(self, path):

        self.player.setMedia(
            QMediaContent(QUrl.fromLocalFile(path))
            )
        self.player.play()
        self.replay = True
        self.setFocus()

    def keyPressEvent(self, sender):
        
        key_press = sender.key()
        if key_press == Qt.Key_Space:
            
            status = self.player.state()
            if status == QMediaPlayer.PlayingState: self.player.pause()
            elif status == QMediaPlayer.PausedState: self.player.play()
            
        elif key_press == Qt.Key_Home: self.player.setPosition(0)
            
        elif key_press == Qt.Key_End: self.player.setPosition(0)  
            
        elif key_press == Qt.Key_Period:
            
            self.player.setPosition(self.player.position() + 5000)
            
        elif key_press == Qt.Key_Comma:
            
            self.player.setPosition(self.player.position() - 5000)
        
        elif key_press == Qt.Key_Up:
            
            self.player.setVolume(self.player.volume() + 10)
            
        elif key_press == Qt.Key_Down:
            
            self.player.setVolume(self.player.volume() - 10)
    
        elif key_press == Qt.Key_Right:
            
            self.replay = False
            self.player.stop()
            self.parent().setCurrentIndex(0)
            self.parent().parent().move(+1)
        
        elif key_press == Qt.Key_Left:
            
            self.replay = False
            self.player.stop()
            self.parent().setCurrentIndex(0)
            self.parent().parent().move(-1) 
        
        elif key_press == Qt.Key_Escape: 
            
            self.replay = False
            self.player.stop()
            self.hide()

    def mediaStatusChanged(self, status):
        
        if self.replay and status == QMediaPlayer.StoppedState: 
            self.player.play()
    
    def wheelEvent(self, sender):
        
        if self.player.isAudioAvailable():
            
            delta = sender.angleDelta().y() // 12
            self.player.setVolume(self.player.volume() + delta)           
