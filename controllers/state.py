import cbpos

from cbpos.mod.auth.models import User

from sqlalchemy.orm import exc

import os, base64

import logging
logger = logging.getLogger(__name__)

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
        
        if self.current is not None and not self.current.super:
            # Filter menu items to display according to permissions
            restrictions = [(mr.root, mr.item) for mr in self.current.menu_restrictions] 
            for root in cbpos.menu.main.items:
                for item in root.children:
                    item.enabled = ((root.label, item.label) in restrictions)
            
        return self.current
    
    def is_logged_in(self):
        return self.current is not None
    
    @property
    def secret_key(self):
        if not cbpos.config['mod.auth', 'secret_key']:
            k = base64.b64encode(os.urandom(50))
            cbpos.config['mod.auth', 'secret_key'] = k
            cbpos.config.save()
            logger.debug('Authentication secret key set.')
         
        return base64.b64decode(cbpos.config['mod.auth', 'secret_key'])

user = UserState()
