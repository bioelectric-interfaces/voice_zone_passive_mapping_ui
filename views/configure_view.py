from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QStyleOption, QStyle
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QBrush, QColor
from PyQt5.QtCore import QRectF, QSize, pyqtSlot

from frameless_widget import FramelessWidget
from configure_tab import ConfigureTab

class ConfigureView(FramelessWidget):
    def __init__(self, toolConfig, viewmodel, actionsViewModel, objectsViewModel):
        super().__init__()

        self.toolConfig = toolConfig

        self.state = FramelessWidget.State.Init

        uic.loadUi(r'views/configure_view.ui', self)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
        self.autoFillBackground()
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
        self.setWindowOpacity(1.0)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setBorderMargin(5)
        self.setCornerMargin(20)
        self.resize(1000, 600)

        self.cfgGridLayout.setSpacing(20)
        self.cfgGridLayout.setVerticalSpacing(20)
        self.cfgGridLayout.setContentsMargins(15, 15, 15, 15)

        self.actionsViewModel = actionsViewModel
        self.objectsViewModel = objectsViewModel
        self.actionsTab = ConfigureTab(toolConfig, self.actionsViewModel, 0, "Actions")
        self.objectsTab = ConfigureTab(toolConfig, self.objectsViewModel, 1, "Objects")
        self.actionsTab.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.objectsTab.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # QtCore.Qt.AlignmentFlag.AlignCenter) ?
        self.actionsTab.setMinimumSize(QSize(1000, 600))
        self.objectsTab.setMinimumSize(QSize(1000, 600))
        self.cfgGridLayout.addWidget(self.objectsTab, 0, 0)
        self.cfgGridLayout.addWidget(self.actionsTab, 0, 0)

        self.tabsLayout = QHBoxLayout()
        switchers = [QPushButton(), QPushButton()]
        switcherSS = """ QPushButton {
                            background-color: transparent;
                            border: 0px solid black;
                            border-radius : 0px;
                         }"""

        for i in range(0, len(switchers)):
            switcher = switchers[i]
            switcher.setMinimumSize(100, 25)
            switcher.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            switcher.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
            switcher.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
            switcher.setStyleSheet(switcherSS)
            self.tabsLayout.addWidget(switcher, i, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.tabsLayout.setSpacing(0)
        self.tabsLayout.setContentsMargins(2, 5, 0, 0)
        self.cfgGridLayout.addLayout(self.tabsLayout, 0, 0)

        self.actionsButton, self.objectsButton = switchers
        self.actionsButton.clicked.connect(self.onActionsButtonClicked)
        self.objectsButton.clicked.connect(self.onObjectsButtonClicked)

        applyCancelButtonSS = """QWidget { border-radius : 5px; }
                                 QPushButton {
                                     background: #EAEAEA;
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
                                     border-color: black;
                                     border-width: 1px;
                                     border-radius : 0px;
                                 }"""

        self.applyButton.setStyleSheet(applyCancelButtonSS)
        self.cancelButton.setStyleSheet(applyCancelButtonSS)
        #self.applyCancelLayout.setAlignment(self.applyButton, QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
        self.applyButton.setMinimumSize(100, 23)
        #self.applyCancelLayout.setAlignment(self.cancelButton, QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.cancelButton.setMinimumSize(100, 23)

        self.viewmodel = viewmodel

    @pyqtSlot(bool)
    def onActionsButtonClicked(self):
        self.cfgGridLayout.removeWidget(self.actionsTab)
        self.actionsTab.setParent(None)
        self.cfgGridLayout.removeWidget(self.objectsTab)
        self.objectsTab.setParent(None)
        self.cfgGridLayout.removeItem(self.tabsLayout)
        self.actionsButton.setParent(None)
        self.objectsButton.setParent(None)

        self.cfgGridLayout.addWidget(self.objectsTab, 0, 0)
        self.cfgGridLayout.addWidget(self.actionsTab, 0, 0)
        self.cfgGridLayout.addLayout(self.tabsLayout, 0, 0)

    @pyqtSlot(bool)
    def onObjectsButtonClicked(self):
        self.cfgGridLayout.removeWidget(self.actionsTab)
        self.actionsTab.setParent(None)
        self.cfgGridLayout.removeWidget(self.objectsTab)
        self.objectsTab.setParent(None)
        self.cfgGridLayout.removeItem(self.tabsLayout)
        self.actionsButton.setParent(None)
        self.objectsButton.setParent(None)

        self.cfgGridLayout.addWidget(self.actionsTab, 0, 0)
        self.cfgGridLayout.addWidget(self.objectsTab, 0, 0)
        self.cfgGridLayout.addLayout(self.tabsLayout, 0, 0)

    @pyqtSlot(bool)
    def on_applyButton_clicked(self):
        toolCfgPictures = getattr(self.toolConfig.Stimuli, 'Action' + 'Pictures')
        toolCfgPictures.Time = self.actionsViewModel.getTimeout()
        self.toolConfig.Presentation.Duration.Picture = self.actionsViewModel.getTimeout()
        self.toolConfig.sync()

        self.viewmodel.handleApplyButton(self.actionsViewModel.getPictures(), self.actionsViewModel.getLabels(),
                                         self.actionsViewModel.getTimeout())
        self.actionsViewModel.cleanPreview()
        self.close()

    @pyqtSlot(bool)
    def on_cancelButton_clicked(self):
        self.viewmodel.handleCancelButton()
        self.actionsViewModel.cleanPreview()
        self.close()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

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

        # rect.adjust(12, 12, -12, -12)
        # innerPath = QPainterPath()
        # innerPath.addRoundedRect(QRectF(rect), 35, 35)
        # painter.fillPath(innerPath, QBrush(QColor(11579568)))
        # painter.strokePath(innerPath, QPen(QColor(8553090), 0.5))

        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.viewmodel.handleCancelButton()
            self.actionsViewModel.cleanPreview()
            self.close()