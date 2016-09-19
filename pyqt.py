import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox,QDesktopWidget,QMainWindow,QAction,qApp,QTextEdit,QLabel,QHBoxLayout,QVBoxLayout
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication

class example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        #set the main widget's tooltip 
        # QToolTip.setFont(QFont('Sansserif',9))
        # self.setToolTip('this is a <b>QWidget</b> widget')

        #set the button
        # btn = QPushButton('Button',self)
        # btn.move(150,250)
        # btn.resize(btn.sizeHint())
        # btn.clicked.connect(QCoreApplication.instance().quit)
        # btn.setToolTip('this is a <b>QPushButton</b> button')

        #set the label
        # label1 = QLabel('label1',self)
        # label1.move(15,100)
        # label2 = QLabel('label2',self)
        # label2.move(35,200)
        #set the textEdit
        # texteEdit = QTextEdit()
        # self.setCentralWidget(texteEdit)
        #set the window center
        self.resize(550,350)
        self.setWindowTitle('Hello,PyQt5')
        self.setWindowIcon(QIcon('./resources/Icon.png'))
        
        #set the status bar
        # self.statusBar().showMessage('Ready')

        #set the menubar
        exitAction = QAction(QIcon('./resources/exit.jpg'),'&Exit',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit the application')
        exitAction.triggered.connect(qApp.quit)
        
        # menuBar = self.menuBar()
        # fileBar = menuBar.addMenu('&File')
        # fileBar.addAction(exitAction)

        #set the toolbar
        # self.addToolBar('Exit').addAction(exitAction)

        #set the Layout
        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')
        hbox = QHBoxLayout()
        hbox.stretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.stretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        self.center()
        self.show()
    
    def closeEvent(self,event):
        reply = QMessageBox.question(self,'Message',"Sure to quit",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = example()
    sys.exit(app.exec_())
