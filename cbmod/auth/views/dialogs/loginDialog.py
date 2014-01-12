from PySide import QtGui, QtSvg, QtCore

import cbpos

logger = cbpos.get_logger(__name__)

import datetime

from cbmod.auth.controllers import user
from cbmod.auth.models import User

from cbmod.auth.views.dialogs.loginpanel import LoginPanel

from pydispatch import dispatcher

class LoginDialog(QtSvg.QSvgWidget):
    def __init__(self):
        super(LoginDialog, self).__init__()
        self.load(cbpos.res.auth("images/login-background2.svg"))
        self.setWindowTitle(cbpos.tr.auth._('Login'))
        
        #Login Panel
        #self.showFullScreen() #To center the login widget on screen, and getting space to show it right.
        self.loginPanel = LoginPanel(self, cbpos.res.auth("images/login.svg"))
        self.loginPanel.setSize(350, 350)
        self.loginPanel.setLoginCallback(self.onOkButton)
        self.loginPanel.setClockingCallback(self.onClocking)
        self.loginPanel.setLoginAndClockinCallback(self.onLoginAndClockin)
        self.loginPanel.editUsername.currentIndexChanged.connect(self.loginPanel.editPassword.setFocus)
        self.loginPanel.editPassword.returnPressed.connect(self.onOkButton)
        self.loginPanel.btnExit.clicked.connect(self.onExitButton)
        #Populate users
        self.populate()
        #Launch login-panel
        QtCore.QTimer.singleShot(300, self.loginPanel.showPanel )
    
    def populate(self):
        session = cbpos.database.session()
        users = session.query(User).filter_by(hidden=False)
        for user in users:
            self.loginPanel.editUsername.addItem(user.display, user)

    def onOkButton(self):
        username = self.loginPanel.getUserName()
        password = self.loginPanel.getPassword()
        
        if user.login(username, password):
            self.loginPanel.hidePanel()
            QtCore.QTimer.singleShot(1000, self.closeAll)
        else:
            self.loginPanel.setError('<html><head/><body><p><span style=" font-size:14pt; font-weight:600; font-style:italic; color:#ff0856;">%s</span></p></body></html>'%cbpos.tr.auth._('Invalid username or password.') )
            self.loginPanel.editPassword.setFocus()
            self.loginPanel.editPassword.selectAll()

    def onClocking(self):
        username = self.loginPanel.getUserName()
        password = self.loginPanel.getPassword()
        
        u = user.check(username, password)
        if u:
            if user.clockin(u):
                date_time = datetime.datetime.now()
                ok_msg = cbpos.tr.auth._('Clock in sucessful.\nYour in time is %s'%date_time)
                self.loginPanel.setMessage(ok_msg)
            else:
                ok_msg = cbpos.tr.auth._('Clock in UNSUCCESSFUL')
                self.loginPanel.setError(ok_msg)
        else:
            self.loginPanel.setError('<html><head/><body><p><span style=" font-size:14pt; font-weight:600; font-style:italic; color:#ff0856;">%s</span></p></body></html>'%cbpos.tr.auth._('Invalid username or password.') )
            self.loginPanel.editPassword.setFocus()
            self.loginPanel.editPassword.selectAll()

    def onLoginAndClockin(self):
        username = self.loginPanel.getUserName()
        password = self.loginPanel.getPassword()
        
        if user.login(username, password):
            if user.clockin():
                self.loginPanel.hidePanel()
                QtCore.QTimer.singleShot(1000, self.closeAll)
            else:
                ok_msg = cbpos.tr.auth._('Clock in UNSUCCESSFUL')
                self.loginPanel.setError(ok_msg)
        else:
            self.loginPanel.setError('<html><head/><body><p><span style=" font-size:14pt; font-weight:600; font-style:italic; color:#ff0856;">%s</span></p></body></html>'%cbpos.tr.auth._('Invalid username or password.') )
            self.loginPanel.editPassword.setFocus()
            self.loginPanel.editPassword.selectAll()

    def resizeEvent(self, event):
        self.loginPanel.reposition()

    def closeAll(self):
        self.close()
        cbpos.ui.show_next()
        #MCH Comment: Why now showing the main ui window first, then login window on top of the main (like a dialog of the main)?
    
    def onExitButton(self):
        user.current = None
        self.close()
        cbpos.terminate()
