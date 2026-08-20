import json
import os

class VirtualDisk:
    def __init__(self,
                 disk_image_file="vos_disk.img",
                 disk_size=1024 * 1024,
                 block_size=4096):
        self.disk_image_file = disk_image_file
        self.disk_size = disk_size
        self.block_size = block_size

        self.total_blocks = self.disk_size // self.block_size
        self.block_offsets = [i * self.block_size for i in range(self.total_blocks)]

        self.block_used = [0]
        self.block_free = list(range(1, self.total_blocks))
        self.file_table = {}

        self.load()

    def load(self):
        if not os.path.exists(self.disk_image_file):
            return
        data = self.read_raw_block(0)
        if data:
            clean_json = data.rstrip(b"\x00").decode("utf-8")
            if clean_json:
                self.file_table = json.loads(clean_json)
                self.block_used = [0]
                for file_info in self.file_table.values():
                    self.block_used.extend(file_info["blocks"])
                self.block_free = [b for b in range(1, self.total_blocks) if b not in self.block_used]

    def save(self):
        metadata = json.dumps(self.file_table)
        self.write_raw_block(0, metadata)

    def allocate_block(self):
        if not self.block_free:
            raise RuntimeError("No free blocks available.")
        allocated_block = self.block_free.pop(0)
        self.block_used.append(allocated_block)
        return allocated_block

    def write_raw_block(self, block_index, data):
        if not os.path.exists(self.disk_image_file):
            with open(self.disk_image_file, "wb") as disk:
                disk.write(b"\x00" * self.disk_size)

        binary_data = data.encode("utf-8") if isinstance(data, str) else data

        if len(binary_data) > self.block_size:
            raise ValueError("Data exceeds single block size limit.")

        padded_data = binary_data.ljust(self.block_size, b"\x00")
        with open(self.disk_image_file, "r+b") as disk:
            disk.seek(self.block_offsets[block_index])
            disk.write(padded_data)

    def read_raw_block(self, block_index):
        if not os.path.exists(self.disk_image_file):
            raise FileNotFoundError("Virtual disk image does not exist yet.")

        with open(self.disk_image_file, "rb") as disk:
            disk.seek(self.block_offsets[block_index])
            return disk.read(self.block_size)

    def read_file(self, file_name):
        if file_name not in self.file_table:
            raise KeyError(f"File '{file_name}' not found.")
        file_info = self.file_table[file_name]
        raw_bytes = b"".join(self.read_raw_block(b) for b in file_info["blocks"])
        return raw_bytes[:file_info["size"]]

    def create_file(self, file_name, content):
        if file_name in self.file_table:
            raise FileExistsError(f"File '{file_name}' already exists.")

        binary_content = content.encode("utf-8") if isinstance(content, str) else content

        if len(binary_content) == 0:
            block_num = self.allocate_block()
            self.write_raw_block(block_num, b"")
            self.file_table[file_name] = {"blocks": [block_num], "size": 0}
            self.save()
            return

        required_blocks = (len(binary_content) + self.block_size - 1) // self.block_size
        if required_blocks > len(self.block_free):
            raise MemoryError("Not enough disk space to write file.")

        allocated_chunks = []
        for offset in range(0, len(binary_content), self.block_size):
            chunk = binary_content[offset: offset + self.block_size]
            block_num = self.allocate_block()
            allocated_chunks.append(block_num)
            self.write_raw_block(block_num, chunk)

        self.file_table[file_name] = {"blocks": allocated_chunks, "size": len(binary_content)}
        self.save()

    def copy_file(self, file_name, filename):
        data = self.read_file(file_name)
        self.create_file(filename, data)

    def move_file(self, file_name, filename):
        data = self.read_file(file_name)
        self.delete_file(file_name)
        self.create_file(filename, data)

    def delete_file(self, file_name):
        if file_name not in self.file_table:
            raise KeyError(f"File '{file_name}' does not exist.")

        file_info = self.file_table.pop(file_name)
        for block_num in file_info["blocks"]:
            self.block_used.remove(block_num)
            self.block_free.append(block_num)
            self.write_raw_block(block_num, b"")
        self.block_free.sort()
        self.save()
        return True

if __name__ == "__main__":
    vdisk = VirtualDisk()
    print("Block size:", vdisk.block_size)
    print("Total blocks:", vdisk.read_file("Registry"))
    print("Blocks used: ", vdisk.block_used)

    choice = input("Read = 1, Write = 2, Delete = 3\nChoice: ").strip()

    if choice == "1":
        file_name = input("Enter file name: ")
        try:
            content = vdisk.read_file(file_name)
            print(f"Content: {content.decode('utf-8')}")
        except KeyError as e:
            print(e)

    elif choice == "2":
        file_name = input("Enter file name: ")
        text = input("Enter content: ")
        try:
            vdisk.create_file(file_name, text)
            print(f"File '{file_name}' written successfully.")
        except (FileExistsError, MemoryError) as e:
            print(e)

    elif choice == "3":
        file_name = input("Enter file name: ")
        try:
            vdisk.delete_file(file_name)
            print(f"File '{file_name}' deleted successfully.")
        except KeyError as e:
            print(e)
