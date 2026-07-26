import sys
import os


# Add VOS root directory to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from shell_bridge import ShellBridge
from bridge.vos_api import vos_api
from filesystem.filesystem import FileSystem


# Create VOS filesystem
filesystem = FileSystem()


# Connect filesystem to VOS API
vos_api.register_filesystem(
    filesystem
)


# Start shell bridge
shell = ShellBridge()


print("\n--- PWD TEST ---")
print(shell.execute("pwd"))


print("\n--- LS TEST ---")
print(shell.execute("ls"))


print("\n--- CD TEST ---")
print(shell.execute("cd home"))


print("\n--- PWD AFTER CD ---")
print(shell.execute("pwd"))


print("\n--- MKDIR TEST ---")
print(shell.execute("mkdir test"))


print("\n--- LS AFTER MKDIR ---")
print(shell.execute("ls"))


print("\n--- TOUCH TEST ---")
print(shell.execute("touch hello.txt"))


print("\n--- FINAL LS ---")
print(shell.execute("ls"))

print("\n--- WRITE TEST ---")
print(shell.execute("write hello.txt Hello World From VOS"))

print("\n--- CAT TEST ---")
print(shell.execute("cat hello.txt"))

print("\n--- RMDIR TEST ---")
print(shell.execute("mkdir empty"))
print(shell.execute("ls"))
print(shell.execute("rmdir empty"))
print(shell.execute("ls"))
print("\n--- TREE TEST ---")
print(shell.execute("tree"))

print("\n--- MV TEST ---")

print(shell.execute("touch old.txt"))

print(shell.execute("write old.txt Hello MV"))

print(shell.execute("mv old.txt new.txt"))

print(shell.execute("ls"))

print(shell.execute("cat new.txt"))

print("\n--- CP TEST ---")

print(shell.execute("touch original.txt"))

print(shell.execute("write original.txt COPY TEST"))

print(shell.execute("cp original.txt backup.txt"))

print(shell.execute("ls"))

print(shell.execute("cat backup.txt"))

shell.shutdown()