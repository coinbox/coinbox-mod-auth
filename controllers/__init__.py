import cbpos

from cbpos.mod.auth.models import User

_logged_in_user = None
@property
def current():
    return _logged_in_user

@current.setter
def current(value):
    _logged_in_value = value

@current.deleter
def current():
    _logged_in_value = None

def login(username, password):
    global current
    
    session = cbpos.database.session()
    try:
        u = session.query(User).filter(User.username == username).one()
    except exc.NoResultFound, exc.MultipleResultsFound:
        current = None
    else:
        current = u if u.login(password) else None
    
    if current is not None and user.current.super:
        # Filter menu items to display according to permissions
        restrictions = [(mr.root, mr.item) for mr in user.current.menu_restrictions] 
        for root in cbpos.menu.main.items:
            for item in root.children:
                item.enabled = ((root.label, item.label) in restrictions)
        
    return current

def is_logged_in():
    return current is not None