import sys
import io

import ipywidgets


widget_table = {}


def create_text_widget( name, placeholder, default_value="" ):

    if name in widget_table:
        widget = widget_table[name]
    if name not in widget_table:
        widget = ipywidgets.Text( description = name, placeholder = placeholder, value=default_value )
        widget_table[name] = widget
    display(widget)
    
    return widget

