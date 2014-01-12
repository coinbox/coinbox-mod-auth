from PySide import QtCore, QtGui

import cbpos

from cbmod.auth.controllers import IndividualUserFormController
from cbmod.auth.models import User, Role

from cbmod.base.controllers import ValidationError
from cbmod.base.views import FormPage

class IndividualUserPage(FormPage):
    controller = IndividualUserFormController()
    single = True
    
    def widgets(self):
        username = QtGui.QLineEdit()
        username.setReadOnly(True)
        
        role = QtGui.QLineEdit()
        role.setReadOnly(True)
        
        password1 = QtGui.QLineEdit()
        password1.setEchoMode(QtGui.QLineEdit.Password)
        password1.setEnabled(False)
        
        password2 = QtGui.QLineEdit()
        password2.setEchoMode(QtGui.QLineEdit.Password)
        password2.setEnabled(False)

        password_check = QtGui.QCheckBox("Change Password")
        password_check.stateChanged.connect(self.onCheckPassword)

        return (("username", username),
                ("role", role),
                ("password_check", password_check),
                ("password1", password1),
                ("password2", password2)
                )
    
    def onCheckPassword(self):
        checked = self.f['password_check'].isChecked()
        self.f['password1'].setEnabled(checked)
        self.f['password2'].setEnabled(checked)
    
    def getDataFromControl(self, field):
        if field == 'username':
            data = self.f[field].text()
        elif field == 'role':
            field, data = None, None
        elif field in ('password1', 'password2'):
            if self.f['password_check'].isChecked():
                password1 = self.f['password1'].text()
                password2 = self.f['password2'].text()
                if password1 != password2:
                    raise ValidationError(cbpos.tr.auth._("Passwords do not match."))
                data = password1
                field = 'password'
            else:
                field, data = None, None
        elif field == 'password_check':
            field, data = None, None
        return (field, data)
    
    def setDataOnControl(self, field, data):
        if field == 'username':
            self.f[field].setText(data)
        elif field == 'role':
            if data == None:
                self.f[field].setText('')
            else:
                self.f[field].setText(data.display) 
        elif field == 'permissions':
            self.f[field].clear()
            self.f[field].addItems([i.display for i in data])
        elif field in ('password1', 'password2'):
            self.f[field].setText(data)
        elif field == 'password_check':
            self.f[field].setChecked(data)
