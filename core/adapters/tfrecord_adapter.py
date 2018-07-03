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

from core.adapters.adapter_base import Adapter, DataItem
from core.adapters.adapter_registry import AdapterRegistry
import h5py as h5
from PyQt5 import QtCore, QtGui, QtWidgets
from windows.ui.mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
from core.utils.tfrecord import TFRecord

@AdapterRegistry.adapter
class TFRecordAdapter(Adapter):
    def __init__(self):
        self._file = None

    def open_file(self, file_name):
        try:
            self._file = TFRecord(file_name)
            self._file_name = file_name
            return True
        except:
            return False

    def close_file(self):
        self._file.close()
        del self._file
        self._file = None

    def get_file_name(self):
        return self._file_name

    def get_treeview_items(self):
        def create_feature(example, feature_name):
            feature_value = example.features.feature.get(feature_name)

            # TODO: Add support for multiple sub-fields
            value = feature_value.ListFields()[0][1].value

            if len(value) == 1:
                value = value[0]

            item = DataItem(name=feature_name, data=value)

            return item

        def create_example(example, index):
            item = DataItem(name="Example #{0}".format(index))

            for feature in example.features.feature:
                item.children.append(create_feature(example, feature))

            return item

        items = []
        if self._file:
            for i, example in enumerate(self._file):
                items.append(create_example(example, i))

        return items

    def is_file_opened(self):
        return self._file != None

    @staticmethod
    def get_file_extensions():
        return "tfrecord (*.tfrecord)"

    @staticmethod
    def can_open_file(file_name):
        try:
            test_file = TFRecord(file_name)
            test_file.close()
            del test_file
            return True
        except:
            return False