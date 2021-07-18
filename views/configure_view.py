import enum
from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QWidget, QPushButton, QTextEdit, QSizePolicy, QGridLayout, QMenu, QStyleOption, QStyle, QFileDialog
from PyQt6.QtGui import QPainter, QPainterPath, QPen, QBrush, QColor, QPalette, QRegion, QIcon, QAction
from PyQt6.QtCore import QRect, QRectF, QLineF, QPointF, QSize, pyqtSlot

import json
import ntpath

from frameless_widget import FramelessWidget

class ConfigureView(FramelessWidget):
    def __init__(self, viewmodel):
        super().__init__()

        self.state = FramelessWidget.State.Init

        uic.loadUi(r'C:\Users\apronina\Syncplicity\Science\Markov_for_passive_ECC_of_voice_zones\voice_zone_passive_mapping\views\configure_view.ui', self)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.autoFillBackground()
        self.setWindowFlags(QtCore.Qt.WindowFlags.Window)
        self.setWindowOpacity(1.0)
        self.setWindowFlags(QtCore.Qt.WindowFlags.FramelessWindowHint)
        self.setBorderMargin(5)
        self.setCornerMargin(20)
        self.resize(600, 400)

        self.layout().setSpacing(20)
        self.layout().setVerticalSpacing(20)
        self.layout().setContentsMargins(35, 35, 35, 35)

        #"background-color: #FAFAFA; /* background color */"
        self.setStyleSheet("""QWidget { border-radius : 5px; }
                              QPushButton {
                                  border: 1px solid black;
                                  border-radius : 0px;
                              }
                              QPushButton:hover {
                                  background: rgb(144, 200, 246);
                                  border-width: 0px;
                                  border-radius : 0px;
                              }
                              QPushButton:pressed {
                                  border-style: solid;
                                  border-color: #828282;
                                  border-width: 1px;
                                  border-radius : 0px;
                              }
                              QLabel {
                                  color: black; /* text color */}
                              QLabel#label_3 {
                                  font-family: \"Century Gothic\"; /* Text font family */
                                  font-size: 10.5pt; /* Text font size */}
                              QLabel#label_4 {
                                  font-family: \"Century Gothic\"; /* Text font family */
                                  font-size: 10.5pt; /* Text font size */}
                              QLabel#label {
                                  padding-left: 15px;
                                  padding-right: 15px;
                                  border-radius: 5px; }
                              QLabel#label_2 {
                                  padding-left: 15px;
                                  padding-right: 15px;
                                  border-radius: 5px; }"""
                           )

        self.viewmodel = viewmodel
        self.actionsPictures = []
        self.actionsLabels = []
        self.actionsTimeout = 0
        self.objectsPictures = []
        self.objectsLabels = []
        self.objectsTimeout = 0

    def browseClicked(self, spinBox, listWidget, mTimeout, mPictures, mLabels):
        config_file_path = QFileDialog.getOpenFileName(self, 'Open file', '/home', '*.json')[0]
        config = None

        if config_file_path == '':
            return
        else:
            listWidget.clear()

        with open(config_file_path, 'r') as config_file:
            config = json.load(config_file)

        assert(config)

        timeout = config['timeout']
        spinBox.setValue(timeout)
        mTimeout = timeout

        images = config['images']
        for key, value in images.items():
            mPictures.append(key)
            mLabels.append(value)
            listWidget.addItem(ntpath.basename(key) + ' - ' + value)

    @pyqtSlot(bool)
    def on_browseActions_clicked(self):
        self.browseClicked(self.actionsTimeoutSpinBox, self.actionsList,
                           self.actionsTimeout, self.actionsPictures, self.actionsLabels)

    @pyqtSlot(bool)
    def on_browseObjects_clicked(self):
        self.browseClicked(self.objectsTimeoutSpinBox, self.objectsList,
                           self.objectsTimeout, self.objectsPictures, self.objectsLabels)

    @pyqtSlot(bool)
    def on_applyButton_clicked(self):
        self.actionsTimeout = self.actionsTimeoutSpinBox.value()
        self.viewmodel.handleApplyButton(self.actionsPictures, self.actionsLabels, self.actionsTimeout)
        self.close()

    @pyqtSlot(bool)
    def on_cancelButton_clicked(self):
        self.close()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHints.Antialiasing)

        pen = QPen(QColor(8553090), 1)
        cursorShape = self.cursor().shape()
        if cursorShape == QtCore.Qt.CursorShape.SizeHorCursor or \
           cursorShape == QtCore.Qt.CursorShape.SizeVerCursor or \
           cursorShape == QtCore.Qt.CursorShape.SizeFDiagCursor or \
           cursorShape == QtCore.Qt.CursorShape.SizeBDiagCursor or \
           self.state == FramelessWidget.State.Resizing:
           pen = QPen(QColor(8553000), 5)
        brush = QBrush(QColor(14079702))

        path = QPainterPath()
        rect = QRectF(self.rect())
        rect.adjust(2, 2, -2, -2)
        path.addRoundedRect(QRectF(rect), 35, 35)
        #it might be needed to clip region for mouse events.
        #painter.setClipPath(path)

        painter.fillPath(path, brush)
        painter.strokePath(path, pen)

        rect.adjust(12, 12, -12, -12)
        innerPath = QPainterPath()
        innerPath.addRoundedRect(QRectF(rect), 35, 35)
        painter.fillPath(innerPath, QBrush(QColor(15395562)))
        painter.strokePath(innerPath, QPen(QColor(8553090), 0.5))

        painter.setPen(QPen(QColor(16448250), 4))
        painter.drawLine(QLineF(QPointF(rect.width() / 2 + 19, rect.top() + 20),
                                QPointF(rect.width() / 2 + 19, rect.bottom() - 50)))

        painter.setPen(QPen(QColor(7697781), 0.5))
        painter.drawLine(QLineF(QPointF(rect.width() / 2 + 19, rect.top() + 20),
                                QPointF(rect.width() / 2 + 19, rect.bottom() - 50)))

        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)

    def keyPressEvent(self, event):
        if event.keyCombination().key() == QtCore.Qt.Key.Key_Escape:
            self.close()
