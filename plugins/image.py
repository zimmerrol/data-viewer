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
import cv2
from PyQt5 import QtGui, QtWidgets

@PluginRegistry.visualizer
class ImageVisualizer(Visualizer):
    def __init__(self):
        self._autoresize_checkbox = None

    @staticmethod
    def get_ui_name():
        return "Image"

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
class ImageVisualizer(Visualizer):
    def __init__(self):
        pass

    @staticmethod
    def get_ui_name():
        return "Image"

    @staticmethod
    def validate_input_format(parsed_data_type):
        return parsed_data_type == ParsedDataImage

    def _show_data(self, container_widget):   
        if self._parsed_data is None:
            return False

        cv_image = self._parsed_data.get_data()
        image = QtGui.QImage(cv_image, cv_image.shape[1], cv_image.shape[0], cv_image.shape[1]*3, QtGui.QImage.Format_RGB888)

        pixmap = QtGui.QPixmap(image)
        label = QtWidgets.QLabel()
        label.setPixmap(pixmap)
        label.setContentsMargins(0,0,0,0)

        if self._autoresize_checkbox.isChecked():
            # auto resize, no scroll viewer
            container_widget.layout().addWidget(label, 0,0,1,1)
            size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            size_policy.setHorizontalStretch(1)
            size_policy.setVerticalStretch(1)
            label.setSizePolicy(size_policy)
            label.setScaledContents(True)
            label.show()
        else:
            # no resize, scroll viewer
            scroll_viewer = QtWidgets.QScrollArea()
            scroll_viewer.setWidget(label)
            scroll_viewer.show()
            container_widget.layout().addWidget(scroll_viewer, 0,0,1,1)
            size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            size_policy.setHorizontalStretch(1)
            size_policy.setVerticalStretch(1)
            scroll_viewer.setSizePolicy(size_policy)
            label.setSizePolicy(size_policy)
            label.setScaledContents(True)
            label.show()

        return True

    def visualize_data(self, parsed_data, container_widget):
        self._parsed_data = parsed_data
        self._container_widget = container_widget

        return self._show_data(container_widget)

@PluginRegistry.parser
class ImageParser(Parser):
    def __init__(self):
        self._autoresize_checkbox = None

    def validate_input_format(self, shape, size, dtype):
        return True

    def parse(self, data):
        value = None
        try:
            if isinstance(data, np.ndarray):
                if data.dtype.type is np.string_:
                    value = np.fromstring(data, dtype=np.uint8)
                if data.dtype.type is np.uint8:
                    value = data
            elif isinstance(data, bytes):
                value = np.fromstring(data, dtype=np.uint8)
                
        finally:
            if value is None:
                return None

        # decode the image
        image = cv2.imdecode(value, -1)

        if image is None:
            return None

        image_shape = np.asarray(image).shape

        if len(image_shape) == 3 and image_shape[-1] == 3:
            # convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        return ParsedDataImage(image)

    def show_settings(self, container_widget):
        if self._autoresize_checkbox:
            del self._autoresize_checkbox

        self._autoresize_checkbox = QtWidgets.QCheckBox()
        self._autoresize_checkbox.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        container_widget.layout().addWidget(self._autoresize_checkbox)
        self._autoresize_checkbox.setText("Resize image")

        # self._autoresize_checkbox.toggled.connect(lambda _: self._show_data(container_widget))

        return True

    @staticmethod
    def get_ui_name():
        return "Image"

class ParsedDataImage(ParsedData):
    def __init__(self, raw_value):
        if isinstance(raw_value, np.ndarray):
            self._value = image
        else:
            self._value = None
        
    def get_data(self):
        return self._value
