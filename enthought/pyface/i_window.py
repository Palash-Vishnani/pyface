#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# 
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" The abstract interface for all pyface top-level windows. """


# Enthought library imports.
from enthought.traits.api import Any, Event, Int, Tuple, Unicode

# Local imports.
from constant import NO
from key_pressed_event import KeyPressedEvent
from i_widget import IWidget


class IWindow(IWidget):
    """ The abstract interface for all pyface top-level windows.

    A pyface top-level window has no visual representation until it is opened
    (ie. its 'control' trait will be None until it is opened).
    """

    #### 'IWindow' interface ##################################################
    
    # The position of the window.
    position = Tuple
    
    # The size of the window.
    size = Tuple

    # The window title.
    title = Unicode

    #### Events #####

    # The window has been activated.
    activated = Event

    # The window has been closed.
    closed =  Event

    # The window is about to be closed.
    closing =  Event
    
    # The window has been deactivated.
    deactivated = Event

    # A key was pressed while the window had focus.
    # FIXME v3: This smells of a hack. What's so special about key presses?
    # FIXME v3: Unicode
    key_pressed = Event(KeyPressedEvent)

    # The window has been opened.
    opened = Event

    # The window is about to open.
    opening = Event
    
    ###########################################################################
    # 'IWindow' interface.
    ###########################################################################

    def open(self):
        """ Opens the window. """

    def close(self):
        """ Closes the window. """

    def show(self, visible):
        """ Show or hide the window.
        
        visible is set if the window should be shown.
        """

    def confirm(self, message, title=None, cancel=False, default=NO):
        """ Convenience method to show a confirmation dialog.
        
        message is the text of the message to display.
        title is the text of the window title.
        cancel is set if the dialog should contain a Cancel button.
        default is the default button.
        """

    ###########################################################################
    # Protected 'IWindow' interface.
    ###########################################################################

    def _add_event_listeners(self):
        """ Adds any event listeners required by the window. """


class MWindow(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IWindow interface.

    Implements: close(), confirm(), open()
    Reimplements: _create()
    """

    ###########################################################################
    # 'IWindow' interface.
    ###########################################################################

    def open(self):
        """ Opens the window. """

        # Trait notification.
        self.opening = self

        if self.control is None:
            self._create()

        self.show(True)

        # Trait notification.
        self.opened = self
        
        return

    def close(self):
        """ Closes the window. """

        if self.control is not None:
            # Trait notification.
            self.closing = self

            # Cleanup the toolkit-specific control.
            self.destroy()

            # Trait notification.
            self.closed = self

        return

    def confirm(self, message, title=None, cancel=False, default=NO):
        """ Convenience method to show a confirmation dialog. """

        from confirmation_dialog import confirm

        return confirm(self.control, message, title, cancel, default)
    
    ###########################################################################
    # Protected 'IWidget' interface.
    ###########################################################################

    def _create(self):
        """ Creates the window's widget hierarchy. """

        # Create the toolkit-specific control.
        super(MWindow, self)._create()

        # Wire up event any event listeners required by the window.
        self._add_event_listeners()
        
        return

#### EOF ######################################################################
