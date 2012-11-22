from PySide import QtGui

import cbpos

from cbpos.mod.auth.controllers import UsersFormController
from cbpos.mod.auth.models import User, Role

from cbpos.mod.base.views import FormPage

class UsersPage(FormPage):
    controller = UsersFormController()
    
    def widgets(self):
        username = QtGui.QLineEdit()
        username.setEnabled(False)
        
        role = QtGui.QComboBox()
        role.setEditable(False)
        role.currentIndexChanged[int].connect(self.onRoleChanged)
        
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
                ("permissions", QtGui.QListWidget()),
                ("hidden", QtGui.QCheckBox("Is Hidden")),
                ("password_check", password_check),
                ("password1", password1),
                ("password2", password2)
                )
    
    def onCheckPassword(self):
        checked = self.f['password_check'].isChecked()
        self.f['password1'].setEnabled(checked)
        self.f['password2'].setEnabled(checked)
    
    def onRoleChanged(self):
        field, data = self.getDataFromControl('role')
        if data is not None:
            self.setDataOnControl('permissions', data.permissions)
        else:
            self.setDataOnControl('permissions', [])
    
    def getDataFromControl(self, field):
        if field == 'username':
            data = self.f[field].text()
        elif field == 'hidden':
            data = self.f[field].isChecked()
        elif field == 'role':
            selected_index = self.f[field].currentIndex()
            if selected_index == -1:
                data = None
            else:
                data = self.f[field].itemData(selected_index)
        elif field in ('password1', 'password2'):
            # TODO: validation
            data = self.f[field].text()
            field = 'password'
        elif field in ('permissions', 'password_check'):
            data = None
            field = None
        return (field, data)
    
    def setDataOnControl(self, field, data):
        if field == 'username':
            self.f[field].setText(data)
        elif field == 'hidden':
            self.f[field].setChecked(data)
        elif field == 'role':
            session = cbpos.database.session()
            items = session.query(Role.display, Role).all()
            self.f[field].clear()
            self.f[field].addItem("", None)
            for i, item in enumerate(items):
                self.f[field].addItem(*item)
                if item[1] == data:
                    self.f[field].setCurrentIndex(i+1) 
        elif field == 'permissions':
            self.f[field].clear()
            self.f[field].addItems([i.display for i in data])
        elif field in ('password1', 'password2'):
            self.f[field].setText(data)
        elif field == 'password_check':
            self.f[field].setChecked(data)
