import cbpos

from cbpos.mod.auth.models import User, Clock

from sqlalchemy.orm import exc

import os, base64, datetime

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
    
    def check(self, username, password):
        session = cbpos.database.session()
        try:
            u = session.query(User).filter(User.username == username).one()
        except exc.NoResultFound, exc.MultipleResultsFound:
            return None
        else:
            return u if u.login(password) else None
    
    def login(self, username, password):
        session = cbpos.database.session()
        u = self.check(username, password)
        if u is None:
            del self.current
        else:
            self.current = u
        
        if self.current is not None and not self.current.super:
            # Filter menu items to display according to permissions
            restrictions = [(mr.root, mr.item) for mr in self.current.menu_restrictions] 
            for root in cbpos.menu.items:
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
    
    def clockin(self, u=None):
        from cbpos.mod.auth.controllers import user

        session = cbpos.database.session()

        date_time = datetime.datetime.now()
        if u is None:
            u = self.current
        
        #create the new row.
        clockcard = Clock(user=u, date_time_in=date_time, date_time_out=date_time)
        session.add(clockcard)
        session.commit()
        return True
    
    def clockout(self, u=None):
        from cbpos.mod.auth.controllers import user

        session = cbpos.database.session()

        date_time = datetime.datetime.now()
        if u is None:
            u = self.current
        
        #Look for the last row for the user, which must have an out equal to the in.
        #In most cases, there will be only one row, but in some cases may be more due to someone forgetting the clock out.
        clockcard = session.query(Clock).filter_by(user=u).filter(Clock.date_time_in==Clock.date_time_out)
        #in cases where there are more than one, we need to know which to apply the changes.
        if clockcard.count() > 1:
            #What to do really? Apply to the last one?
            clockcard = clockcard.order_by("id DESC").first() #here we find the last one (ordering by id in descending order)
        else:
            clockcard = clockcard.order_by("id DESC").first()

        try:
            clockcard.date_time_out = date_time
            session.commit()
        except Exception as e:
            session.rollback()
            logger.debug("Error on saving clock out for user %s. Error is: %s"%(u, e))
            return False
        else:
            return True

user = UserState()
