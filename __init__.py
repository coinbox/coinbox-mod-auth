from pydispatch import dispatcher

import cbpos
from cbpos.modules import BaseModuleLoader

class ModuleLoader(BaseModuleLoader):
    dependencies = ('base',)
    config = [['mod.auth', {'allow_empty_passwords': '1'}]]
    name = 'Authentication Support'

    def load(self):
        from cbpos.mod.auth.models import Permission, MenuRestriction, Role, User
        return [Permission, MenuRestriction, Role, User]

    def test(self):
        from cbpos.mod.auth.models import Permission, MenuRestriction, Role, User
    
        mr = lambda root, item: MenuRestriction(root=root, item=item)
    
        permissions_text = [
            ('common', 'Manage own user information', [mr('Administration', 'User')]),
            ('users', 'Manage users, permissions and roles.', [mr('Users', 'Users'), mr('Users', 'Roles'), mr('Users', 'Permissions')]),
            ('sales', 'Manage sales: tickets and orders.', [mr('Main', 'Sales'), mr('Main', 'Debts')]),
            ('cash', 'Manage cash register: close cash and manage payments.', []),
            ('stock', 'Manage products and categories in stock.', [mr('Stock', 'Products'), mr('Stock', 'Categories'), mr('Stock', 'Stock Diary')]),
            ('customers', 'Manage customers.', [mr('Customers', 'Customers'), mr('Customers', 'Groups')]),
            ('reports', 'View and print reports.', [mr('Reports', 'Sales'), mr('Reports', 'Customers'), mr('Reports', 'Stock'), mr('Reports', 'Stock Diary'), mr('Reports', 'Users')]),
            ('system', 'Edit system settings.', [mr('System', 'Configuration'), mr('System', 'Currencies')])]
        permissions = [Permission(name=p[0], description=p[1], menu_restrictions=p[2]) for p in permissions_text]
    
        admin_permissions = map(lambda p: permissions[p], range(len(permissions)))
        manager_permissions = map(lambda p: permissions[p], [0, 2, 3, 4, 5, 6])
        employee_permissions = map(lambda p: permissions[p], [0, 2])
    
        admin_role = Role(name='admin', permissions=admin_permissions)
        manager_role = Role(name='manager', permissions=manager_permissions)
        employee_role = Role(name='employee', permissions=employee_permissions)
    
        super_user = User(username='Super', password='super', hidden=True, super=True)
        admin_user = User(username='Admin', password='admin', role=admin_role)
        manager_user = User(username='Manager', password='manager', role=manager_role)
        employee_user = User(username='Employee', password='employee', role=employee_role)
    
        session = cbpos.database.session()
        session.add(super_user)
        session.add(admin_user)
        session.add(manager_user)
        session.add(employee_user)
        session.commit()

    def menu(self):
        from cbpos.mod.auth.views import UsersPage, RolesPage, PermissionsPage, IndividualUserPage
        
        return [[{'label': 'Users', 'rel': -2, 'priority': 3, 'image': cbpos.res.auth('images/menu-root-users.png')}],
                [{'parent': 'Users', 'label': 'Users', 'page': UsersPage, 'image': cbpos.res.auth('images/menu-users.png')},
                 {'parent': 'Users', 'label': 'Roles', 'page': RolesPage, 'image': cbpos.res.auth('images/menu-roles.png')},
                 {'parent': 'Users', 'label': 'Permissions', 'page': PermissionsPage, 'image': cbpos.res.auth('images/menu-permissions.png')},
                 {'parent': 'Administration', 'label': 'User', 'page': IndividualUserPage, 'image': cbpos.res.auth('images/menu-user.png')}]]

    
    def actions(self):
        """
        Returns the module actions for the Actions toolbar.
        Format for each action:
        {'label':'TheLabel', 'callback': the_callback, 'icon': 'the_icon.png', 'shortcut':'Ctrl+L'} 
        """
        return [ 
            {'label':'Logout', 'callback': self.do_load_login, 'icon': cbpos.res.auth('images/menu-user.png'), 'shortcut':'Ctrl+L'}
        ]


    def init(self):
        dispatcher.connect(self.do_load_login, signal='ui-post-init', sender='app')
        return True

    def do_load_login(self):
        from PySide import QtGui
        from cbpos.mod.auth.views.dialogs import LoginDialog
        # TODO: change this!
        from cbpos.mod.auth.controllers import user
        from cbpos.mod.auth.models import User
        
        session = cbpos.database.session()
        user_count = session.query(User).count()
        if user_count > 0:
            login = LoginDialog()
            cbpos.ui.window = login
            return True
        else:
            user.current = User(username='_superuser_', password='_superuser_', hidden=True, super=True)
            session.add(user.current)
            session.commit()
            message = '''No user found. Creating Super User.
Create a normal user as soon as possible.
Username: _superuser_
Password: _superuser_
'''
            QtGui.QMessageBox.information(self, 'Login', message, QtGui.QMessageBox.Ok)
            return True

    def config_panels(self):
        from cbpos.mod.auth.views import UserConfigPage 
        return [UserConfigPage]
