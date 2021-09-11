'''
Home to the GUI for cAppInstaller
'''
from inspect import trace
import queue
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, TimeoutError

import numpy as np
import PySimpleGUI as sg

from .choco import CHECKBOXES_PER_ROW as CHOCO_CHECKBOXES_PER_ROW
from .choco import CHOCOLATEY_APPS, Choco
from .combobox_grid import ComboboxGrid
from .misc_cmd import CHECKBOXES_PER_ROW as MISC_CMD_CHECKBOXES_PER_ROW
from .misc_cmd import MISC_COMMANDS


class cAppInstaller:
    '''
    This object will create/start/run the Window for cAppInstaller
    '''
    def __init__(self):
        self.window = sg.Window('cAppInstaller', self._get_layout(), grab_anywhere=True, resizable=True)

    def _get_layout(self) -> list:
        '''
        Gets the layout grid for the window
        '''
        cg1 = ComboboxGrid(list(CHOCOLATEY_APPS.keys()), 'choco', CHOCO_CHECKBOXES_PER_ROW)
        cg2 = ComboboxGrid(list(MISC_COMMANDS.keys()), 'cmd', MISC_CMD_CHECKBOXES_PER_ROW)

        return [
            [
                sg.Column(
                    [
                        [sg.Frame('Chocolatey Packages', cg1.get_list_of_list_of_checkboxes().tolist())],
                        [sg.Frame('Configurations', cg2.get_list_of_list_of_checkboxes().tolist(), expand_x=True)]
                    ]
                ),
                sg.Multiline(key='Output', disabled=True, expand_x=True, expand_y=True, autoscroll=True, size=(100, 1))
            ],
            [sg.Frame('Actions', [[sg.Button(button_text='Select All', key='select_all'), sg.Button(button_text='Install Selected', key='install_selected')]], expand_x=True)]
        ]

    def select_all_checkboxes_action(self):
        '''
        Checks all checkboxes if they are not all checked. If all are checked, uncheck all
        '''
        checkboxes = [a for a in self.window.key_dict.values() if isinstance(a, sg.Checkbox)]

        # if all checkboxes are checked... uncheck... otherwise check
        if all([c.get() for c in checkboxes]):
            value = False
        else:
            value = True
        for cb in checkboxes:
            cb.update(value=value)

    def get_checked_checkboxes(self) -> list:
        '''
        Gets a list of checkboxes that are checked
        '''
        return [a for a in self.window.key_dict.values() if isinstance(a, sg.Checkbox) and a.get()]

    def install_single_thing(self, tag: str, key: str) -> int:
        '''
        Installs the given thing... returns exit code. 0 == success.

        Internally the install will run in a thread and pass back output via a queue.
        This is done so that during the operation, the window can continue to update and not freeze.
        '''
        output_queue = queue.Queue()
        output = self.window['Output']

        def _inner():
            try:
                if tag == 'choco':
                    return Choco(key, output_queue).install()
                elif tag == 'cmd':
                    obj = MISC_COMMANDS[key]
                    return obj.install(output_queue)
                else:
                    raise ValueError(f"{tag} is not supported")
            except Exception as ex:
                output_queue.put_nowait([f"Unhandled Exception: {ex}"])
                output_queue.put_nowait([traceback.format_exc()])
                return -1

        def xfer_from_queue_to_output():
            lines = output_queue.get_nowait()
            for line in lines:
                output.print(line)

        output.print(f"About to run: {tag} - {key}")
        with ThreadPoolExecutor(max_workers=1) as pool:
            result = pool.submit(_inner)
            try:
                while True:
                    try:
                        xfer_from_queue_to_output()
                    except queue.Empty:
                        pass

                    try:
                        return result.result(timeout=.001)
                    except TimeoutError:
                        pass

                    self.window.finalize()
            finally:
                # flush the queue!
                while True:
                    try:
                        xfer_from_queue_to_output()
                    except queue.Empty:
                        break
                    self.window.finalize()
                    time.sleep(.001)

    def install_selected(self):
        '''
        Attempts to install all selected items
        '''
        self.window['install_selected'].update(disabled=True)
        try:
            checked = self.get_checked_checkboxes()

            for checkbox in checked:
                tag, key = checkbox.Key.split('_', 1)
                checkbox.update(background_color=sg.rgb(158, 163, 0))
                self.window.finalize() # forces the window to render the yellow now
                if self.install_single_thing(tag, key) == 0:
                    checkbox.update(background_color='green')
                    checkbox.update(value=False)
                else:
                    checkbox.update(background_color='red')
                self.window.finalize() # forces the window to render the next color now
        finally:
            self.window['install_selected'].update(disabled=False)

    def run(self):
        '''
        Runs until an exit
        '''
        while True:
            event, values = self.window.read()
            if event in (None, 'Exit'):
                break

            if event == 'select_all':
                self.select_all_checkboxes_action()
            elif event == 'install_selected':
                self.install_selected()

def main():
    cAppInstaller().run()

if __name__ == '__main__':
    main()
