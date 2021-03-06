from PySide import QtGui

import cbpos

class UserConfigPage(QtGui.QWidget):
    label = 'User'
    
    def __init__(self):
        super(UserConfigPage, self).__init__()
        
        self.allow_empty_password = QtGui.QCheckBox()
        
        form = QtGui.QFormLayout()
        form.setSpacing(10)
        
        form.addRow('Allow empty passwords', self.allow_empty_passwords)
        
        self.setLayout(form)

    def populate(self):
        allow = bool(cbpos.config['mod.auth', 'allow_empty_passwords'])
        self.allow_empty_password.setChecked(allow)
    
    def update(self):
        checked = self.allow_empty_password.isChecked()
        cbpos.config['mod.auth', 'allow_empty_passwords'] = checked
