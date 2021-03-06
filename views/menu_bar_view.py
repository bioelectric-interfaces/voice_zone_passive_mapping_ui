import enum

from models.preview_model import PreviewModel
from viewmodels.configure_script_viewmodel import ConfigureScriptViewModel

from viewmodels.configure_viewmodel import ConfigureViewModel

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QMenu, QAction
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QBrush, QColor, QPalette
from PyQt5.QtCore import QRectF, pyqtSlot

from configure_view import ConfigureView

class MenuBarView(QWidget):
    def __init__(self, toolConfig, viewmodel):
        super().__init__()

        self.toolConfig = toolConfig

        self.setWindowOpacity(1.0);
        self.setAutoFillBackground(True)
        pal = QPalette(QColor(14079702))
        self.setPalette(pal)

        horizontalLayout = QHBoxLayout()
        # fix by background element 
        self.fileMenuButton = QPushButton("File")
        self.fileMenuButton.setMinimumSize(80, 20)
        self.fileMenuButton.setStyleSheet("""
            QPushButton {
                border-style: solid;
                border-width: 0px;
            }
            QPushButton:hover {
                background: rgb(144, 200, 246);
                border-style: solid;
                border-color: #828282;
                border-width: 0px;
            }
            QPushButton:pressed {
                border-style: solid;
                border-color: #828282;
                border-width: 1px;
            }
            """)
        menu = QMenu()
        menu.setStyleSheet(
            """QMenu {
                border-style: solid;
                border-color: #828282;
                border-width: 1px;
            }
           }""")
        configure = QAction("Configure experiment", self)
        configure.setShortcut("Ctrl+E")
        configure.triggered.connect(self.configureExperiment)
        menu.addAction(configure)
        self.fileMenuButton.setMenu(menu)
        horizontalLayout.addWidget(self.fileMenuButton, 0, QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.closeButton = QPushButton("X")
        self.closeButton.setMinimumSize(20, 20)
        self.closeButton.setStyleSheet("""
            QPushButton {
                border-style: solid;
                border-width: 0px;
            }
            QPushButton:hover {
                background: rgb(144, 200, 246);
                border-style: solid;
                border-color: #828282;
                border-width: 0px;
            }
            QPushButton:pressed {
                border-style: solid;
                border-color: #828282;
                border-width: 1px;
            }
            """)
        horizontalLayout.addWidget(self.closeButton, 1, QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

        horizontalLayout.setContentsMargins(20, 2, 10, 2)
        self.setLayout(horizontalLayout)

        self.closeButton.clicked.connect(self.onCloseButtonClicked)

        self.viewmodel = viewmodel

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
        path.addRoundedRect(rect, 10, 10)

        painter.fillPath(path, painter.brush())
        painter.strokePath(path, painter.pen())

    @pyqtSlot()
    def configureExperiment(self):
        print("conflgure clicked!")
        self.viewmodel.stopScript()

        actVM = ConfigureScriptViewModel(PreviewModel(), self.viewmodel.getModel())
        objVM = ConfigureScriptViewModel(PreviewModel(), self.viewmodel.getModel())
        self.window = ConfigureView(self.toolConfig, ConfigureViewModel(self.viewmodel.getModel()), actVM, objVM)
        self.window.show()

    @pyqtSlot()
    def onCloseButtonClicked(self):
        print("close clicked!")
        self.parent().close()
