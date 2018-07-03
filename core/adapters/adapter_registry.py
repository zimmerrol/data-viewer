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

from core.adapters.adapter_base import Adapter
from glob import glob
import os
import importlib.machinery
import inspect
import sys

class AdapterRegistry(object):
    _adapters = []

    @staticmethod
    def adapter(adapter_class):
        if not issubclass(adapter_class, Adapter):
            raise ValueError("The class `{0}´ does not inherit from `Adapter` class. Therefore, it cannot be registered as a data adapter.".format(adapter_class))
        if not adapter_class in AdapterRegistry._adapters:
            AdapterRegistry._adapters.append(adapter_class)

    @staticmethod
    def get_adapters():
        for adapter in AdapterRegistry._adapters:
            yield adapter

    @staticmethod
    def get_adapter(file_name):
        for adapter in AdapterRegistry._adapters:
            if adapter.can_open_file(file_name):
                return adapter
        return None

    @staticmethod
    def load_adapters(adapter_directory):
        for file_name in glob(os.path.join(adapter_directory, "*.py")):
            module_name = file_name[:-3].replace("\\", "/").replace("/",".").replace("..", "")

            sys.modules[module_name] = importlib.machinery.SourceFileLoader(module_name, file_name).load_module()