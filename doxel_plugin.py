import sublime_plugin
import os
import sys
from . import dq


DOXELS_REPO = '/Users/kamrik/src/dox/doxels'


class OpenDoxelCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        reg = self.view.sel()[0]
        ln = self.view.line(reg)
        line = self.view.substr(ln).strip()
        # print(line_contents)
        sep = os.path.sep
        # TODO: this is really fragile
        path = sep + line.split(sep, 1)[1]
        self.view.window().open_file(path)
        # self.view.insert(edit, 0, "Hello, World!")

class AppendDoxelListCommand(sublime_plugin.TextCommand):
    def run(self, edit, contents):
        txt = contents
        self.view.insert(edit, self.view.size() - 1, txt)




class QueryDoxelsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Assume that first line in the view is the query
        line = self.view.substr(self.view.line(0)).strip()
        print(line)
        repo = dq.Repo(DOXELS_REPO)
        doxels = repo.query(line)
        #for d in doxels:
        #    self.view.insert(edit, self.view.size() - 1 , d.id + '\n')
        # self.view.insert(edit, self.view.size() - 1 , 'Version is: ' + sys.version)
        # f = open('/Users/kamrik/src/dox/doxels/KitchenShelves.doxel', encoding='UTF-8')

        lst = ['* copy to view']
        shift = len(lst)
        lst.extend(d.title for d in doxels)



        def on_selectd_doxel(idx):
            # Panel cancelled (Esc pressed)
            if idx == -1:
                return
            # Copy to view
            if idx == 0:
                txt = '\n'.join(d.id for d in doxels)
                self.view.run_command("append_doxel_list", {"contents": txt})
                return

            path = doxels[idx - shift].id
            self.view.window().open_file(path)

        self.view.window().show_quick_panel(lst, on_selectd_doxel)
