from pydispatch import dispatcher

from PySide import QtGui, QtCore
import datetime

import cbpos
logger = cbpos.get_logger(__name__)

from cbpos.mod.auth.views.dialogs.clockingpanel import ClockingPanel
from cbpos.mod.auth.views.dialogs import LoginDialog
from cbpos.mod.auth.controllers import user
from cbpos.mod.base.ui import MainWindowExtension
from cbpos.mod.base.views import MainWindow

class ClockingMainWindow(MainWindowExtension):
    """
    Adds the clock-in/clock-out panel on startup and handles the clock-in/out
    and logout actions.
    """
    def init(self):
        self.do_load_clocking_panel()
    
    def do_load_clocking_panel(self):
        #adds the clock-in/clock-out slide panel.
        self.clockingPanel = ClockingPanel(self, cbpos.res.auth("images/clocking.svg"))
        self.clockingPanel.setSize(300, 260)
        self.clockingPanel.btnLogin.clicked.connect(self.onDoClocking)
        self.clockingPanel.btnExit.clicked.connect(self.onExitButton)
        self.clockingPanel.editUsername.currentIndexChanged.connect(self.clockingPanel.editPassword.setFocus)
        self.clockingPanel.editPassword.returnPressed.connect(self.onDoClocking)
        
        self.clockingPanel.setIsIn(True)
        self.clockingPanel.showPanel()
        self.tabs.setEnabled(False)
        
        self.__connect_receivers()

    def __connect_receivers(self):
        """
        Connect the receivers of the clock-in/out and logout actions so that
        they can be handled properly.
        
        Make sure they are disconnected when the
        window is destroyed (or closed), otherwise the login dialog will
        display multiple times every time the logout button is pressed (since
        the action-logout will call it multiple times).
        """
        dispatcher.connect(self.do_show_clockin, signal='action-clockin', sender='action')
        dispatcher.connect(self.do_show_clockout, signal='action-clockout', sender='action')
        dispatcher.connect(self.do_logout, signal='action-logout', sender='action')

    def __disconnect_receivers(self):
        """
        Disconnect the receivers of the actions, so that they no longer get
        called when the window is re-created.
        """
        dispatcher.disconnect(self.do_show_clockin, signal='action-clockin', sender='action')
        dispatcher.disconnect(self.do_show_clockout, signal='action-clockout', sender='action')
        dispatcher.disconnect(self.do_logout, signal='action-logout', sender='action')

    def closeEvent(self, event):
        """
        Overrides the MainWindow closeEvent to disconnect the receivers,
        then calls the MainWindow's closeEvent so that it handles the rest.
        """
        self.__disconnect_receivers()
        return MainWindow.closeEvent(self, event)

    def do_logout(self):
        """
        Closes the MainWindow and shows the LoginDialog when the action-logout
        is received.
        """
        self.close()
        cbpos.ui.window = dialog =  LoginDialog()
        dialog.show()

    def do_show_clockin(self):
        """
        Show the clock-in dialog when the action-clockin is received.
        """
        self.clockingPanel.setIsIn(True)
        self.clockingPanel.showPanel()
        self.tabs.setEnabled(False)
    
    def do_show_clockout(self):
        """
        Show the clock-out dialog when the action-clockout is received.
        """
        self.clockingPanel.setIsIn(False)
        self.clockingPanel.showPanel()
        self.tabs.setEnabled(False)

    def onExitButton(self):
        self.clockingPanel.clean()
        self.clockingPanel.hidePanel()
        self.tabs.setEnabled(True)

    def onDoClocking(self):
        """
        Callback to actually clock-in the user.
        Called when the clock-in button is pressed or return is pressed.
        """
        username = self.clockingPanel.getUserName()
        password = self.clockingPanel.getPassword()
        
        u = user.check(username, password)
        
        if not u:
            message = '<html><head/><body><p><span style=" font-size:14pt; font-weight:600; font-style:italic; color:#ff0856;">%s</span></p></body></html>'%cbpos.tr.auth._('Invalid username or password.')
            self.showAuthErrorMessage(message)
            return
        
        is_in = self.clockingPanel.isIn()
        date_time = datetime.datetime.now()
        
        if is_in:
            if user.clockin(u):
                message = cbpos.tr.auth._('Clock in sucessful.\nYour in time is %s'%date_time)
                self.showDoneMessage(message)
            else:
                message = cbpos.tr.auth._('Clock in UNSUCCESSFUL')
                self.showErrorMessage(message)
        else:
            if user.clockout(u):
                message = cbpos.tr.auth._('Clock out sucessful.\nYour out time is %s'%date_time)
                self.showDoneMessage(message)
            else:
                message = cbpos.tr.auth._('Clock out UNSUCESSFUL')
                self.showErrorMessage(message)

    def showAuthErrorMessage(self, msg):
        self.clockingPanel.setError(msg)

    def showErrorMessage(self, msg):
        self.clockingPanel.setError(msg)

    def showDoneMessage(self, msg):
        self.clockingPanel.setMessage(msg)
        #Wait 1 seconds to close the panel.
        QtCore.QTimer.singleShot(1000, self.clockingPanel.hidePanel)
