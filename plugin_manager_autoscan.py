import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


class PluginManager(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Plugin Manager")
        self.master.geometry("400x150")
        self.create_widgets()

        # Default plugin directories to scan
        self.default_plugin_dirs = [
            "/Library/Audio/Plug-Ins/VST",
            "/Library/Audio/Plug-Ins/VST3",
            "/Library/Audio/Plug-Ins/Components",
            "/Library/Application Support/Avid/Audio/Plug-Ins",
            os.path.expanduser("~/Library/Audio/Plug-Ins/VST"),
            os.path.expanduser("~/Library/Audio/Plug-Ins/VST3"),
            os.path.expanduser("~/Library/Audio/Plug-Ins/Components"),
            os.path.expanduser("~/Library/Application Support/Avid/Audio/Plug-Ins"),
        ]
        self.file_extensions = (".vst3", ".vst", ".component", ".aaxplugin")

    def create_widgets(self):
        self.scan_add_button = tk.Button(self.master, text="Scan and Add Plugins", command=self.scan_and_add_plugins)
        self.scan_add_button.pack(pady=10)

        self.destination_label = tk.Label(self.master, text="Destination folder:")
        self.destination_label.pack()

        self.destination_path = tk.StringVar()
        self.destination_path.set(os.path.expanduser("~/Desktop"))
        self.destination_entry = tk.Entry(self.master, textvariable=self.destination_path)
        self.destination_entry.pack()

        self.choose_folder_button = tk.Button(self.master, text="Choose folder", command=self.choose_destination_folder)
        self.choose_folder_button.pack(pady=10)

    def choose_destination_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.destination_path.set(folder_path)

    def scan_and_add_plugins(self):
        print("Scanning and adding plugins...")
        for plugins_dir in self.default_plugin_dirs:
            print(f"Checking directory: {plugins_dir}")
            if os.path.isdir(plugins_dir):
                for root, _, files in os.walk(plugins_dir):
                    for file in files:
                        if file.endswith(self.file_extensions):
                            plugin_path = os.path.join(root, file)
                            print(f"Found file: {file}")
                            self.add_plugin(plugin_path)
        messagebox.showinfo("Success", "Plugins found in the default locations have been added to the FlashDrivePlugins folder.")

    def add_plugin(self, plugin_path):
        destination_folder = os.path.join(self.destination_path.get(), "FlashDrivePlugins")
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        shutil.copy2(plugin_path, destination_folder)


if __name__ == "__main__":
    root = tk.Tk()
    app = PluginManager(master=root)
    app.mainloop()
