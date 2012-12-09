from PySide import QtGui, QtSvg, QtCore

import cbpos

from cbpos.mod.auth.controllers import user
from cbpos.mod.auth.models import User

#from pos.modules.user.windows import UserCatalog

from cbpos.mod.auth.views.dialogs.loginpanel import LoginPanel

class LoginDialog(QtSvg.QSvgWidget):
    def __init__(self):
        super(LoginDialog, self).__init__()
        self.load(cbpos.res.auth("images/login-background2.svg"))
        self.setWindowTitle(cbpos.tr.auth._('Login'))
        
        #Login Panel
        self.showFullScreen() #To center the login widget on screen, and getting space to show it right.
        self.loginPanel = LoginPanel(self, cbpos.res.auth("images/login.svg"))
        self.loginPanel.setSize(350, 350)
        self.loginPanel.btnLogin.clicked.connect(self.onOkButton)
        self.loginPanel.editUsername.currentIndexChanged.connect(self.loginPanel.editPassword.setFocus)
        self.loginPanel.editPassword.returnPressed.connect(self.onOkButton)
        self.loginPanel.btnExit.clicked.connect(self.onExitButton)
        #Populate users
        self.populate()
        #Launch login-panel
        QtCore.QTimer.singleShot(300, self.loginPanel.showPanel )
    
    def populate(self):
        session = cbpos.database.session()
        users = session.query(User.display, User).filter_by(hidden=False).all()
        for user in users:
            self.loginPanel.editUsername.addItem(*user)
    
    def onOkButton(self):
        username = self.loginPanel.getUserName()
        password = self.loginPanel.getPassword()
        
        if user.login(username, password):
            self.loginPanel.hidePanel()
            QtCore.QTimer.singleShot(1000, self.closeAll)
        else:
            #Jad: your text was not translated!
            self.loginPanel.setError('<html><head/><body><p><span style=" font-size:14pt; font-weight:600; font-style:italic; color:#ff0856;">%s</span></p></body></html>'%cbpos.tr.auth._('Invalid username or password.') )
            self.loginPanel.editPassword.setFocus()
            self.loginPanel.editPassword.selectAll()

    def closeAll(self):
        self.close()
        cbpos.ui.show_default()
        #MCH Comment: Why now showing the main ui window first, then login window on top of the main (like a dialog of the main)?
    
    def onExitButton(self):
        user.current = None
        self.close()
