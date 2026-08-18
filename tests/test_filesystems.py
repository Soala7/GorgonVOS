from filesystem.filesystem import FileSystem


fs = FileSystem()

BASE = "/users/guest/Documents"

FILE_A = BASE + "/edge_test.txt"
FILE_B = BASE + "/existing.txt"
COPY_FILE = BASE + "/edge_copy.txt"
MOVE_FILE = "/users/guest/Downloads/edge_test.txt"
RENAMED_FILE = BASE + "/renamed_edge.txt"

print("\n==============================")
print(" FILESYSTEM EDGE CASE TEST")
print("==============================")


# ==================================================
# 1. CREATE FILE
# ==================================================

print("\n--- 1. CREATE FILE ---")

result = fs.create_file(
    FILE_A,
    "Edge case test file."
)

print("Result:", result)


# ==================================================
# 2. CREATE EXISTING FILE
# ==================================================

print("\n--- 2. CREATE EXISTING FILE ---")

result = fs.create_file(
    FILE_A,
    "This should not replace the file."
)

print("Result:", result)


# ==================================================
# 3. CREATE SECOND FILE
# ==================================================

print("\n--- 3. CREATE SECOND FILE ---")

result = fs.create_file(
    FILE_B,
    "Existing destination file."
)

print("Result:", result)


# ==================================================
# 4. READ FILE
# ==================================================

print("\n--- 4. READ FILE ---")

print("Content:", fs.read_file(FILE_A))


# ==================================================
# 5. READ NONEXISTENT FILE
# ==================================================

print("\n--- 5. READ NONEXISTENT FILE ---")

print(
    "Content:",
    fs.read_file(BASE + "/does_not_exist.txt")
)


# ==================================================
# 6. COPY FILE
# ==================================================

print("\n--- 6. COPY FILE ---")

result = fs.copy_file(
    FILE_A,
    COPY_FILE
)

print("Result:", result)
print("Copied content:", fs.read_file(COPY_FILE))


# ==================================================
# 7. COPY TO EXISTING FILE
# ==================================================

print("\n--- 7. COPY TO EXISTING FILE ---")

result = fs.copy_file(
    FILE_A,
    FILE_B
)

print("Result:", result)
print("Destination content:", fs.read_file(FILE_B))


# ==================================================
# 8. COPY NONEXISTENT FILE
# ==================================================

print("\n--- 8. COPY NONEXISTENT FILE ---")

result = fs.copy_file(
    BASE + "/does_not_exist.txt",
    BASE + "/bad_copy.txt"
)

print("Result:", result)


# ==================================================
# 9. CREATE MOVE DESTINATION FOLDER
# ==================================================

print("\n--- 9. MOVE TEST SETUP ---")

result = fs.create_folder(
    "/users/guest/Downloads"
)

print("Downloads folder result:", result)


# ==================================================
# 10. MOVE FILE
# ==================================================

print("\n--- 10. MOVE FILE ---")

result = fs.move_file(
    FILE_A,
    MOVE_FILE
)

print("Result:", result)

print(
    "Old location:",
    fs.read_file(FILE_A)
)

print(
    "New location:",
    fs.read_file(MOVE_FILE)
)


# ==================================================
# 11. MOVE NONEXISTENT FILE
# ==================================================

print("\n--- 11. MOVE NONEXISTENT FILE ---")

result = fs.move_file(
    BASE + "/does_not_exist.txt",
    "/users/guest/Downloads/bad_move.txt"
)

print("Result:", result)


# ==================================================
# 12. MOVE TO EXISTING FILE
# ==================================================

print("\n--- 12. MOVE TO EXISTING FILE ---")

result = fs.move_file(
    MOVE_FILE,
    FILE_B
)

print("Result:", result)

print(
    "Source still exists:",
    fs.read_file(MOVE_FILE)
)

print(
    "Destination unchanged:",
    fs.read_file(FILE_B)
)


# ==================================================
# 13. RENAME FILE
# ==================================================

print("\n--- 13. RENAME FILE ---")

result = fs.rename_file(
    COPY_FILE,
    "renamed_edge.txt"
)

print("Result:", result)

print(
    "Old name:",
    fs.read_file(COPY_FILE)
)

print(
    "New name:",
    fs.read_file(RENAMED_FILE)
)


# ==================================================
# 14. RENAME NONEXISTENT FILE
# ==================================================

print("\n--- 14. RENAME NONEXISTENT FILE ---")

result = fs.rename_file(
    BASE + "/does_not_exist.txt",
    "bad_name.txt"
)

print("Result:", result)


# ==================================================
# 15. RENAME TO EXISTING FILE
# ==================================================

print("\n--- 15. RENAME TO EXISTING FILE ---")

result = fs.rename_file(
    RENAMED_FILE,
    "existing.txt"
)

print("Result:", result)

print(
    "Original file still exists:",
    fs.read_file(RENAMED_FILE)
)

print(
    "Existing destination:",
    fs.read_file(FILE_B)
)


# ==================================================
# 16. DELETE NONEXISTENT FILE
# ==================================================

print("\n--- 16. DELETE NONEXISTENT FILE ---")

result = fs.delete_file(
    BASE + "/does_not_exist.txt"
)

print("Result:", result)


# ==================================================
# 17. CREATE NON-EMPTY FOLDER
# ==================================================

print("\n--- 17. NON-EMPTY FOLDER TEST ---")

TEST_FOLDER = BASE + "/EdgeFolder"

result = fs.create_folder(TEST_FOLDER)

print("Folder result:", result)

result = fs.create_file(
    TEST_FOLDER + "/inside.txt",
    "This prevents folder deletion."
)

print("File result:", result)


# ==================================================
# 18. DELETE NON-EMPTY FOLDER
# ==================================================

print("\n--- 18. DELETE NON-EMPTY FOLDER ---")

result = fs.delete_folder(TEST_FOLDER)

print("Result:", result)

print(
    "Folder still exists:",
    fs._get_folder(TEST_FOLDER) is not None
)


# ==================================================
# 19. DELETE FILE INSIDE FOLDER
# ==================================================

print("\n--- 19. DELETE FILE INSIDE FOLDER ---")

result = fs.delete_file(
    TEST_FOLDER + "/inside.txt"
)

print("Result:", result)


# ==================================================
# 20. DELETE NOW-EMPTY FOLDER
# ==================================================

print("\n--- 20. DELETE NOW-EMPTY FOLDER ---")

result = fs.delete_folder(TEST_FOLDER)

print("Result:", result)

print(
    "Folder exists:",
    fs._get_folder(TEST_FOLDER) is not None
)


# ==================================================
# 21. FINAL FILESYSTEM STATE
# ==================================================

print("\n--- FINAL FILE TABLE ---")

print(fs.disk.file_table)

print("\n--- USED BLOCKS ---")

print(fs.disk.block_used)

print("\n--- FREE BLOCKS ---")

print(fs.disk.block_free)


# ==================================================
# 22. CLEANUP
# ==================================================

print("\n--- CLEANING UP TEST FILES ---")

cleanup_files = [
    FILE_B,
    MOVE_FILE,
    RENAMED_FILE,
]

for path in cleanup_files:
    result = fs.delete_file(path)
    print(path, "->", result)


print("\n--- FINAL STATE AFTER CLEANUP ---")

print("File table:", fs.disk.file_table)
print("Used blocks:", fs.disk.block_used)
print("Free blocks:", fs.disk.block_free)


print("\n==============================")
print(" EDGE CASE TEST COMPLETE")
print("==============================")


