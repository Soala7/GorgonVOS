"""
File: VOS/bridge/shell_bridge.py

Bridge between Python VOS services and the C shell.
"""

import ctypes
import os

from bridge.vos_api import vos_api


PWD_CALLBACK = ctypes.CFUNCTYPE(
    None,
    ctypes.POINTER(ctypes.c_char),
    ctypes.c_int
)


LS_CALLBACK = ctypes.CFUNCTYPE(
    None,
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_char),
    ctypes.c_int
)


CD_CALLBACK = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_char_p
)


MKDIR_CALLBACK = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_char_p
)

TOUCH_CALLBACK = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_char_p
)

WRITE_CALLBACK = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_char_p
)

CAT_CALLBACK = ctypes.CFUNCTYPE(
    None,
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_char),
    ctypes.c_int
)

RM_CALLBACK = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_char_p
)

RMDIR_CALLBACK = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_char_p
)

TREE_CALLBACK = ctypes.CFUNCTYPE(
    None,
    ctypes.POINTER(ctypes.c_char),
    ctypes.c_int
)

MV_CALLBACK = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_char_p
)

CP_CALLBACK = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_char_p
)

class ShellBridge:
    def __init__(self, service_manager):

        self.service_manager = service_manager

        shell_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "apps",
            "terminal",
            "shell",
            "libvos_shell.so"
        )


        self.shell = ctypes.CDLL(
            os.path.abspath(shell_path)
        )


        # Shell API

        self.shell.vos_shell_init.restype = None
        self.shell.vos_shell_execute.restype = ctypes.c_char_p
        self.shell.vos_shell_shutdown.restype = None


        self.shell.vos_shell_execute.argtypes = [
            ctypes.c_char_p
        ]


        # Callback registration

        self.shell.host_register_pwd.argtypes = [
            PWD_CALLBACK
        ]

        self.shell.host_register_ls.argtypes = [
            LS_CALLBACK
        ]

        self.shell.host_register_cd.argtypes = [
            CD_CALLBACK
        ]

        self.shell.host_register_mkdir.argtypes = [
            MKDIR_CALLBACK
        ]

        self.shell.host_register_touch.restype = None
        self.shell.host_register_touch.argtypes = [
            TOUCH_CALLBACK
        ]

        self.shell.host_register_write.argtypes = [
            WRITE_CALLBACK
        ]

        self.shell.host_register_cat.restype = None
        self.shell.host_register_cat.argtypes = [
            CAT_CALLBACK
        ]

        self.shell.host_register_rm.argtypes = [
            RM_CALLBACK
        ]

        self.shell.host_register_tree.argtypes = [
            TREE_CALLBACK
        ]

        self.shell.host_register_mv.argtypes = [
            MV_CALLBACK
        ]

        self.shell.host_register_cp.argtypes = [
            CP_CALLBACK
        ]

        self.shell.vos_shell_init()


        self._register_callbacks()



    def _register_callbacks(self):


        def pwd_callback(buffer, size):

            print("[HOST CALLBACK] pwd called")

            data = vos_api.pwd().encode()


            ctypes.memset(
                buffer,
                0,
                size
            )


            ctypes.memmove(
                buffer,
                data,
                min(
                    len(data),
                    size - 1
                )
            )



        def ls_callback(path, buffer, size):

            print("[HOST CALLBACK] ls called")


            path_value = (
                path.decode()
                if path
                else None
            )


            data = vos_api.ls(
                path_value
            ).encode()


            ctypes.memset(
                buffer,
                0,
                size
            )


            ctypes.memmove(
                buffer,
                data,
                min(
                    len(data),
                    size - 1
                )
            )



        def cd_callback(path):

            print("[HOST CALLBACK] cd called")


            success = vos_api.cd(
                path.decode()
            )


            return 1 if success else 0

        def mkdir_callback(path):

            print("[HOST CALLBACK] mkdir called")


            success = vos_api.mkdir(
                path.decode()
            )


            return 1 if success else 0

        def touch_callback(path):

            print("[HOST CALLBACK] touch called")

            path_string = path.decode("utf-8")

            success = vos_api.touch(
                path_string
            )

            return 1 if success else 0

        def write_callback(path, content):

            print("[HOST CALLBACK] write called")


            path_string = path.decode("utf-8")

            content_string = content.decode("utf-8")


            success = vos_api.write(
                path_string,
                content_string
            )


            return 1 if success else 0

        def cat_callback(path, buffer, size):

            print("[HOST CALLBACK] cat called")

            path_string = path.decode("utf-8")

            content = vos_api.cat(path_string)

            if content is None:
                content = "File not found."

            data = content.encode()

            ctypes.memset(
                buffer,
                0,
                size
            )

            ctypes.memmove(
                buffer,
                data,
                min(
                    len(data),
                    size - 1
                )
            )

        def rm_callback(path):

            print("[HOST CALLBACK] rm called")

            path_string = path.decode("utf-8")

            success = vos_api.rm(
                path_string
            )

            return 1 if success else 0

        def rmdir_callback(path):

            print("[HOST CALLBACK] rmdir called")

            path_string = path.decode("utf-8")

            success = vos_api.rmdir(
                path_string
            )

            return 1 if success else 0

        def tree_callback(buffer, size):

            print("[HOST CALLBACK] tree called")


            data = vos_api.tree().encode()


            ctypes.memset(
                buffer,
                0,
                size
            )


            ctypes.memmove(
                buffer,
                data,
                min(
                    len(data),
                    size - 1
                )
            )

        def mv_callback(source, destination):

            print("[HOST CALLBACK] mv called")


            source_string = source.decode("utf-8")
            destination_string = destination.decode("utf-8")


            success = vos_api.mv(
                source_string,
                destination_string
            )


            return 1 if success else 0

        def cp_callback(source, destination):

            print("[HOST CALLBACK] cp called")


            source_string = source.decode("utf-8")
            destination_string = destination.decode("utf-8")


            success = vos_api.cp(
                source_string,
                destination_string
            )


            return 1 if success else 0

        self.pwd_callback = PWD_CALLBACK(
            pwd_callback
        )

        self.ls_callback = LS_CALLBACK(
            ls_callback
        )

        self.cd_callback = CD_CALLBACK(
            cd_callback
        )

        self.mkdir_callback = MKDIR_CALLBACK(
            mkdir_callback
        )

        self.touch_callback = TOUCH_CALLBACK(
            touch_callback
        )

        self.write_callback = WRITE_CALLBACK(
            write_callback
        )

        self.cat_callback = CAT_CALLBACK(
            cat_callback
        )

        self.rm_callback = RM_CALLBACK(
            rm_callback
        )

        self.rmdir_callback = RMDIR_CALLBACK(
            rmdir_callback
        )

        self.tree_callback = TREE_CALLBACK(
            tree_callback
        )

        self.mv_callback = MV_CALLBACK(
            mv_callback
        )

        self.cp_callback = CP_CALLBACK(
            cp_callback
        )

        self.shell.host_register_pwd(
            self.pwd_callback
        )

        self.shell.host_register_ls(
            self.ls_callback
        )

        self.shell.host_register_cd(
            self.cd_callback
        )

        self.shell.host_register_mkdir(
            self.mkdir_callback
        )

        self.shell.host_register_touch(
            self.touch_callback
        )

        self.shell.host_register_write(
            self.write_callback
        )
        
        self.shell.host_register_cat(
            self.cat_callback
        )

        self.shell.host_register_rm(
            self.rm_callback
        )

        self.shell.host_register_rmdir(
            self.rmdir_callback
        )

        self.shell.host_register_tree(
            self.tree_callback
        )

        self.shell.host_register_mv(
            self.mv_callback
        )

        self.shell.host_register_cp(
            self.cp_callback
        )

    def execute(self, command):

        result = self.shell.vos_shell_execute(
            command.encode()
        )

        return result.decode()



    def shutdown(self):

        self.shell.vos_shell_shutdown()