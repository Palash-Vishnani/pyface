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
""" The interface of a workbench editor. """
# standard library imports
import uuid

# Enthought library imports.
from enthought.traits.api import Any, Bool, HasTraits, Instance, Interface
from enthought.traits.api import implements

# Local imports.
from i_workbench_part import IWorkbenchPart, MWorkbenchPart


class IEditor(IWorkbenchPart):
    """ The interface of a workbench editor. """

    # The optional command stack.
    command_stack = Instance('enthought.undo.api.ICommandStack')

    # Is the object that the editor is editing 'dirty' i.e., has it been
    # modified but not saved?
    dirty = Bool(False)

    # The object that the editor is editing.
    #
    # The framework sets this when the editor is created.
    obj = Any

    #### Methods ##############################################################
    
    def close(self):
        """ Close the editor.

        This method is not currently called by the framework itself as the user
        is normally in control of the editor lifecycle. Call this if you want
        to control the editor lifecycle programmatically.

        """


class MEditor(MWorkbenchPart):
    """ Mixin containing common code for toolkit-specific implementations. """

    implements(IEditor)
    
    #### 'IEditor' interface ##################################################
    
    # The optional command stack.
    command_stack = Instance('enthought.undo.api.ICommandStack')

    # Is the object that the editor is editing 'dirty' i.e., has it been
    # modified but not saved?
    dirty = Bool(False)

    # The object that the editor is editing.
    #
    # The framework sets this when the editor is created.
    obj = Any

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __str__(self):
        """ Return an informal string representation of the object. """

        return 'Editor(%s)' % self.id

    ###########################################################################
    # 'IWorkbenchPart' interface.
    ###########################################################################

    def _id_default(self):
        """ Trait initializer. """

        # If no Id is specified then use a random uuid
        # this gaurantees (barring *really* unusual cases) that there are no
        # collisions between the ids of editors.
        return uuid.uuid4().bytes

    ###########################################################################
    # 'IEditor' interface.
    ###########################################################################
    
    def close(self):
        """ Close the editor. """

        if self.control is not None:
            self.window.close_editor(self)

        return

    #### Initializers #########################################################

    def _command_stack_default(self):
        """ Trait initializer. """

        # We make sure the undo package is entirely optional.
        try:
            from enthought.undo.api import CommandStack
        except ImportError:
            return None
            
        return CommandStack(undo_manager=self.window.workbench.undo_manager)

#### EOF ######################################################################
