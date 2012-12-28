#
#   Copyright (C) 2011-2013 by the Coinbox team.
#
#   Miguel Chavez Gamboa <miguel@coinboxpos.org>
#
#   License: MIT
#
#   Permission is hereby granted, free of charge, to any person obtaining
#   a copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the 
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
#   THE SOFTWARE.
#


from PySide import QtGui, QtCore, QtSvg


import cbpos

class LoginPanel(QtSvg.QSvgWidget):
    def __init__(self, parent, File):
        super(LoginPanel, self).__init__(parent)

        #Gui components
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(15, 5, 5, 15)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(60, 60, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lblUsername = QtGui.QLabel(self)
        self.lblUsername.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lblUsername.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblUsername.setObjectName("lblUsername")
        self.gridLayout.addWidget(self.lblUsername, 0, 1, 1, 1)
        self.editUsername = QtGui.QComboBox(self)
        self.editUsername.setEditable(True)
        self.editUsername.setMaximumSize(QtCore.QSize(300, 16777215))
        self.editUsername.setMinimumSize(QtCore.QSize(170, 48))
        self.editUsername.setFixedHeight(48)
        self.editUsername.setObjectName("editUsername")
        self.gridLayout.addWidget(self.editUsername, 0, 2, 1, 1)
        self.lblPassword = QtGui.QLabel(self)
        self.lblPassword.setMaximumSize(QtCore.QSize(300, 16777215))
        self.lblPassword.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblPassword.setObjectName("lblPassword")
        self.gridLayout.addWidget(QtGui.QLabel(""), 1,1,1,1)
        self.gridLayout.addWidget(self.lblPassword, 2, 1, 1, 1)
        self.editPassword = QtGui.QLineEdit(self)
        self.editPassword.setMaximumSize(QtCore.QSize(300, 16777215))
        self.editPassword.setMinimumSize(QtCore.QSize(170, 48))
        self.editPassword.setFixedHeight(48)
        self.editPassword.setObjectName("editPassword")
        self.gridLayout.addWidget(self.editPassword, 2, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtGui.QSpacerItem(100, 100, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.btnExit = QtGui.QPushButton(self)
        self.btnExit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btnExit.setObjectName("btnExit")
        self.btnExit.setFixedHeight(48)
        self.horizontalLayout.addWidget(self.btnExit)
        self.btnLogin = QtGui.QPushButton(self)
        self.btnLogin.setMinimumSize(QtCore.QSize(150, 0))
        self.btnLogin.setMaximumSize(QtCore.QSize(200, 16777215))
        self.btnLogin.setDefault(True)
        self.btnLogin.setObjectName("btnLogin")
        self.btnLogin.setFixedHeight(48)
        
        self.clockAction = QtGui.QAction(QtGui.QIcon(cbpos.res.auth('images/clock_in.png')), cbpos.tr.auth._("Clock in"), self)
        self.loginAction = QtGui.QAction(QtGui.QIcon(cbpos.res.auth('images/menu-users.png')), cbpos.tr.auth._("Log in"), self)
        self.loginMenu = QtGui.QMenu(self)
        self.loginMenu.addAction(self.clockAction)
        self.loginMenu.addAction(self.loginAction)
        self.loginMenu.setDefaultAction(self.loginAction)
        self.btnLogin.setMenu(self.loginMenu)

        self.horizontalLayout.addWidget(self.btnLogin)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lblError = QtGui.QLabel("")
        self.lblError.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.lblError)
        #spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        #self.verticalLayout.addItem(spacerItem5)


        self.editPassword.setEchoMode(QtGui.QLineEdit.Password)
        #Enter texts
        self.lblUsername.setText("<b><i>" + cbpos.tr.auth._("Username:") + "</i></b>")
        self.lblPassword.setText("<b><i>" + cbpos.tr.auth._("Password:") + "</i></b>")
        self.lblUsername.setStyleSheet("color:white")
        self.lblPassword.setStyleSheet("color:white")
        self.editPassword.setPlaceholderText(cbpos.tr.auth._("Enter your password"))
        self.btnExit.setText(cbpos.tr.auth._("Exit"))
        self.btnLogin.setText(cbpos.tr.auth._("Log in"))
        
        #setting member properties
        self.parent = parent
        self.maxHeight = 0
        self.maxWidth = 0
        #self.animType = aType #NOT USED FOR NOW. Will implement later...
        self.setMinimumHeight(100)
        self.setFixedSize(0,0)
        self.setMaxHeight(300)
        self.setMaxWidth(300)
        self.animRate = 2500 #default animation speed (half second rate).
        self.shakeTimeToLive = 400 #default shake time..
        self.par = False
        self.parTimes = 0

        #The timer
        self.shakeTimer = QtCore.QTimer(self)
        self.shakeTimer.setInterval(20)
        self.shakeTimer.timeout.connect(self.shakeIt)

        #Setting gui properties
        self.load(File)

        #animation
        self.timeLine  = QtCore.QTimeLine(self.animRate, self)
        self.timeLine.finished.connect(self.onAnimationFinished)
        self.timeLine.frameChanged[int].connect(self.animate)

    def getUserName(self):
        return self.editUsername.currentText()

    def getPassword(self):
        return self.editPassword.text()

    def setLoginCallback(self, callback):
        self.loginAction.triggered.connect(callback)
        self.btnLogin.clicked.connect(callback)

    def setClockingCallback(self, callback):
        self.clockAction.triggered.connect(callback)

    def setFile(self, File):
        self.load(File)

    def setMaxHeight(self, m):
        self.setMaximumHeight(m)
        self.maxHeight = m

    def setMaxWidth(self,m):
        self.setMaximumWidth(m)
        self.maxWidth = m

    def setSize(self, w, h):
        self.setMaxWidth(w)
        self.setMaxHeight(h)
        #print 'Setting Size: %sx%s | Parent %sx%s'%(w,h, self.parent.geometry().width(),self.parent.geometry().height())
    
    def hidePanel(self):
        self.editPassword.clear()
        self.editUsername.clear()

        maj,minor,rel = QtCore.__version_info__ 
        maj = int(maj); minor=int(minor); rel = int(rel)
        if maj >= 4 and minor >= 6:
            self.timeLine.setEasingCurve(QtCore.QEasingCurve.InExpo)
            self.timeLine.toggleDirection() #reverse!
            self.timeLine.start()
        else:
            self.hide()

        #NOTE: Anyone using this class must be aware of THIS, the aboutBox parent must have a disableUi/actions & enableUi/actions Methods.
        #self.parent.enableUi()
        #self.parent.enableActions()

    def onAnimationFinished(self):
        if self.timeLine.direction() == QtCore.QTimeLine.Backward :
            self.close()
            self.shakeTimer.stop()

    def setError(self, text):
        self.lblError.setText(text)
        self.shake()
        QtCore.QTimer.singleShot(5000, self.clearError)

    def setMessage(self, text):
        self.lblError.setText(text)
        QtCore.QTimer.singleShot(5000, self.clearError)

    def clearError(self):
        self.lblError.setText("")

    def shake(self):
        self.shakeTimer.start()
        if self.shakeTimeToLive > 0 :
            QtCore.QTimer.singleShot(self.shakeTimeToLive, self.stopShaking)
        

    def stopShaking(self):
        self.shakeTimer.stop()
        initX = (self.parent.geometry().width()/2) - (self.maxWidth/2)
        initY = (self.parent.geometry().height()/2) - (self.maxHeight/2)
        self.setGeometry(initX, initY, self.geometry().width(), self.geometry().height())

    def shakeIt(self):
        #print 'shaking...  par:%s  parTimes:%s'%(self.par, self.parTimes)
        if self.par:
            if self.parTimes < 10 :
                if self.parTimes % 2 == 0 :
                    self.setGeometry(self.geometry().x()-5, self.geometry().y()+5, self.geometry().width(), self.geometry().height())
                else:
                    self.setGeometry(self.geometry().x()+5, self.geometry().y()+5, self.geometry().width(), self.geometry().height())
            else:
                self.parTimes = 0
            self.parTimes += 1
        else:
            if self.parTimes < 10 :
                if  self.parTimes % 2 == 0 :
                    self.setGeometry(self.geometry().x()+5, self.geometry().y()-5, self.geometry().width(), self.geometry().height())
                else:
                    self.setGeometry(self.geometry().x()-5, self.geometry().y()-5, self.geometry().width(), self.geometry().height())
            else:
                self.parTimes = 0
        #change direction
        self.par = not self.par


    def animate(self, step):
        #This just animates from up to down. Maybe later port the other animations.
        windowGeom = self.parent.geometry()
        midPointX = (windowGeom.width()/2)
        midPointY = (windowGeom.height()/2)
        newY = 0
        newX = 0
        dRect = QtCore.QRect()

        if (midPointX-(self.maxWidth/2)) < 0 :
            newX = 0
        else:
            newX = midPointX - self.maxWidth/2

        dRect.setX(newX)
        dRect.setY(step)
        dRect.setWidth(self.maxWidth)
        dRect.setHeight(self.maxHeight)
        self.setGeometry(dRect)
        self.setFixedHeight(self.maxHeight)
        self.setFixedWidth(self.maxWidth)


    def showPanel(self):
        self.setGeometry(-1000,-1000,0,0)
        self.show()
        maxStep = 0
        minStep = 0

        maxStep = (self.parent.geometry().height()/2)-(self.maxHeight/2)
        minStep = -self.maxHeight

        #NOTE: We assume everybody has qt 4.6+.. how to check it? (in c++ -> with #if QT_VERSION >= 0x040600)
        maj,minor,rel = QtCore.__version_info__ 
        maj = int(maj); minor=int(minor); rel = int(rel)
        if maj >= 4 and minor >= 6:
            self.timeLine.setEasingCurve(QtCore.QEasingCurve.OutBounce)
            self.timeLine.setFrameRange(minStep,maxStep)
            self.timeLine.setDirection(QtCore.QTimeLine.Forward)
            self.timeLine.start()
        else:
            self.setGeometry(QtCore.QRect((self.parent.geometry().width()/2)- self.maxWidth/2, 0, self.maxWidth, self.maxHeight))
            self.show()

        #NOTE: Anyone using this class must be aware of THIS, the aboutBox parent must have a disableUi/actions & enableUi/actions Methods.
        #self.parent.disableUi()
        #self.parent.disableActions()

        self.editUsername.setFocus()

