# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" Enthought pyface package component
"""

import wx

from traits.api import Instance, provides

from pyface.i_heading_text import IHeadingText, MHeadingText
from pyface.image_resource import ImageResource
from .widget import Widget


@provides(IHeadingText)
class HeadingText(MHeadingText, Widget):
    """ The Wx-specific implementation of a HeadingText.
    """

    #: Background image.  This is deprecated and no-longer used.
    image = Instance(ImageResource, ImageResource("heading_level_1"))

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = wx.StaticText(parent)
        return control

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _set_control_text(self, text):
        """ Set the text on the toolkit specific widget. """
        # Bold the text. Wx supports a limited subset of HTML for rich text.
        text = f"<b>{text}</b>"
        self.control.SetLabelMarkup(text)

    def _get_control_text(self):
        """ Get the text on the toolkit specific widget. """
        return self.control.GetLabelText()
