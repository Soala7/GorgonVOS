"""
File: VOS/bridge/vos_api.py

VOS API Bridge

Provides access to VOS services for external systems
such as the C shell.
"""


class VOSAPI:

    def __init__(self):

        self.filesystem = None
        self.process_manager = None
        self.window_manager = None


    # -------------------------
    # Service registration
    # -------------------------

    def register_filesystem(self, filesystem):

        self.filesystem = filesystem


    def register_process_manager(self, process_manager):

        self.process_manager = process_manager


    def register_window_manager(self, window_manager):

        self.window_manager = window_manager



    # -------------------------
    # Filesystem commands
    # -------------------------

    def pwd(self):

        if self.filesystem:

            return self.filesystem.get_current_path()

        return "/"



    def ls(self, path=None):

        if not self.filesystem:

            return ""


        try:

            if path is None or path == "":

                contents = (
                    self.filesystem.current_directory
                    .list_contents()
                )
                print(
                    "[VOS API] ls contents:",
                    contents
                )

            else:

                contents = (
                    self.filesystem.list_directory(path)
                )


            if contents is None:

                return ""


            # New filesystem format:
            # {
            #     "folders": [],
            #     "files": []
            # }

            if isinstance(contents, dict):

                folders = contents.get(
                    "folders",
                    []
                )

                files = contents.get(
                    "files",
                    []
                )

                return "\n".join(
                    folders + files
                )


            # Old list format

            if isinstance(contents, list):

                return "\n".join(contents)


        except Exception as error:

            print(
                "[VOS API] ls error:",
                error
            )


        return ""



    def cd(self, path):

        if not self.filesystem:

            return False


        print(
            "[VOS API] cd request:",
            path
        )


        try:

            success = (
                self.filesystem
                .change_directory(path)
            )


            print(
                "[VOS API] cd result:",
                success
            )


            return success


        except Exception as error:

            print(
                "[VOS API] cd error:",
                error
            )

            return False



    def mkdir(self, path):

        if not self.filesystem:

            return False


        print(
            "[VOS API] mkdir request:",
            path
        )


        try:

            success = (
                self.filesystem
                .create_folder(path)
            )


            print(
                "[VOS API] mkdir result:",
                success
            )


            return success


        except Exception as error:

            print(
                "[VOS API] mkdir error:",
                error
            )

            return False



    def touch(self, path):

        if not self.filesystem:

            return False


        print(
            "[VOS API] touch request:",
            path
        )


        try:

            success = (
                self.filesystem
                .create_file(path)
            )


            print(
                "[VOS API] touch result:",
                success
            )


            return success


        except Exception as error:

            print(
                "[VOS API] touch error:",
                error
            )

            return False

    def write(self, path, content):

        if not self.filesystem:
            return False


        print(
            "[VOS API] write request:",
            path
        )


        try:

            success = self.filesystem.write_file(
                path,
                content
            )


            print(
                "[VOS API] write result:",
                success
            )


            return success


        except Exception as error:

            print(
                "[VOS API] write error:",
                error
            )

            return False

    def cat(self, path):

        if not self.filesystem:
            return None

        print(
            "[VOS API] cat request:",
            path
        )

        try:

            content = (
                self.filesystem
                .read_file(path)
            )

            print(
                "[VOS API] cat result:",
                content
            )

            return content

        except Exception as error:

            print(
                "[VOS API] cat error:",
                error
            )

            return None

    def tree(self):

        if not self.filesystem:
            return ""


        print(
            "[VOS API] tree request"
        )


        try:

            lines = self.filesystem.get_tree()


            result = "\n".join(
                lines
            )


            print(
                "[VOS API] tree result:",
                result
            )


            return result


        except Exception as error:

            print(
                "[VOS API] tree error:",
                error
            )

            return ""


    def rm(self, path):

        if not self.filesystem:
            return False

        print(
            "[VOS API] rm request:",
            path
        )

        try:

            success = self.filesystem.delete_file(
                path
            )

            print(
                "[VOS API] rm result:",
                success
            )

            return success

        except Exception as error:

            print(
                "[VOS API] rm error:",
                error
            )

            return False
    
    def rmdir(self, path):

        if not self.filesystem:
            return False


        print(
            "[VOS API] rmdir request:",
            path
        )


        try:

            success = self.filesystem.delete_folder(
                path
            )


            print(
                "[VOS API] rmdir result:",
                success
            )


            return success


        except Exception as error:

            print(
                "[VOS API] rmdir error:",
                error
            )

            return False

    def mv(self, source, destination):

        if not self.filesystem:
            return False


        print(
            "[VOS API] mv request:",
            source,
            "->",
            destination
        )


        try:

            success = self.filesystem.move_file(
                source,
                destination
            )


            print(
                "[VOS API] mv result:",
                success
            )


            return success


        except Exception as error:

            print(
                "[VOS API] mv error:",
                error
            )

            return False
        
    def cp(self, source, destination):

        if not self.filesystem:
            return False


        print(
            "[VOS API] cp request:",
            source,
            "->",
            destination
        )


        try:

            success = self.filesystem.copy_file(
                source,
                destination
            )


            print(
                "[VOS API] cp result:",
                success
            )


            return success


        except Exception as error:

            print(
                "[VOS API] cp error:",
                error
            )

            return False


# Global API instance

vos_api = VOSAPI()