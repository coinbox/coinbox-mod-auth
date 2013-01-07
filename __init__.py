from pydispatch import dispatcher

import cbpos
from cbpos.modules import BaseModuleLoader

import logging
logger = logging.getLogger(__name__)

class ModuleLoader(BaseModuleLoader):
    dependencies = ('base',)
    config = [['mod.auth', {'allow_empty_passwords': '1', 'secret_key': ''}]]
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
            {'label':cbpos.tr.auth._('Logout'), 'callback': self.do_load_login, 'icon': cbpos.res.auth('images/menu-user.png'), 'shortcut':'Ctrl+L'},
            {'label':cbpos.tr.auth._('Clock-in'), 'callback': self.do_load_clock_in, 'icon': cbpos.res.auth('images/clock_in.png'), 'shortcut':'Ctrl+I'},
            {'label':cbpos.tr.auth._('Clock-out'), 'callback': self.do_load_clock_out, 'icon': cbpos.res.auth('images/clock_out.png'), 'shortcut':'Ctrl+O'}
        ]


    def init(self):
        from cbpos.mod.auth.controllers import user
        try:
            assert user.secret_key, 'Secret key is not set!'
        except:
            logger.warning('Secret key is damaged or not set!')
            return False
        dispatcher.connect(self.do_load_login, signal='ui-post-init', sender='app')
        dispatcher.connect(self.do_clocking, signal='do-clocking', sender=dispatcher.Any)
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
            QtGui.QMessageBox.information(QtGui.QWidget(), 'Login', message, QtGui.QMessageBox.Ok)
            return True

    def config_panels(self):
        from cbpos.mod.auth.views import UserConfigPage 
        return [UserConfigPage]

    def do_load_clock_in(self):
        """
        Loads the Clock-in dialog.
        """
        #Here we just send a signal to open the clocking panel. We just need to wait for the proper signal to arraive again.
        dispatcher.send(signal='do-show-clockin-panel', sender='auth', isIn=True)

    def do_load_clock_out(self):
        """
        Loads the Clock-out dialog.
        """
        #Here we just send a signal to open the clocking panel. We just need to wait for the proper signal to arraive again.
        dispatcher.send(signal='do-show-clockout-panel', sender='auth', isIn=False)


    def do_clocking(self, sender, usern, passw, isIn):
        """
        This does the authentication for the user, and creates the entry for the clock-in at the database.
        """
        from cbpos.mod.auth.controllers import user
        from cbpos.mod.auth.models import User, Clock
        import datetime

        session = cbpos.database.session()

        if user.login(usern, passw):
            date_time = datetime.datetime.now()
            the_user  = session.query(User).filter_by(username=usern).first()
            ok_msg = ""
            if isIn:
                #create the new row.
                clockcard = Clock(user=the_user, date_time_in=date_time, date_time_out=date_time)
                session.add(clockcard)
                session.commit()
                ok_msg = cbpos.tr.auth._('Clock in sucessful.\nYour in time is %s'%date_time)
            else:
                #Look for the last row for the user, which must have an out equal to the in.
                #In most cases, there will be only one row, but in some cases may be more due to someone forgetting the clock out.
                clockcard = session.query(Clock).filter_by(user=the_user).filter(Clock.date_time_in==Clock.date_time_out)
                #in cases where there are more than one, we need to know which to apply the changes.
                if clockcard.count() > 1:
                    #What to do really? Apply to the last one?
                    clockcard = clockcard.order_by("id DESC").first() #here we find the last one (ordering by id in descending order)
                else:
                    clockcard = clockcard.order_by("id DESC").first()

                try:
                    clockcard.date_time_out = date_time
                    session.commit()
                    ok_msg = cbpos.tr.auth._('Clock out sucessful.\nYour in time is %s'%date_time)
                except Exception as e:
                    session.rollback()
                    ok_msg = cbpos.tr.auth._('Clock out UNSUCESSFUL')
                    logger.debug("Error on saving clock out for user %s. Error is: %s"%(usern, e))


            dispatcher.send(signal='do-hide-clockin-panel', sender='auth', msg=ok_msg)
        else:
            error_msg = '<html><head/><body><p><span style=" font-size:14pt; font-weight:600; font-style:italic; color:#ff0856;">%s</span></p></body></html>'%cbpos.tr.auth._('Invalid username or password.') 
            #Send the signal for error
            dispatcher.send(signal='do-show-error-on-clock-in', sender='auth', msg=error_msg)
