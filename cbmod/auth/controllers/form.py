import cbpos

from cbmod.auth.models import User, Role, Permission

from cbmod.base.controllers import FormController

class UsersFormController(FormController):
    cls = User
    
    def fields(self):
        return {"username": (cbpos.tr.auth_("Username"), ""),
                "role": (cbpos.tr.auth_("Role"), None),
                "permissions": (cbpos.tr.auth_("Permissions"), []),
                "hidden": (cbpos.tr.auth_("Show in Login Box"), False),
                "password_check": ("", False),
                "password1": (cbpos.tr.auth_("Password"), ""),
                "password2": (cbpos.tr.auth_("Confirm Password"), "")
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
        return {"name": (cbpos.tr.auth_("Name"), ""),
                "permissions": (cbpos.tr.auth_("Permissions"), []),
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
        return {"name": (cbpos.tr.auth_("Name"), ""),
                "description": (cbpos.tr.auth_("Description"), ""),
                "menu_restrictions": (cbpos.tr.auth_("Menu Restrictions"), []),
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
        return {"username": (cbpos.tr.auth_("Username"), ""),
                "role": (cbpos.tr.auth_("Role"), None),
                "password_check": ("", False),
                "password1": (cbpos.tr.auth_("Password"), ""),
                "password2": (cbpos.tr.auth_("Confirm Password"), "")
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
