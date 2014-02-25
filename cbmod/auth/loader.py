from pydispatch import dispatcher

import cbpos
logger = cbpos.get_logger(__name__)

from cbpos.modules import BaseModuleLoader

class ModuleLoader(BaseModuleLoader):
    def load_models(self):
        from cbmod.auth.models import Permission, MenuRestriction, Role, User
        return [Permission, MenuRestriction, Role, User]

    def test_models(self):
        from cbmod.auth.models import Permission, MenuRestriction, Role, User
    
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
        from cbmod.auth.views import UsersPage, RolesPage, PermissionsPage, IndividualUserPage
        
        return [[MenuRoot('users',
                          label=cbpos.tr.auth_('Users'),
                          icon=cbpos.res.auth('images/menu-root-users.png'),
                          rel=-2,
                          priority=3
                          )],
                [MenuItem('users', parent='users',
                          label=cbpos.tr.auth_('Users'),
                          icon=cbpos.res.auth('images/menu-users.png'),
                          page=UsersPage
                          ),
                 MenuItem('roles', parent='users',
                          label=cbpos.tr.auth_('Roles'),
                          icon=cbpos.res.auth('images/menu-roles.png'),
                          page=RolesPage
                          ),
                 MenuItem('permissions', parent='users',
                          label=cbpos.tr.auth_('Permissions'),
                          icon=cbpos.res.auth('images/menu-permissions.png'),
                          page=PermissionsPage
                          ),
                 MenuItem('indivdual-user', parent='administration',
                          label=cbpos.tr.auth_('User'),
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
                       label=cbpos.tr.auth_('Logout'),
                       icon=cbpos.res.auth('images/menu-user.png'),
                       shortcut='Ctrl+L',
                       signal='action-logout'
                       ),
                Action('clockin',
                       label=cbpos.tr.auth_('Clock-in'),
                       icon=cbpos.res.auth('images/clock_in.png'),
                       shortcut='Ctrl+I',
                       signal='action-clockin'
                       ),
                Action('clockout',
                       label=cbpos.tr.auth_('Clock-out'),
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
        from cbmod.auth.views import ClockingMainWindow
        cbpos.ui.extend_default_main_window(ClockingMainWindow)
        
        # Load the login dialog before anything else
        from PySide import QtGui
        from cbmod.auth.views.dialogs import LoginDialog
        
        login = LoginDialog()
        cbpos.ui.chain_window(login, cbpos.ui.PRIORITY_FIRST_HIGH)
        return True

    def config_panels(self):
        from cbmod.auth.views import UserConfigPage 
        return [UserConfigPage]
