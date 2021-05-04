import os
import sys
import platform
from PySide2 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
from music_player.player import *
from music_player.imagenes import rcc_version

system = platform.system()
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def hhmmss(ms):
    # s = 1000
    # m = 60000
    # h = 360000

    h, r = divmod(ms, 360000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d:%02d" % (h, m, s)) if h else("%d:%02d" % (m, s))

class myplayer(QtWidgets.QMainWindow):
    def __init__(self):
        super(myplayer, self).__init__()
        self.ui = Ui_musicplayer()
        self.ui.setupUi(self)
        self.setFixedSize(440, 460)
        self.ui.config.clicked.connect(self.menu_config)
        #******************#
        # play/pause
        #******************#
        self.ui.play_button.clicked.connect(self.play)
        self.onplay = 0
        self.iconpausa = QtGui.QIcon()
        self.iconpausa.addPixmap(QtGui.QPixmap(
            ":/neuron_music/img/pausa.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.iconplay = QtGui.QIcon()
        self.iconplay.addPixmap(QtGui.QPixmap(
            ":/neuron_music/img/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)

        #******************#
        # playlist
        #******************#
        self.player = QtMultimedia.QMediaPlayer()
        self.path = list()
        try:
            if system == "Windows":
                self.musicpath = os.listdir(CURRENT_DIR + r'\records')
                for i in self.musicpath:
                    self.path.append(CURRENT_DIR + r'\records'+"\\"+i)
            elif system == "Linux":
                self.musicpath = os.listdir(CURRENT_DIR+'/records')
                for i in self.musicpath:
                    self.path.append(CURRENT_DIR+'/records/'+i)
        except:
            pass
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        for i in self.path:
            self.playlist.addMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(i)))
        self.ui.next_button.clicked.connect(self.playlist.next)
        self.ui.back_button.clicked.connect(self.playlist.previous)
        #******************#
        # playlist elementos texto/imagen
        #******************#
        self.playlist.currentMediaChanged.connect(self.songChanged)
        #******************#
        # volumen
        #******************#
        self.player.setVolume(80)
        self.ui.control_volumen.setMinimum(0)
        self.ui.control_volumen.setMaximum(100)
        self.ui.control_volumen.setValue(80)
        self.ui.control_volumen.valueChanged.connect(self.player.setVolume)
        #******************#
        # volume hiden
        #******************#
        self.volumen_r_l = self.ui.control_volumen
        self.volumen_r_l.lower()
        self.vol_buttom = 0
        self.ui.img_volumen.mousePressEvent = self.hide_volumen
        #******************#
        # time
        #******************#
        self.ui.time_inicio.setStyleSheet('color:#ffffff;font-size:15px;')
        self.ui.time_final.setStyleSheet('color:#ffffff;font-size:15px;')
        self.ui.time_final.setFixedWidth(80)
        self.ui.slider_2.setValue(0)
        self.player.durationChanged.connect(self.cargar_duracion)
        self.player.positionChanged.connect(self.cargar_posicion)
        self.ui.slider_2.valueChanged.connect(self.player.setPosition)

#******************#
# metodos
#******************#
    def play(self):
        if self.onplay == 0:
            self.player.play()
            self.ui.play_button.setIcon(self.iconpausa)
            self.ui.play_button.setIconSize(QtCore.QSize(25, 25))
            self.onplay += 1
        elif self.onplay == 1:
            self.player.pause()
            self.ui.play_button.setIcon(self.iconplay)
            self.ui.play_button.setIconSize(QtCore.QSize(30, 30))
            self.onplay -= 1

    def songChanged(self, media):
        if not media.isNull():
            url = media.canonicalUrl()
            direccion = str(url.fileName())
            quitar_formato = direccion.split('.')
            nombre_cancion = quitar_formato[0]
            self.ui.cover.setScaledContents(True)
            self.ui.nombre_cancion.setText(nombre_cancion)
            if nombre_cancion == "02 Bitch, Don't Kill My Vibe":
                cover = QtGui.QPixmap(CURRENT_DIR+'/covers/kl.jpg')
                self.ui.cover.setPixmap(cover)
            elif nombre_cancion == "03-This Boy" or nombre_cancion == "04-It Won't Be Long" or nombre_cancion == "All I've Got To Do.mp3":
                cover = QtGui.QPixmap(CURRENT_DIR+'/covers/tb.jpg')
                self.ui.cover.setPixmap(cover)

    def cargar_duracion(self, duracion):

        self.ui.slider_2.setMaximum(duracion)

        if duracion >= 0:
            self.ui.time_final.setText(hhmmss(duracion))

    def cargar_posicion(self, posicion):
        if posicion >= 0:
            self.ui.time_inicio.setText(hhmmss(posicion))

        self.ui.slider_2.blockSignals(True)
        self.ui.slider_2.setValue(posicion)
        self.ui.slider_2.blockSignals(False)

    def hide_volumen(self, event):
        if self.vol_buttom == 0:
            self.ui.control_volumen.raise_()
            self.vol_buttom += 1
        elif self.vol_buttom == 1:
            self.ui.control_volumen.lower()
            self.vol_buttom -= 1

    def menu_config(self):
        pass

if __name__ == "__main__":
    app=QtWidgets.QApplication([])
    widget = myplayer()
    widget.show()
    app.exec_()
