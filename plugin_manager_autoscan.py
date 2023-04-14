import os
import shutil
import tkinter as tk
from tkinter import messagebox

class PluginManager:
    def __init__(self, flash_drive_path=None):
        self.flash_drive_path = flash_drive_path
        self.plugin_directories = []

        if self.flash_drive_path:
            self.flash_drive_plugins_dir = os.path.join(self.flash_drive_path, "FlashDrivePlugins")
            self.scan_directory(self.flash_drive_plugins_dir)
        else:
            self.default_vst3_dir = "/Library/Audio/Plug-Ins/VST3"
            self.default_vst2_dir = "/Library/Audio/Plug-Ins/VST"
            self.default_audio_unit_dir = "/Library/Audio/Plug-Ins/Components"
            self.default_aax_dir = "/Library/Application Support/Avid/Audio/Plug-Ins"

            self.scan_directory(self.default_vst3_dir)
            self.scan_directory(self.default_vst2_dir)
            self.scan_directory(self.default_audio_unit_dir)
            self.scan_directory(self.default_aax_dir)

        if not self.plugin_directories:
            messagebox.showinfo("No plugins found", "No plugins were found in the default locations.")

        if self.flash_drive_path:
            if not os.path.exists(self.flash_drive_plugins_dir):
                os.mkdir(self.flash_drive_plugins_dir)
                messagebox.showinfo("FlashDrivePlugins created", f"FlashDrivePlugins folder has been created in {self.flash_drive_path}")
            else:
                messagebox.showinfo("FlashDrivePlugins exists", f"FlashDrivePlugins folder already exists in {self.flash_drive_path}")

        self.master = tk.Tk()
        self.master.title("Plugin Manager")

        self.plugin_listbox = tk.Listbox(self.master)
        self.plugin_listbox.pack(expand=True, fill="both")

        self.copy_button = tk.Button(self.master, text="Copy to Flash Drive", command=self.copy_to_flash_drive)
        self.copy_button.pack(side="right")

        self.delete_button = tk.Button(self.master, text="Delete from Flash Drive", command=self.delete_from_flash_drive)
        self.delete_button.pack(side="left")

        for plugin_dir in self.plugin_directories:
            for root, dirs, files in os.walk(plugin_dir):
                for file in files:
                    if file.endswith((".aaxplugin", ".vst3", ".vst", ".component")):
                        self.plugin_listbox.insert(tk.END, os.path.join(root, file))

    def scan_directory(self, dir_path):
        if os.path.exists(dir_path):
            self.plugin_directories.append(dir_path)
            for root, dirs, files in os.walk(dir_path):
                for dir in dirs:
                    self.plugin_directories.append(os.path.join(root, dir))
        else:
            print(f"{dir_path} not found.")

    def copy_to_flash_drive(self):
        if not self.flash_drive_path:
            messagebox.showerror("Error", "No flash drive detected.")
            return

        selected_plugins = self.plugin_listbox.curselection()

        if not selected_plugins:
            messagebox.showerror("Error", "No plugins selected.")
            return

        for index in selected_plugins:
            plugin_path = self.plugin_listbox.get(index)
            plugin_name = os.path.basename(plugin_path)
            target_dir = os.path.join(self.flash_drive_plugins_dir, plugin_name)

            try:
                shutil.copytree(plugin_path, target_dir)
            except FileExistsError:
                shutil.rmtree(target_dir)
                shutil.copytree(plugin_path, target_dir)

        messagebox.showinfo("Copy Successful", "Selected plugins have been copied to the FlashDrivePlugins folder.")

    def delete_from_flash_drive(self):
        "if not self.flash_drive"
