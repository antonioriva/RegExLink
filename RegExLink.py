#!/usr/bin/python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import webbrowser
from subprocess import call

REGION_NAME = "RegExLink"

class RegExLinkEventCommand(sublime_plugin.EventListener):

    def on_activated_async(self, view):
        self.highlight(view)

    def on_post_save_async(self, view):
        self.highlight(view)

    def highlight(self, view):
        settings = sublime.load_settings("RegExLink.sublime-settings")
        regex_link_def = settings.get('regex_link_def')
        regex_link_mark_style = settings.get('regex_link_mark_style')

        for link_def in regex_link_def:
            if 'link' in link_def:
                extract = []
                result = view.find_all(link_def['regex'], 0, link_def['link'], extract)
                for sel in view.sel():
                    view.add_regions(
                        REGION_NAME + link_def['name'], result, link_def['style'],
                        regex_link_mark_style, sublime.DRAW_NO_FILL)

            if 'command' in link_def:
                extract = []
                result = view.find_all(link_def['regex'], 0, link_def['command'], extract)
                for sel in view.sel():
                    view.add_regions(
                        REGION_NAME + link_def['name'], result, link_def['style'],
                        regex_link_mark_style, sublime.DRAW_NO_FILL)


class RegExLinkCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        settings = sublime.load_settings("RegExLink.sublime-settings")
        regex_link_def = settings.get('regex_link_def')

        for link_def in regex_link_def:
            extract = []

            if 'link' in link_def:
                result = self.view.find_all(link_def['regex'], 0, link_def['link'], extract)
                for sel in self.view.sel():
                    for region in zip(result, extract):
                        if sel.b >= region[0].a and sel.a <= region[0].b:
                            webbrowser.open(region[1])

            if 'command' in link_def:
                result = self.view.find_all(link_def['regex'], 0, link_def['command'], extract)
                for sel in self.view.sel():
                    for region in zip(result, extract):
                        if sel.b >= region[0].a and sel.a <= region[0].b:
                            print(region[1].split(" "))
                            call(region[1].split(" "))

    def is_visible(self, paths=None):
        return True
