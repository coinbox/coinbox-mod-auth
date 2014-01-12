from PySide import QtCore, QtGui

import cbpos

from cbmod.auth.controllers import RolesFormController
from cbmod.auth.models import Role, Permission

from cbmod.base.views import FormPage

class RolesPage(FormPage):
    controller = RolesFormController()
    
    def widgets(self):
        permissions = QtGui.QTreeWidget()
        permissions.setHeaderHidden(True)
        
        return (("name", QtGui.QLineEdit()),
                ("permissions", permissions)
                )
    
    def getDataFromControl(self, field):
        if field == 'name':
            data = self.f[field].text()
        elif field == 'permissions':
            data = []
            for i in xrange(self.f[field].topLevelItemCount()):
                root = self.f[field].topLevelItem(i)
                if root.checkState(0) == QtCore.Qt.Checked:
                    item = root.data(0, QtCore.Qt.UserRole+1)
                    data.append(item)
        return (field, data)
    
    def setDataOnControl(self, field, data):
        if field == 'name':
            self.f[field].setText(data)
        elif field == 'permissions':
            session = cbpos.database.session()
            self.f[field].clear()
            for item in session.query(Permission):
                root = QtGui.QTreeWidgetItem(self.f[field], [item.display])
                root.setData(0, QtCore.Qt.UserRole+1, item)
                if item in data:
                    root.setCheckState(0, QtCore.Qt.Checked)
                else:
                    root.setCheckState(0, QtCore.Qt.Unchecked)
