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
class ArrayVisualizer(Visualizer):
    def __init__(self):
        self._autoresize_checkbox = None

    @staticmethod
    def get_ui_name():
        return "Array"

    @staticmethod
    def validate_input_format(parsed_data_type):
        pass

    def show_settings(self, container_widget):
        return False

    def _show_data(self, container_widget):
        data = None
        try:
            if isinstance(self._data, list):
                try:
                    self._data = np.array(self._data)
                except:
                    pass

            if isinstance(self._data, np.ndarray):
                self._data = np.squeeze(self._data)
                if len(self._data.shape) < 2:
                    data = np.empty_like(self._data, dtype=object)
                    for i in range(data.size):
                        data.itemset(i, str(self._data.item(i)))
                else:
                    raise ValueError("Array has rank > 2. This cannot be displayed.")
                # to make vectors appear as (-1, 1) matrices
                data = data.reshape(len(data), -1)
            else:
                return False
        except:
            return False
       
        
        table = QtWidgets.QTableWidget()
        table.setContentsMargins(0,0,0,0)
        table.setRowCount(data.shape[0])
        table.setColumnCount(data.shape[1])
        # table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # table.horizontalHeader().setStretchLastSection(True)

        for i, row in enumerate(data):
            for j, val in enumerate(row):
                table.setItem(i, j, QtWidgets.QTableWidgetItem(val))


        # no resize, scroll viewer
        container_widget.layout().addWidget(table, 0,0,1,1)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(1)
        table.setSizePolicy(size_policy)
        table.show()

        return True

    def visualize_data(self, data, container_widget):
        self._data = data
        self._container_widget = container_widget

        return self._show_data(container_widget)

@PluginRegistry.visualizer
class ArrayVisualizer(Visualizer):
    def __init__(self):
        pass

    @staticmethod
    def get_ui_name():
        return "Array"

    @staticmethod
    def validate_input_format(parsed_data_type):
        return parsed_data_type == ParsedDataArray

    def _show_data(self, container_widget):   
        if self._parsed_data is None:
            return False

        table = QtWidgets.QTableWidget()
        table.setContentsMargins(0,0,0,0)
        table.setRowCount(self._parsed_data.get_shape()[0])
        table.setColumnCount(self._parsed_data.get_shape()[1])

        for i, row in enumerate(self._parsed_data.get_data()):
            for j, val in enumerate(row):
                table.setItem(i, j, QtWidgets.QTableWidgetItem(str(val))) 
                #table.resizeRowsToContents()
                #table.resizeColumnsToContents()

        # table.horizontalHeader().setStretchLastSection(True)

        # no resize, scroll viewer
        container_widget.layout().addWidget(table, 0,0,1,1)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(1)
        table.setSizePolicy(size_policy)
        table.show()

        return True

    def visualize_data(self, parsed_data, container_widget):
        self._parsed_data = parsed_data
        self._container_widget = container_widget

        return self._show_data(container_widget)

@PluginRegistry.parser
class ArrayParser(Parser):
    def __init__(self):
        pass

    def validate_input_format(self, shape, size, dtype):
        return True

    def parse(self, data):
        value = None
        if isinstance(data, np.ndarray):
            value = data
        else:
            try:
                value = np.array(data)
            except:
                value = None

        return ParsedDataArray(value)

    def show_settings(self, container_widget):
        return True

    @staticmethod
    def get_ui_name():
        return "Array"

class ParsedDataArray(ParsedData):
    def __init__(self, raw_value):
        if isinstance(raw_value, np.ndarray):
            self._value = raw_value
        else:
            self._value = np.array(raw_value)
        
    def get_data(self):
        return self._value

    def get_shape(self):
        if self._value is not None:
            return self._value.shape
        else:
            return None