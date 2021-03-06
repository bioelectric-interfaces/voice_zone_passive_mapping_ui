import enum
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QSizePolicy
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QBrush, QColor, QPalette, QRegion, QIcon
from PyQt5.QtCore import QRect, QRectF, QSize, pyqtSlot, pyqtSignal

from resources import resources

# remember to get property for background equal to color of parent widget. (for qss?)
class PlayerView(QWidget):

    invalidateLastRecord = pyqtSignal(name='invalidateLastRecord')

    class State(enum.Enum):
        Init = 0
        Paused = 1
        Playing = 2

    def __init__(self, viewmodel):
        super().__init__()

        self.state = PlayerView.State.Init

        uic.loadUi(r'views/player_view.ui', self)
        self.setWindowOpacity(1.0);
        self.setAutoFillBackground(True)
        pal = QPalette(QColor(14079702));
        self.setPalette(pal)

        self.setStyleSheet("""QPushButton {
                            background: rgb(205, 205, 205);
                            border: 1px solid #828282;
                            border-radius : 8px;
                            font-family: \"IntelOne Display Light\"; /* Text font family */
                            font-size: 12pt; /* Text font size */
                        }
                        QPushButton:hover {
                            background: rgba(144, 200, 246, 155);
                            border-color: #828282;
                            border-width: 1px;
                            border-radius : 8px;
                            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));
                        }
                        QPushButton:pressed,
                        QPushButton:checked
                        {
                            background: rgba(144, 200, 246, 155);
                            border-color: #828282;
                            border-style: solid;
                            border-width: 1px;
                            border-radius : 8px;
                            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));
                        }
                        """
                    )

        self.layout().setRowStretch(0, 2)
        self.layout().setRowStretch(1, 5)
        self.layout().setRowStretch(2, 2)

        self.playButton.setIcon(QIcon(r':/logos/play.png'))

        self.viewmodel = viewmodel
        self.viewmodel.playing.connect(self.handlePlaying)
        self.viewmodel.paused.connect(self.handlePaused)
        self.viewmodel.endOfStream.connect(self.handleEndOfStream)

    @pyqtSlot(bool)
    def on_playButton_clicked(self):
        if self.state != PlayerView.State.Playing:
            self.viewmodel.handlePlayButton()
        else:
            # multiple times called pause -> leads to bug
            self.viewmodel.handlePauseButton()

    @pyqtSlot(bool)
    def on_stopButton_clicked(self):
        #These 2 are extra, they will be done on "endOfStream" handler
        #self.playButton.setIcon(QIcon(r':/logos/play.png'))
        #self.state = PlayerView.State.Init
        self.viewmodel.handleStopButton()

    @pyqtSlot(bool)
    def on_invalidateButton_clicked(self):
        print("player: invalidate clicked!")
        self.invalidateLastRecord.emit()
        self.viewmodel.handleInvalidateButton()

    @pyqtSlot(bool)
    def on_actionsButton_clicked(self):
        print("player: actions clicked!")
        #self.restore()

    @pyqtSlot(bool)
    def on_objectsButton_clicked(self):
        print("player: objects clicked!")
        #self.restore()

    @pyqtSlot()
    def handlePlaying(self):
        print("player: playing")
        self.playButton.setIcon(QIcon(r':/logos/pause.png'))
        self.state = PlayerView.State.Playing

    @pyqtSlot()
    def handlePaused(self):
        print("player: pause")
        self.playButton.setIcon(QIcon(r':/logos/play.png'))
        self.state = PlayerView.State.Paused

    @pyqtSlot()
    def handleEndOfStream(self):
        print("player: end of stream")
        self.playButton.setIcon(QIcon(r':/logos/play.png'))
        self.state = PlayerView.State.Init

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(QColor(8553090), 0.5)
        painter.setPen(pen)
        brush = QBrush(QColor(15395562))
        painter.setBrush(brush)

        path = QPainterPath()
        rect = QRectF(self.rect())
        rect.adjust(2, 2, -2, -2)
        path.addRoundedRect(rect, 35, 35)

        painter.fillPath(path, painter.brush())
        painter.strokePath(path, painter.pen())

