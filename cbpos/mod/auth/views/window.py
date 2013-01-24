from pydispatch import dispatcher

from PySide import QtGui, QtCore
import datetime

import cbpos

import logging
logger = logging.getLogger(__name__)

from cbpos.mod.auth.views.dialogs.clockingpanel import ClockingPanel
from cbpos.mod.auth.controllers import user
from cbpos.mod.base.ui import MainWindowExtension

class ClockingMainWindow(MainWindowExtension):
    
    def init(self):
        self.do_load_clocking_panel()
    
    def do_load_clocking_panel(self):
        #adds the clock-in/clock-out slide panel.
        self.clockingPanel = ClockingPanel(self, cbpos.res.auth("images/clocking.svg"))
        self.clockingPanel.setSize(300, 260)
        self.clockingPanel.btnLogin.clicked.connect(self.onDoClocking)
        self.clockingPanel.btnExit.clicked.connect(self.do_hidePanel)
        self.clockingPanel.editUsername.currentIndexChanged.connect(self.clockingPanel.editPassword.setFocus)
        self.clockingPanel.editPassword.returnPressed.connect(self.onDoClocking)
        
        dispatcher.connect(self.do_show_clockin, signal='action-clockin', sender='action')
        dispatcher.connect(self.do_show_clockout, signal='action-clockout', sender='action')
        
        self.clockingPanel.setIsIn(True)
        self.clockingPanel.showPanel()

    def do_show_clockin(self):
        self.clockingPanel.setIsIn(True)
        self.clockingPanel.showPanel()
    
    def do_show_clockout(self):
        self.clockingPanel.setIsIn(False)
        self.clockingPanel.showPanel()

    def do_hidePanel(self):
        self.clockingPanel.clean()
        self.clockingPanel.hidePanel()

    def onDoClocking(self):
        username = self.clockingPanel.getUserName()
        password = self.clockingPanel.getPassword()
        
        u = user.check(username, password)
        
        if not u:
            message = '<html><head/><body><p><span style=" font-size:14pt; font-weight:600; font-style:italic; color:#ff0856;">%s</span></p></body></html>'%cbpos.tr.auth._('Invalid username or password.')
            self.onAuthError(message)
            return
        
        is_in = self.clockingPanel.isIn()
        date_time = datetime.datetime.now()
        
        if is_in:
            if user.clockin(u):
                message = cbpos.tr.auth._('Clock in sucessful.\nYour in time is %s'%date_time)
                self.onClockingDone(message)
            else:
                message = cbpos.tr.auth._('Clock in UNSUCCESSFUL')
                self.onClockingError(message)
        else:
            if user.clockout(u):
                message = cbpos.tr.auth._('Clock out sucessful.\nYour out time is %s'%date_time)
                self.onClockingDone(message)
            else:
                message = cbpos.tr.auth._('Clock out UNSUCESSFUL')
                self.onClockingError(message)

    def onAuthError(self, msg):
        self.clockingPanel.setError(msg)

    def onClockingDone(self, msg):
        self.clockingPanel.setMessage(msg)
        #Wait 1 seconds to close the panel.
        QtCore.QTimer.singleShot(1000, self.clockingPanel.hidePanel)
