from PySide import QtGui, QtSvg

import cbpos

from sqlalchemy.orm import exc

from cbpos.mod.auth.controllers import user
from cbpos.mod.auth.models import User

#from pos.modules.user.windows import UserCatalog

from cmWidgets.cmLoginWindow import *

class LoginDialog(QtSvg.QSvgWidget):
    def __init__(self):
        super(LoginDialog, self).__init__()
        self.load("cmWidgets/images/login-background2.svg")
        self.setWindowTitle(cbpos.tr.auth._('Login'))
        
        #MCH Login Dialog
        self.showFullScreen() #To center the login widget on screen, and getting space to show it right.
        self.loginWindow = cmLoginWindow(self, "cmWidgets/images/about.svg")
        self.loginWindow.setSize(350, 350)
        self.loginWindow.btnLogin.clicked.connect(self.onOkButton)
        self.loginWindow.editUsername.returnPressed.connect(self.loginWindow.editPassword.setFocus)
        self.loginWindow.editPassword.returnPressed.connect(self.onOkButton)
        self.loginWindow.btnExit.clicked.connect(self.onExitButton)
        #Launch login-dialog
        QtCore.QTimer.singleShot(300, self.loginWindow.showDialog )
    
    def populate(self):
        session = cbpos.database.session()
        users = session.query(User.display, User).filter_by(hidden=False).all()
        for user in users:
            self.user.addItem(*user)
    
    def onOkButton(self):
        username = self.loginWindow.getUserName() #self.user.currentText()
        password = self.loginWindow.getPassword() #self.password.text()
        
        if user.login(username, password):
            self.loginWindow.hideDialog()
            QtCore.QTimer.singleShot(1000, self.closeAll)
        else:
            #Jad: your text was not translated!
            self.loginWindow.setError('<html><head/><body><p><span style=" font-size:14pt; font-weight:600; font-style:italic; color:#ff0856;">%s</span><span style=" font-size:14pt; font-style:italic; color:#ff0856;">%s</span></p></body></html>'%(cbpos.tr.auth._('Invalid '),cbpos.tr.auth._('username or password.')) )
            self.loginWindow.editPassword.setFocus()
            self.loginWindow.editPassword.selectAll()

    def closeAll(self):
        self.close()
        cbpos.ui.show_default()
        #MCH Comment: Why now showing the main ui window first, then login window on top of the main (like a dialog of the main)?
    
    def onExitButton(self):
        user.current = None
        self.close()
    
    """
    def OnF3Command(self, event):
        dlg = HiddenUserLoginDialog(None)
        dlg.ShowModal()
        if dlg.success:
            user.current = dlg.user
            self.Close()
    """

"""
class HiddenUserLoginDialog(wx.Dialog):
    def __init_ctrls(self):
        self.panel = wx.Panel(self, -1)

        # User
        self.usernameLbl = wx.StaticText(self.panel, -1, label='Username')
        self.usernameTxt = wx.TextCtrl(self.panel, -1)
        
        # Password
        self.passwordLbl = wx.StaticText(self.panel, -1, label='Password')
        self.passwordTxt = wx.TextCtrl(self.panel, -1, style=wx.TE_PASSWORD)

        # Controls
        self.okBtn = wx.Button(self, wx.ID_OK, label='OK')
        self.okBtn.Bind(wx.EVT_BUTTON, self.OnOkButton)
        self.cancelBtn = wx.Button(self, wx.ID_CANCEL, label='Cancel')
    
    def __init_sizers(self):
        self.panelSizer = wx.GridSizer(hgap=5, vgap=5, cols=2)
        self.panelSizer.Add(self.usernameLbl, 0, flag=wx.ALL | wx.ALIGN_LEFT)
        self.panelSizer.Add(self.usernameTxt, 1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT)
        self.panelSizer.Add(self.passwordLbl, 0, flag=wx.ALL | wx.ALIGN_LEFT)
        self.panelSizer.Add(self.passwordTxt, 1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT)
        self.panel.SetSizerAndFit(self.panelSizer)

        self.controlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.okBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL)
        self.controlSizer.Add(self.cancelBtn, 0, flag=wx.CENTER | wx.ALL)
        self.controlSizer.Add(wx.Size(0, 0), 1, flag=wx.EXPAND | wx.ALL) 
        
        self.mainSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.mainSizer.Add(self.panel, 1, border=10, flag=wx.ALL | wx.EXPAND)
        self.mainSizer.AddSizer(self.controlSizer, 0, border=10, flag=wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.EXPAND)
        self.SetSizerAndFit(self.mainSizer)
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, title='Login')

        self.__init_ctrls()
        self.__init_sizers()
        
        self.success = False
        self.user = None
    
    def OnOkButton(self, event):
        username = self.usernameTxt.GetValue()
        password = self.passwordTxt.GetValue()
        session = pos.database.session()
        try:
            self.user = session.query(User).filter(User.username == username).one()
        except exc.NoResultFound, exc.MultipleResultsFound:
            pass
        if self.user is not None and self.user.login(password):
            self.success = True
            event.Skip()
        else:
            wx.MessageBox('Invalid username/password.', 'Error', style=wx.OK | wx.ICON_EXCLAMATION)
            self.usernameTxt.SetFocus()
            self.usernameTxt.SelectAll()

class LoginValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.user = None

    Clone = lambda self: LoginValidator()

    def Validate(self, parent):
        password = parent.passwordTxt.GetValue()
        u = parent.userList.GetValue()
        
        password_valid = True
        username_valid = u is not None
        
        if not username_valid:
            wx.MessageBox(message='Select a user', caption='Failure',
                                style=wx.OK, parent=None)
            return False
        elif not password_valid:
            wx.MessageBox(message='Invalid password', caption='Failure',
                                style=wx.OK, parent=None)
            return False
        else:
            if not u.login(password):
                wx.MessageBox(message='Wrong username/password', caption='Failure',
                                    style=wx.OK, parent=None)
                return False
            else:
                self.user = u
                return True

    def TransferToWindow(self):
        user.current = None
        return True

    def TransferFromWindow(self):
        user.current = self.user
        return True
"""