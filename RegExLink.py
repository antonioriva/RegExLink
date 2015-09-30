#!/usr/bin/python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import webbrowser
import subprocess
import shlex
import os

REGION_NAME = "RegExLink"

class RegExLinkEventCommand(sublime_plugin.EventListener):

    def on_activated_async(self, view):
        self._highlight(view)

    def on_post_save_async(self, view):
        self._highlight(view)

    def on_load(self, view):
        self._highlight(view)

    def _highlight(self, view):
        settings = sublime.load_settings("RegExLink.sublime-settings")
        regex_link_def = settings.get('regex_link_def')
        regex_link_mark_style = settings.get('regex_link_mark_style')
        regex_link_outlines = settings.get('regex_link_outlines', False)

        if not regex_link_outlines:
            for link_def in regex_link_def:
                view.erase_regions(REGION_NAME + link_def['name'])
            return

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
        currfolder = sublime.expand_variables(
            "$folder", sublime.active_window().extract_variables())
        os.chdir(currfolder)
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
                            command = shlex.split(region[1])
                            try:
                                subprocess.Popen(command)
                            except:
                                sublime.error_message("Error executing: \n\n" + " ".join(command))

    def is_visible(self, paths=None):
        return True
