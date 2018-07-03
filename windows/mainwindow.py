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

from PyQt5 import QtCore, QtGui, QtWidgets
from windows.ui.mainwindow import Ui_MainWindow
from core.adapters.adapter_registry import AdapterRegistry
from PyQt5.QtWidgets import QMessageBox
import h5py as h5
import sys
import os
from core.plugins import PluginRegistry

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self._adapter = None

        self._setup_ui()

        self._switch_parser()

        self._update_groups([])

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            if len(event.mimeData().urls()) == 1:
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self._open_file(files[0])

    def _switch_parser(self):
        self._current_parser = PluginRegistry.get_parser(self.parserComboBox.currentIndex())()

        # clear current settings
        for child in self.parserSettingsGroupBox.children(): 
            if child is self.parserSettingsGroupBox.layout():
                continue

            child.deleteLater()

        if not self._current_parser.show_settings(self.parserSettingsGroupBox):
            self.parserSettingsGroupBox.setVisible(False)
        else:
             self.parserSettingsGroupBox.setVisible(True)

        current_item = self.groups_treeWidget.currentItem()
        if current_item:
            data = current_item.data(1, 0)
            if data is not None:
                self._parsed_data = self._current_parser.parse(data)
                visualizer_type = PluginRegistry.get_visualizer(type(self._parsed_data))
                if visualizer_type is not None:
                    visualizer_type().visualize_data(self._parsed_data, self.widgetDataContent)

    def _setup_ui(self):
        self.parserComboBox.clear()
        for plugin in PluginRegistry.get_parsers():
            parser_name = plugin.get_ui_name()
            self.parserComboBox.addItem(parser_name)
        self.parserComboBox.setCurrentIndex(1)
            
        self._connect_ui_components()


    def _connect_ui_components(self):
        self.actionOpen.triggered.connect(self._actionOpen_triggered)
        self.actionClose.triggered.connect(self._actionClose_triggered)
        self.actionExit.triggered.connect(self._actionExit_triggered)

        self.groups_treeWidget.currentItemChanged.connect(self._groups_treeWidget_itemChanged)

        self.parserComboBox.currentIndexChanged.connect(lambda: self._switch_parser())
        
    def _groups_treeWidget_itemChanged(self, new_item, old_item):
        for child in self.widgetDataContent.children(): 
            if child is self.widgetDataContent.layout():
                continue

            child.deleteLater()

        if not new_item:
            return

        data = new_item.data(1, 0)
        if data is not None:
            self._parsed_data = self._current_parser.parse(data)

            if self._parsed_data:
                visualizer_type = PluginRegistry.get_visualizer(type(self._parsed_data))
                if visualizer_type is not None:
                    visualizer_type().visualize_data(self._parsed_data, self.widgetDataContent)

            # else:
            # spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            # self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)

    def _close_file(self):
        if not self._adapter:
            return True

        if self._adapter.is_file_opened():
            self._adapter.close_file()

        if not self._adapter.is_file_opened():
            self.setWindowTitle("Data Viewer")
            self._update_groups([])

            return True
        else:
            return False

    def _open_file(self, file_name=None):
        if self._adapter and self._adapter.is_file_opened():
            if not self._close_file():
                return

        extensions = ";;".join(["All files (*.*)"] + [x.get_file_extensions() for x in AdapterRegistry.get_adapters()])
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a data file", "", extensions)

        if file_name:
            adapter_class = AdapterRegistry.get_adapter(file_name)
            if adapter_class:
                self._adapter = adapter_class()

            if not self._adapter or not self._adapter.open_file(file_name):
                QMessageBox.warning(self, "Could not open file", "The file selected could be opened.")
            else:
                self.setWindowTitle("{0} - Data Viewer".format(self._adapter.get_file_name()))
                self._update_groups(self._adapter.get_treeview_items())

    def _actionOpen_triggered(self):
        self._open_file()

    def _actionClose_triggered(self):
        self._close_file()

    def _actionExit_triggered(self):
        if self._close_file():
            sys.exit()

    def _update_groups(self, items):
        self.groups_treeWidget.clear()

        def translate_item(item):
            ui_item = QtWidgets.QTreeWidgetItem([item.name])
            ui_item.setData(1, 0, item.data)

            for child in item.children:
                ui_item.addChild(translate_item(child))

            return ui_item

        top_level_ui_items = []
        for item in items:
            ui_item = translate_item(item)
            top_level_ui_items.append(ui_item)

        self.groups_treeWidget.addTopLevelItems(top_level_ui_items)