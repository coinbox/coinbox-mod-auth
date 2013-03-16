from pydispatch import dispatcher

import cbpos
from cbpos.modules import BaseModuleLoader

import logging
logger = logging.getLogger(__name__)

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
            ('common', 'Manage own user information', [mr('administration', 'user')]),
            ('users', 'Manage users, permissions and roles.', [mr('users', 'users'), mr('users', 'roles'), mr('users', 'permissions')]),
            ('sales', 'Manage sales: tickets and orders.', [mr('main', 'sales'), mr('main', 'debts')]),
            ('cash', 'Manage cash register: close cash and manage payments.', []),
            ('stock', 'Manage products and categories in stock.', [mr('stock', 'products'), mr('stock', 'categories'), mr('stock', 'stock-diary')]),
            ('customers', 'Manage customers.', [mr('customers', 'customers'), mr('customers', 'groups')]),
            ('reports', 'View and print reports.', [mr('reports', 'sales'), mr('reports', 'customers'), mr('reports', 'stock'), mr('reports', 'stock-diary'), mr('reports', 'users')]),
            ('system', 'Edit system settings.', [mr('system', 'configuration'), mr('system', 'currencies')])]
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
        from cbpos.interface import MenuRoot, MenuItem
        from cbpos.mod.auth.views import UsersPage, RolesPage, PermissionsPage, IndividualUserPage
        
        return [[MenuRoot('users',
                          label=cbpos.tr.auth._('Users'),
                          icon=cbpos.res.auth('images/menu-root-users.png'),
                          rel=-2,
                          priority=3
                          )],
                [MenuItem('users', parent='users',
                          label=cbpos.tr.auth._('Users'),
                          icon=cbpos.res.auth('images/menu-users.png'),
                          page=UsersPage
                          ),
                 MenuItem('roles', parent='users',
                          label=cbpos.tr.auth._('Roles'),
                          icon=cbpos.res.auth('images/menu-roles.png'),
                          page=RolesPage
                          ),
                 MenuItem('permissions', parent='users',
                          label=cbpos.tr.auth._('Permissions'),
                          icon=cbpos.res.auth('images/menu-permissions.png'),
                          page=PermissionsPage
                          ),
                 MenuItem('indivdual-user', parent='administration',
                          label=cbpos.tr.auth._('User'),
                          icon=cbpos.res.auth('images/menu-user.png'),
                          page=IndividualUserPage
                          )
                 ]
                ]

    
    def actions(self):
        """
        Returns a list of Action objects.
        """
        from cbpos.interface import Action
        return [Action('logout',
                       label=cbpos.tr.auth._('Logout'),
                       icon=cbpos.res.auth('images/menu-user.png'),
                       shortcut='Ctrl+L',
                       signal='action-logout'
                       ),
                Action('clockin',
                       label=cbpos.tr.auth._('Clock-in'),
                       icon=cbpos.res.auth('images/clock_in.png'),
                       shortcut='Ctrl+I',
                       signal='action-clockin'
                       ),
                Action('clockout',
                       label=cbpos.tr.auth._('Clock-out'),
                       icon=cbpos.res.auth('images/clock_out.png'),
                       shortcut='Ctrl+O',
                       signal='action-clockout'
                       )
                ]

    def init(self):
        dispatcher.connect(self.do_post_init, signal='ui-post-init', sender='app')
        
        return True

    def do_post_init(self):
        # Extend the main window, for the clocking feature
        from cbpos.mod.auth.views import ClockingMainWindow
        cbpos.ui.extend_default(ClockingMainWindow)
        
        # Load the login dialog before anything else
        from PySide import QtGui
        from cbpos.mod.auth.views.dialogs import LoginDialog
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
            QtGui.QMessageBox.information(QtGui.QWidget(), 'Login', message, QtGui.QMessageBox.Ok)
            return True

    def config_panels(self):
        from cbpos.mod.auth.views import UserConfigPage 
        return [UserConfigPage]
