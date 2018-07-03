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

@AdapterRegistry.adapter
class HDF5Adapter(Adapter):
    def __init__(self):
        self._file = None

    def open_file(self, file_name):
        try:
            self._file = h5.File(file_name, "r")
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
        def create_dataset(dataset):
            return DataItem(name=dataset.name.split("/")[-1], data=dataset.value)

        def create_group(group):
            item = DataItem(name=group.name.split("/")[-1])

            for child_group_name in group:
                if not isinstance(group[child_group_name], h5.Dataset):
                    item.children.append(create_group(group[child_group_name]))
                else:
                    item.children.append(create_dataset(group[child_group_name]))

            return item

        items = []
        if self._file:
            
            for group_name in self._file:
                if not isinstance(self._file[group_name], h5.Dataset):
                    items.append(create_group(self._file[group_name]))
                else:
                    items.append(create_dataset(self._file[group_name]))

        return items

    def is_file_opened(self):
        return self._file != None

    @staticmethod
    def get_file_extensions():
        return "HDF5 (*.h5 *.hdf *.hdf5)"

    @staticmethod
    def can_open_file(file_name):
        try:
            test_file = h5.File(file_name)
            test_file.close()
            del test_file
            return True
        except:
            return False