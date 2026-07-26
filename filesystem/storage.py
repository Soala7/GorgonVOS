"""
VOS Filesystem Storage

Handles saving and loading the virtual filesystem.
"""

import json
import os

from .folder import Folder


class FileSystemStorage:

    def save(self, root, path):

        directory = os.path.dirname(path)

        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        data = self._folder_to_dict(root)

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        print(
            "[STORAGE] filesystem saved:",
            path
        )


    def load(self, path="VOS.os"):
        """
        Loads the filesystem tree from disk.
        """

        if not os.path.exists(path):

            print(
                "[STORAGE] save file not found"
            )

            return None



        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)



        print(
            "[STORAGE] filesystem loaded:",
            path
        )


        return self._dict_to_folder(
            data
        )



    def _folder_to_dict(self, folder):

        return {

            "name": folder.name,

            "files": folder.files,

            "folders": {

                name: self._folder_to_dict(
                    subfolder
                )

                for name, subfolder
                in folder.folders.items()

            }

        }



    def _dict_to_folder(self, data, parent=None):

        folder = Folder(
            data["name"],
            parent=parent
        )


        folder.files = data.get(
            "files",
            {}
        )


        for name, subfolder_data in data.get(
            "folders",
            {}
        ).items():

            subfolder = self._dict_to_folder(
                subfolder_data,
                parent=folder
            )


            folder.add_folder(
                subfolder
            )


        return folder