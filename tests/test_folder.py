from filesystem.filesystem import FileSystem


fs = FileSystem()


print("\n==============================")
print(" FOLDER OPERATIONS TEST")
print("==============================")


# --------------------------------------------------
# 1. CREATE FOLDERS
# --------------------------------------------------

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


# --------------------------------------------------
# 2. CHECK FOLDER EXISTS
# --------------------------------------------------

print("\n--- CHECKING FOLDER ---")

folder = fs._get_folder(
    "/users/guest/Documents/Projects/VOS"
)

print("Folder found:", folder is not None)


# --------------------------------------------------
# 3. DELETE EMPTY FOLDER
# --------------------------------------------------

print("\n--- DELETING EMPTY FOLDER ---")

result = fs.delete_folder(
    "/users/guest/Documents/Projects/VOS"
)

print("Delete VOS result:", result)


print("\n--- AFTER DELETING VOS ---")

print(fs.get_tree())


# --------------------------------------------------
# 4. CREATE NON-EMPTY FOLDER
# --------------------------------------------------

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


# --------------------------------------------------
# 5. TRY TO DELETE NON-EMPTY FOLDER
# --------------------------------------------------

print("\n--- DELETING NON-EMPTY FOLDER ---")

result = fs.delete_folder(
    "/users/guest/Documents/TestFolder"
)

print("Delete result:", result)


# --------------------------------------------------
# 6. VERIFY NON-EMPTY FOLDER STILL EXISTS
# --------------------------------------------------

print("\n--- CHECKING NON-EMPTY FOLDER ---")

folder = fs._get_folder(
    "/users/guest/Documents/TestFolder"
)

print("Folder still exists:", folder is not None)

file_content = fs.read_file(
    "/users/guest/Documents/TestFolder/test.txt"
)

print("File still exists:", file_content)


# --------------------------------------------------
# 7. DELETE FILE FIRST
# --------------------------------------------------

print("\n--- DELETING FILE INSIDE FOLDER ---")

result = fs.delete_file(
    "/users/guest/Documents/TestFolder/test.txt"
)

print("Delete file result:", result)


# --------------------------------------------------
# 8. NOW DELETE EMPTY FOLDER
# --------------------------------------------------

print("\n--- DELETING NOW-EMPTY FOLDER ---")

result = fs.delete_folder(
    "/users/guest/Documents/TestFolder"
)

print("Delete folder result:", result)


# --------------------------------------------------
# 9. PERSISTENCE TEST
# --------------------------------------------------

print("\n--- CREATING PERSISTENCE TEST FOLDER ---")

result = fs.create_folder(
    "/users/guest/Documents/PersistentFolder"
)

print("Create result:", result)


print("\n--- SAVING FILESYSTEM ---")

fs.save()


# --------------------------------------------------
# 10. LOAD NEW FILESYSTEM INSTANCE
# --------------------------------------------------

print("\n--- LOADING NEW FILESYSTEM INSTANCE ---")

fs2 = FileSystem()


# --------------------------------------------------
# 11. VERIFY PERSISTENCE
# --------------------------------------------------

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
