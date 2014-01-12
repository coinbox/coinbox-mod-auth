from PySide import QtCore, QtGui

from sqlalchemy.orm import exc

import cbpos

from cbmod.auth.controllers import PermissionsFormController
from cbmod.auth.models import Permission, MenuRestriction

from cbmod.base.views import FormPage

class PermissionsPage(FormPage):
    controller = PermissionsFormController()
    
    def widgets(self):
        menu_restrictions = QtGui.QTreeWidget()
        menu_restrictions.setHeaderHidden(True)
        
        return (("name", QtGui.QLineEdit()),
                ("description", QtGui.QTextEdit()),
                ("menu_restrictions", menu_restrictions)
                )
    
    def getDataFromControl(self, field):
        if field == 'name':
            data = self.f[field].text()
        elif field == 'description':
            data = self.f[field].toPlainText()
        elif field == 'menu_restrictions':
            data = []
            for i in xrange(self.f[field].topLevelItemCount()):
                root = self.f[field].topLevelItem(i)
                for j in xrange(root.childCount()):
                    child = root.child(j)
                    if child.checkState(0) == QtCore.Qt.Checked:
                        mr = child.data(0, QtCore.Qt.UserRole+1)
                        data.append(mr)
        return (field, data)
    
    def setDataOnControl(self, field, data):
        if field in ('name', 'description'):
            self.f[field].setText(data)
        elif field == 'menu_restrictions':
            session = cbpos.database.session()
            restrictions = [(mr.root, mr.item) for mr in data]
            self.f[field].clear()
            for item in cbpos.menu.items:
                root = QtGui.QTreeWidgetItem(self.f[field], [item.label])
                root.setExpanded(True)
                for i in item.children:
                    child = QtGui.QTreeWidgetItem(root, [i.label])
                    try:
                        mr = session.query(MenuRestriction).filter_by(root=item.name, item=i.name).one()
                    except (exc.NoResultFound, exc.MultipleResultsFound) as e:
                        mr = MenuRestriction(root=item.name, item=i.name)
                    child.setData(0, QtCore.Qt.UserRole+1, mr)
                    if (item.name, i.name) in restrictions:
                        child.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        child.setCheckState(0, QtCore.Qt.Unchecked)
