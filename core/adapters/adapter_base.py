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

from abc import ABC, abstractclassmethod

class Adapter(ABC):
    def __init__(self):
        pass

    @abstractclassmethod
    def open_file(self):
        raise NotImplementedError("This method has to be defined in the inherited class. There is no base definition available.")

    @abstractclassmethod
    def close_file(self):
        raise NotImplementedError("This method has to be defined in the inherited class. There is no base definition available.")

    @abstractclassmethod
    def get_file_name(self):
        raise NotImplementedError("This method has to be defined in the inherited class. There is no base definition available.")

    @abstractclassmethod
    def get_treeview_items(self):
        raise NotImplementedError("This method has to be defined in the inherited class. There is no base definition available.")

    @abstractclassmethod
    def is_file_opened(self):
        raise NotImplementedError("This method has to be defined in the inherited class. There is no base definition available.")

    @abstractclassmethod
    def get_file_extensions(self):
        raise NotImplementedError("This method has to be defined in the inherited class. There is no base definition available.")

    @abstractclassmethod
    def can_open_file(self, file_name):
        raise NotImplementedError("This method has to be defined in the inherited class. There is no base definition available.")

class DataItem(object):
    def __init__(self, name, data=None):
        self.name = name
        self.data = data
        self.children = []