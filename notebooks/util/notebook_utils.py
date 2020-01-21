import sys
import io

import ipywidgets


widget_table = {}


def create_text_widget( name, placeholder ):

    if name in widget_table:
        widget = widget_table[name]
    if name not in widget_table:
        widget = ipywidgets.Text( description = name, placeholder = placeholder )
        widget_table[name] = widget
    display(widget)
    
    return widget

