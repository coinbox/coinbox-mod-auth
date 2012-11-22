import cbpos

from cbpos.mod.auth.models import User

class UserState(object):
    __logged_in_user = None
    
    @property
    def current(self):
        return self.__logged_in_user
    
    @current.setter
    def current(self, value):
        self.__logged_in_user = value
    
    @current.deleter
    def current(self):
        self.__logged_in_user = None
    
    def login(self, username, password):
        session = cbpos.database.session()
        try:
            u = session.query(User).filter(User.username == username).one()
        except exc.NoResultFound, exc.MultipleResultsFound:
            del self.current
        else:
            if u.login(password):
                self.current = u
            else:
                del self.current
        
        if self.current is not None and self.current.super:
            # Filter menu items to display according to permissions
            restrictions = [(mr.root, mr.item) for mr in self.current.menu_restrictions] 
            for root in cbpos.menu.main.items:
                for item in root.children:
                    item.enabled = ((root.label, item.label) in restrictions)
            
        return self.current
    
    def is_logged_in(self):
        return self.current is not None

user = UserState()