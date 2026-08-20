from filesystem.filesystem import FileSystem

fs = FileSystem()

print("\n==============================")
print(" FOLDER OPERATIONS TEST")
print("==============================")

print("\n--- CREATING FOLDERS ---")

result = fs.create_folder(
    "/users/guest/Documents/Projects"
)

print("Projects result:", result)

result = fs.create_folder(
    "/users/guest/Documents/Projects/VOS"
)

print("VOS result:", result)

print("\n--- AFTER FOLDER CREATION ---")

print(fs.get_tree())

print("\n--- CHECKING FOLDER ---")

folder = fs._get_folder(
    "/users/guest/Documents/Projects/VOS"
)

print("Folder found:", folder is not None)

print("\n--- DELETING EMPTY FOLDER ---")

result = fs.delete_folder(
    "/users/guest/Documents/Projects/VOS"
)

print("Delete VOS result:", result)

print("\n--- AFTER DELETING VOS ---")

print(fs.get_tree())

print("\n--- CREATING NON-EMPTY FOLDER ---")

fs.create_folder(
    "/users/guest/Documents/TestFolder"
)

fs.create_file(
    "/users/guest/Documents/TestFolder/test.txt",
    "This file prevents the folder from being deleted."
)

print("\n--- BEFORE NON-EMPTY DELETE ---")

print(fs.get_tree())

print("\n--- DELETING NON-EMPTY FOLDER ---")

result = fs.delete_folder(
    "/users/guest/Documents/TestFolder"
)

print("Delete result:", result)

print("\n--- CHECKING NON-EMPTY FOLDER ---")

folder = fs._get_folder(
    "/users/guest/Documents/TestFolder"
)

print("Folder still exists:", folder is not None)

file_content = fs.read_file(
    "/users/guest/Documents/TestFolder/test.txt"
)

print("File still exists:", file_content)

print("\n--- DELETING FILE INSIDE FOLDER ---")

result = fs.delete_file(
    "/users/guest/Documents/TestFolder/test.txt"
)

print("Delete file result:", result)

print("\n--- DELETING NOW-EMPTY FOLDER ---")

result = fs.delete_folder(
    "/users/guest/Documents/TestFolder"
)

print("Delete folder result:", result)

print("\n--- CREATING PERSISTENCE TEST FOLDER ---")

result = fs.create_folder(
    "/users/guest/Documents/PersistentFolder"
)

print("Create result:", result)

print("\n--- SAVING FILESYSTEM ---")

fs.save()

print("\n--- LOADING NEW FILESYSTEM INSTANCE ---")

fs2 = FileSystem()

print("\n--- CHECKING PERSISTENCE ---")

folder = fs2._get_folder(
    "/users/guest/Documents/PersistentFolder"
)

print("Persistent folder exists:", folder is not None)

print("\n--- FINAL TREE ---")

print(fs2.get_tree())

print("\n==============================")
print(" TEST COMPLETE")
print("==============================")
