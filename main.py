import os
import glob
import tkinter as tk
from tkinter import messagebox
import requests
# import subprocess
# import webbrowser
import re
from pyfiglet import Figlet

def find_all_games():
    stplug_path = "C:\\Program Files (x86)\\Steam\\config\\stplug-in\\"
    
    if os.path.exists(stplug_path):
        for file in os.listdir(stplug_path):
            if file.endswith(".lua"):
                games.append(file.replace(".lua", ""))
    
    if not games:
        print("No games found!")
        messagebox.showerror("Error", "No games found in Steam config folder!")
        return
        
    game_listbox.delete(0, tk.END)
    print("Sending requests to Steam API for game names...")
    for game in games:
        game_name = get_game_name(game)
        game_names[game] = game_name if game_name else game
        game_listbox.insert(tk.END, f"{game_name} | {game}" if game_name else game)
    print("Done.")

def get_depot_ids_from_lua(game_id):
    """
    Чете .lua файл от stplug-in за даден game_id и връща списък с depot ID-та.
    """
    base_path = "C:\\Program Files (x86)\\Steam\\config\\stplug-in"
    file_path = os.path.join(base_path, f"{game_id}.lua")

    if not os.path.exists(file_path):
        print(f"Lua file not found: {file_path}")
        return []

    depots = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            # търсим редове като addappid(1030301, ...
            match = re.match(r"addappid\((\d+)", line)
            if match:
                depot_id = match.group(1)
                depots.append(depot_id)
                print(f"Found game or depot ID: {depot_id}")

    return depots

def find_files():
    # selected_game = game_listbox.get(tk.ACTIVE)
    selected_index = game_listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error", "No game selected")
        return
    print("Finding files for selected game...")
    
    files_to_delete.clear()
    listbox.delete(0, tk.END)
    selected_game_id = games[selected_index[0]]
    lua_file_path = f"C:\\Program Files (x86)\\Steam\\config\\stplug-in\\{selected_game_id}.lua"
    listbox.insert(tk.END, lua_file_path)
    files_to_delete.append(lua_file_path)

    depot_ids = get_depot_ids_from_lua(selected_game_id)

    for depot_id in depot_ids:
        depot_files = glob.glob(f"C:\\Program Files (x86)\\Steam\\config\\depotcache\\{depot_id}_*.manifest")
        for depot_file in depot_files:
            print("Found depot file:", depot_file)
            files_to_delete.append(depot_file)
            listbox.insert(tk.END, depot_file)
    
    # if os.path.exists(game_install_path):
    #     open_game_folder_button.config(state=tk.NORMAL)
    # else:
    #     open_game_folder_button.config(state=tk.DISABLED)
    print("Checking if game is still installed in Steam...")
    check_if_game_installed(selected_game_id)

def check_if_game_installed(game_id):
    manifest_path = f"C:\\Program Files (x86)\\Steam\\steamapps\\appmanifest_{game_id}.acf"
    if os.path.exists(manifest_path):
        print(f"Game {game_id} is still installed.")
        # messagebox.showerror("Error", f"Game {game_id} is still installed in Steam. Please uninstall it first.")
        return
    print(f"Game {game_id} is not installed in Steam.")
def delete_files():
    selected_index = game_listbox.curselection()
    for file in files_to_delete:
        try:
            print(f"Deleting file: {file}")
            os.remove(file)
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't delete {file}: {e}")
    messagebox.showinfo("Success", "Selected files deleted!")
    # messagebox.showwarning("Warning", "Please restart Steam to ensure all changes take effect.")
    result = messagebox.askyesno("Restart Steam", "Do you want to restart Steam now?")
    if result:
        restart_steam()
    game_listbox.delete(selected_index)
    del games[selected_index[0]]
    listbox.delete(0, tk.END)
    files_to_delete.clear()

def get_game_name(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    r = requests.get(url)
    data = r.json()
    if data[str(app_id)]["success"]:
        return data[str(app_id)]["data"]["name"]
    return None

def restart_steam():
    os.system("taskkill /f /im steam.exe")
    os.startfile("C:\\Program Files (x86)\\Steam\\Steam.exe")

# def open_game_folder():
#     selected_game = game_listbox.get(tk.ACTIVE)
#     game_install_path = f"C:\\Program Files (x86)\\Steam\\steamapps\\common\\{selected_game}"  
#     if os.path.exists(game_install_path):
#         webbrowser.open(game_install_path)

root = tk.Tk()
root.title("Steamtools Game Uninstaller")
root.geometry("400x485")

tk.Button(root, text="Find Games", command=find_all_games).pack()

game_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=60, height=10)
game_listbox.pack()

tk.Button(root, text="Find Files", command=find_files).pack()

listbox = tk.Listbox(root, width=60, height=15, selectmode=tk.NONE)
listbox.pack()

# tk.Button(root, text="Delete All Files", command=delete_files).pack()
frame = tk.Frame(root)
frame.pack()
tk.Button(frame, text="Delete All Files", command=delete_files).pack(side=tk.LEFT)
tk.Button(frame, text="Restart Steam", command=restart_steam).pack(side=tk.LEFT)

# open_game_folder_button = tk.Button(root, text="Open Game Folder", command=open_game_folder, state=tk.DISABLED)
# open_game_folder_button.pack()

files_to_delete = []
games = []
game_names = {}

print(Figlet(font='doom').renderText('Steamtools Game Uninstaller'))
print("Tool made by GreeningSiren and N1ghtMare.")
messagebox.showinfo("Credits", "Created by GreeningSiren and 𝓝1𝓰𝓱𝓽𝓜𝓪𝓻𝓮. Contact on Discord for more information.")
# messagebox.showwarning("Warning", "Please delete the selected game from Steam first to avoid issues.")

root.mainloop()
