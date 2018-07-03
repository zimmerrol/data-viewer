# Copyright (c) 2018 Roland Zimmermann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from core.plugins import Visualizer, PluginRegistry, Parser, ParsedData
import numpy as np
from PyQt5 import QtGui, QtWidgets

@PluginRegistry.visualizer
class StringVisualizer(Visualizer):
    def __init__(self):
        pass

    @staticmethod
    def get_ui_name():
        return "String"

    @staticmethod
    def validate_input_format(parsed_data_type):
        return parsed_data_type == ParsedDataString

    def _show_data(self, container_widget):       
        label = QtWidgets.QTextEdit()
        label.setText(self._parsed_data.get_data())
        label.setContentsMargins(0,0,0,0)
        label.setReadOnly(True)
       
        container_widget.layout().addWidget(label, 0,0,1,1)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(1)
        label.setSizePolicy(size_policy)
        #label.setScaledContents(True)
        #label.setWordWrap(True)
        label.show()

        return True

    def visualize_data(self, parsed_data, container_widget):
        self._parsed_data = parsed_data
        self._container_widget = container_widget

        return self._show_data(container_widget)

@PluginRegistry.parser
class StringParser(Parser):
    def __init__(self):
        self._encoding_combobox = None

    def validate_input_format(self, shape, size, dtype):
        return True

    def parse(self, data):
        value = None
        if isinstance(data, str):
            value = data
        else:
            try:
                if isinstance(data, np.ndarray) and data.dtype.type is np.string_ and data.size == 1:
                    value = data.item(0)
                elif isinstance(data, bytes):
                    value = data
            except:
                value = str(data)

            if isinstance(value, bytes):
                try:
                    value  = value.decode(self._encoding_combobox.itemText(self._encoding_combobox.currentIndex()))
                except:
                    # decoding failed
                    value  = str(value )

            if value is None:
                value = str(data)

        return ParsedDataString(value)

    def show_settings(self, container_widget):
        options_box = QtWidgets.QWidget()
        options_layout = QtWidgets.QHBoxLayout(options_box) 
        options_layout.setContentsMargins(0, 0, 0, 0)
        options_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        container_widget.layout().addWidget(options_box)

        if self._encoding_combobox:
            del self._encoding_combobox

        label = QtWidgets.QLabel()
        label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        options_layout.addWidget(label)
        label.setText("Encoding:")

        self._encoding_combobox = QtWidgets.QComboBox()
        self._encoding_combobox.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        options_layout.addWidget(self._encoding_combobox)
        self._encoding_combobox.addItems(["utf-8", "ascii", "utf-16", "utf-32"])

        return True

    @staticmethod
    def get_ui_name():
        return "String"

class ParsedDataString(ParsedData):
    def __init__(self, raw_value):
        if isinstance(raw_value, str):
            self._value = raw_value
        else:
            self._value = str(raw_value)
        
    def get_data(self):
        return self._value