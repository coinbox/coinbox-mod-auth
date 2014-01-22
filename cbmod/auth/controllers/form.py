import cbpos

from cbmod.auth.models import User, Role, Permission

from cbmod.base.controllers import FormController

class UsersFormController(FormController):
    cls = User
    
    def fields(self):
        return {"username": (cbpos.tr.auth._("Username"), ""),
                "role": (cbpos.tr.auth._("Role"), None),
                "permissions": (cbpos.tr.auth._("Permissions"), []),
                "hidden": (cbpos.tr.auth._("Show in Login Box"), False),
                "password_check": ("", False),
                "password1": (cbpos.tr.auth._("Password"), ""),
                "password2": (cbpos.tr.auth._("Confirm Password"), "")
                }
    
    def items(self):
        session = cbpos.database.session()
        return session.query(User)
    
    def canDeleteItem(self, item):
        from cbmod.auth.controllers import user
        return user.current != item
    
    def canEditItem(self, item):
        from cbmod.auth.controllers import user
        return user.current != item
    
    def canAddItem(self):
        return True
    
    def getDataFromItem(self, field, item):
        if field in ('username', 'role', 'hidden'):
            return getattr(item, field)
        elif field == 'permissions':
            return item.role.permissions if item.role is not None else []
        elif field in ('password1', 'password2'):
            return ""
        elif field == 'password_check':
            return False

class RolesFormController(FormController):
    cls = Role
    
    def fields(self):
        return {"name": (cbpos.tr.auth._("Name"), ""),
                "permissions": (cbpos.tr.auth._("Permissions"), []),
                }
    
    def items(self):
        session = cbpos.database.session()
        return session.query(Role)
    
    def canDeleteItem(self, item):
        from cbmod.auth.controllers import user
        return user.current.role != item
    
    def canEditItem(self, item):
        from cbmod.auth.controllers import user
        return user.current.role != item
    
    def canAddItem(self):
        return True

    def getDataFromItem(self, field, item):
        return getattr(item, field)

class PermissionsFormController(FormController):
    cls = Permission
    
    def fields(self):
        return {"name": (cbpos.tr.auth._("Name"), ""),
                "description": (cbpos.tr.auth._("Description"), ""),
                "menu_restrictions": (cbpos.tr.auth._("Menu Restrictions"), []),
                }
    
    def items(self):
        session = cbpos.database.session()
        return session.query(Permission)
    
    def canDeleteItem(self, item):
        return len(item.roles) == 0
    
    def canEditItem(self, item):
        return True
    
    def canAddItem(self):
        return True

    def getDataFromItem(self, field, item):
        return getattr(item, field)

class IndividualUserFormController(FormController):
    cls = User
    single = True
    
    def fields(self):
        return {"username": (cbpos.tr.auth._("Username"), ""),
                "role": (cbpos.tr.auth._("Role"), None),
                "password_check": ("", False),
                "password1": (cbpos.tr.auth._("Password"), ""),
                "password2": (cbpos.tr.auth._("Confirm Password"), "")
                }
    
    def item(self):
        from cbmod.auth.controllers import user
        return user.current
    
    def items(self):
        return []
    
    def canDeleteItem(self, item):
        return False
    
    def canEditItem(self, item):
        return True
    
    def canAddItem(self):
        return False
    
    def getDataFromItem(self, field, item):
        if field in ('username', 'role'):
            return getattr(item, field)
        elif field in ('password1', 'password2'):
            return ""
        elif field == 'password_check':
            return False
