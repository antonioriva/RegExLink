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

        flags = sublime.DRAW_NO_FILL
        if not regex_link_outlines:
            flags = sublime.HIDDEN

        for link_def in regex_link_def:
            if 'link' in link_def:
                extract = []
                result = view.find_all(
                    link_def['regex'], 0, link_def['link'], extract)
                for sel in view.sel():
                    view.add_regions(
                        REGION_NAME +
                        link_def['name'], result, link_def['style'],
                        regex_link_mark_style, flags)

            if 'command' in link_def:
                extract = []
                result = view.find_all(
                    link_def['regex'], 0, link_def['command'], extract)
                for sel in view.sel():
                    view.add_regions(
                        REGION_NAME +
                        link_def['name'], result, link_def['style'],
                        regex_link_mark_style, flags)


class RegExLinkCommand(sublime_plugin.TextCommand):

    contentmenu = ""

    def run(self, edit):
        settings = sublime.load_settings("RegExLink.sublime-settings")
        regex_link_def = settings.get('regex_link_def')
        currfolder = sublime.expand_variables(
            "$folder", sublime.active_window().extract_variables())
        os.chdir(currfolder)
        for link_def in regex_link_def:
            extract = []
            if 'link' in link_def:
                linktype = 'link'
            elif 'command' in link_def:
                linktype = 'command'
            else:
                continue

            result = self.view.find_all(
                link_def['regex'], 0, link_def[linktype], extract)
            for sel in self.view.sel():
                for region in zip(result, extract):
                    if sel.b >= region[0].a and sel.a <= region[0].b:
                        if linktype == 'link':
                            webbrowser.open(region[1])
                        elif linktype == 'command':
                            command = shlex.split(region[1])
                            try:
                                subprocess.Popen(command)
                            except:
                                sublime.error_message(
                                   "Error executing: \n\n" + " ".join(command))

    def is_visible(self, paths=None):
        if self.contentmenu != "":
            return True
        else:
            return False

    def description(self):
        settings = sublime.load_settings("RegExLink.sublime-settings")
        regex_link_def = settings.get('regex_link_def')
        for link_def in regex_link_def:
            extract = []
            if 'link' in link_def:
                linktype = 'link'
            elif 'command' in link_def:
                linktype = 'command'
            else:
                continue

            result = self.view.find_all(
                link_def['regex'], 0, link_def[linktype], extract)
            for sel in self.view.sel():
                for region in zip(result, extract):
                    if sel.b >= region[0].a and sel.a <= region[0].b:
                        self.contentmenu = link_def[
                            'name'] + " " + self.view.substr(region[0])
                        return "Open " + self.contentmenu
                    else:
                        self.contentmenu = ""
        return "Open " + self.contentmenu
