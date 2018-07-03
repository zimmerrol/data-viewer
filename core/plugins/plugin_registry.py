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

from core.plugins.visualizer_base import Visualizer
from core.plugins.parser_base import Parser
from glob import glob
import os
import imp
import inspect

class PluginRegistry(object):
    _visualizers = []
    _parsers = []

    @staticmethod
    def visualizer(visualizer_class):
        if not issubclass(visualizer_class, Visualizer):
            raise ValueError("The class `{0}´ does not inherit from Visualizer class. Therefore, it cannot be registered as a visualizer plugin.".format(visualizer_class))
        if not visualizer_class in PluginRegistry._visualizers:
            PluginRegistry._visualizers.append(visualizer_class)

    @staticmethod
    def get_visualizers():
        for visualizer in PluginRegistry._visualizers:
            yield visualizer

    @staticmethod
    def get_visualizer(parsed_data_type):
        for visualizer_type in PluginRegistry._visualizers:
            if visualizer_type.validate_input_format(parsed_data_type):
                return visualizer_type
        else:
            return None

    @staticmethod
    def parser(parser_class):
        if not issubclass(parser_class, Parser):
            raise ValueError("The class `{0}´ does not inherit from Parser class. Therefore, it cannot be registered as a parser plugin.".format(parser_class))
        if not parser_class in PluginRegistry._parsers:
            PluginRegistry._parsers.append(parser_class)

    @staticmethod
    def get_parsers():
        for plugin in PluginRegistry._parsers:
            yield plugin

    @staticmethod
    def get_parser(index):
        return PluginRegistry._parsers[index]

    @staticmethod
    def load_plugins(plugin_directory):
        for file_name in glob(os.path.join(plugin_directory, "*.py")):
            imp.load_source(os.path.basename(file_name), file_name)