'''
Home to the ComboboxGrid utility for cAppInstaller
'''
import numpy as np
import PySimpleGUI as sg

class ComboboxGrid:
    '''
    Helps make a grid of Comboboxes
    '''
    def __init__(self, names: list, tag: str, max_per_row: int):
        '''
        Each Combobox will have the a name prefixed by <tag>_
        '''
        self.names = names
        self.tag = tag

        if '_' in tag:
            raise ValueError(f"_ cannot be in tag: {tag}")

        self.max_per_row = max_per_row

    @classmethod
    def np_split_with_none_fillers(cls, itr, split_count):
        '''
        More or less splits the given itr based off the split_count
        If the division is not evenly made, adds Nones to make it an even split.
        '''
        itr = np.array(itr[:], dtype=object)
        while True:
            try:
                return np.split(itr, split_count)
            except ValueError as ex:
                itr = np.append(itr, [None])

    def get_list_of_list_of_str(self):
        '''
        Splits the names into a list of lists using max_per_row
        '''
        return self.np_split_with_none_fillers(sorted(self.names), self.max_per_row)

    def get_list_of_list_of_checkboxes(self):
        '''
        Creates the checkboxes based off the given names/tag and max_per_row
        '''
        list_of_list_of_str = self.get_list_of_list_of_str()
        for h_idx, list_of_str in enumerate(list_of_list_of_str):
            max_display_name_length = len(max(list_of_str, key=lambda x: len(x) if x is not None else 0) or '')
            for idx, y in enumerate(list_of_str):
                if y is not None:
                    list_of_str[idx] = sg.Checkbox(key=f'{self.tag}_{y}', text=y, size=(max_display_name_length, 1), tooltip=f'{self.tag}: {y}')
                else:
                    list_of_str[idx] = sg.Text()
            list_of_list_of_str[h_idx] = list_of_str

        return np.swapaxes(list_of_list_of_str, 0, 1)