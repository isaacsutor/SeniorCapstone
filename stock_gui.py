import sys
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QAction, qApp, QMenu, QLabel, QPushButton, QHBoxLayout, \
    QVBoxLayout, QWidget, QFrame, QSplitter, QStyleFactory
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# DO the things
class Example(QWidget): #QMainWindow

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # exitAct = QAction(QIcon('exitpic.png'), ' &Exit', self)
        # exitAct.setShortcut('Ctrl+Q')
        # exitAct.setStatusTip('Exit application')
        # exitAct.triggered.connect(qApp.quit)

        # self.statusbar = self.statusBar()
        # self.statusbar.showMessage('Ready')

        # menubar = self.menuBar()

        # fileMenu = menubar.addMenu(' &File')
        # fileMenu.addAction(exitAct)

        # impMenu = QMenu('Import', self)
        # impAct = QAction('Import mail', self)
        # impMenu.addAction(impAct)

        # newAct = QAction('New', self)
        # fileMenu.addAction(newAct)
        # fileMenu.addMenu(impMenu)

        # viewMenu = menubar.addMenu('View')
        # viewStatAct = QAction('View statusbar', self, checkable=True)
        # viewStatAct.setStatusTip('View statusbar')
        # viewStatAct.setChecked(True)
        # viewStatAct.triggered.connect(self.toggleMenu)

        # viewMenu.addAction(viewStatAct)

        # self.setGeometry(300, 300, 250, 150)
        # self.setWindowTitle('Statusbar')
        # self.show()

        hbox = QHBoxLayout(self)

        topleft = QFrame(self)
        topleft.setFrameShape(QFrame.StyledPanel)

        topright = QFrame(self)
        topright.setFrameShape(QFrame.StyledPanel)

        bottom = QFrame(self)
        bottom.setFrameShape(QFrame.StyledPanel)

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")
        topright.addWidget(okButton)
        topleft.addWidget(cancelButton)
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(topleft)
        splitter1.addWidget(topright)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)

        # okButton = QPushButton("OK")
        # cancelButton = QPushButton("Cancel")
        # hbox = QHBoxLayout()
        # hbox.addStretch(1)
        # hbox.addWidget(okButton)
        # hbox.addWidget(cancelButton)

        # vbox = QVBoxLayout()
        # vbox.addStretch(1)
        # vbox.addLayout(hbox)

        # self.setLayout(vbox)

        # self.setGeometry(300, 300, 300, 150)
        # self.setWindowTitle('Buttons')
        # self.show()
        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QSplitter')
        self.show()

    def toggleMenu(self, state):
        if state:
            self.statusbar.show()
        else:
            self.statusbar.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

