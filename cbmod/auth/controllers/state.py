from sqlalchemy.orm import exc
from sqlalchemy.sql import desc, asc
from sqlalchemy import func

import os, base64, datetime

import cbpos
logger = cbpos.get_logger(__name__)

from cbmod.auth.models import User, Clock

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
        except (exc.NoResultFound, exc.MultipleResultsFound) as e:
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
        
        if self.current is None:
            pass
        elif self.current.super:
            # Filter menu items to display all items 
            for root in cbpos.menu.items:
                for item in root.children:
                    item.enabled = True
        else:
            # Filter menu items to display according to permissions
            restrictions = [(mr.root, mr.item) for mr in self.current.menu_restrictions] 
            for root in cbpos.menu.items:
                for item in root.children:
                    item.enabled = ((root.name, item.name) in restrictions)
        
        return self.current
    
    def is_logged_in(self):
        return self.current is not None
    
    def clockin(self, u=None):
        from cbmod.auth.controllers import user

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
        from cbmod.auth.controllers import user

        session = cbpos.database.session()

        date_time = datetime.datetime.now()
        if u is None:
            u = self.current
        
        #Look for the last row for the user, which must have an out equal to the in.
        #In most cases, there will be only one row, but in some cases may be more due to someone forgetting the clock out.
        query = session.query(Clock).filter_by(user=u) \
            .filter(Clock.date_time_in==Clock.date_time_out) \
            .order_by(desc(Clock.id))
        
        # We find the last one (ordering by id in descending order)
        try:
            # Try to find the single one which matches
            clockcard = query.one()
        except exc.NoResultFound as e:
            # If none is found, fail.
            logger.debug("No corresponding clock in found.")
            return False
        except exc.MultipleResultsFound as e:
            # In cases where there are more than one,
            # we need to know which to apply the changes.
            # TODO: What to do really? Apply to the last one?
            logger.debug("Multiple corresponding clock-ins found, taking the first one.")
            clockcard = query.first()

        # Update the record with current time
        clockcard.date_time_out = func.now()
        try:
            session.commit()
        except:
            session.rollback()
            logger.exception("Error on saving clock out for user %s", u)
            return False
        else:
            return True

user = UserState()
