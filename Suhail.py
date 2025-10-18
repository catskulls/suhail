import os, sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import random




playlist = []
music_root = ""
all_files = []


def resource_path(relative_path):
    try:     
        base_path = sys._MEIPASS
    except AttributeError:  
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def choose_root():
    global music_root, all_files
    folder = filedialog.askdirectory(title="Select your Walkman music folder")
    if folder:
        music_root = folder
        label_root.config(text=f"Root: {music_root}")
        btn_load.config(state="normal")

        all_files.clear()
        file_tree.delete(*file_tree.get_children())
        for root_dir, dirs, files in os.walk(music_root):
            for f in files:
                if f.lower().endswith(".mp3"):
                    full_path = os.path.join(root_dir, f)
                    all_files.append(full_path)
                    rel = os.path.relpath(full_path, music_root).replace("\\", "/")
                    file_tree.insert("", "end", values=(rel,), tags=("even" if len(all_files)%2==0 else "odd",))


def add_selected():
    for item_id in file_tree.selection():
        idx = file_tree.index(item_id)
        full_path = all_files[idx]
        if full_path not in playlist:
            playlist.append(full_path)
    update_playlist_tree()

def remove_selected():
    selected = list(playlist_tree.selection())
    selected.reverse()
    for item_id in selected:
        idx = playlist_tree.index(item_id)
        playlist.pop(idx)
    update_playlist_tree()

def move_up():
    selected = list(playlist_tree.selection())
    if not selected:
        return

    indices = [playlist_tree.index(item) for item in selected]

    for i in indices:
        if i == 0:
            continue
        playlist[i], playlist[i-1] = playlist[i-1], playlist[i]

    update_playlist_tree()

    children = playlist_tree.get_children()
    new_selection = []
    for i in indices:
        new_idx = i-1 if i > 0 else 0
        new_selection.append(children[new_idx])
    playlist_tree.selection_set(new_selection)

def move_down():
    selected = list(playlist_tree.selection())
    if not selected:
        return
    indices = [playlist_tree.index(item) for item in selected]

    for i in reversed(indices):
        if i == len(playlist)-1:
            continue
        playlist[i], playlist[i+1] = playlist[i+1], playlist[i]


    update_playlist_tree()

    children = playlist_tree.get_children()
    new_selection = []
    for i in indices:
        new_idx = i+1 if i < len(playlist)-1 else i
        new_selection.append(children[new_idx])
    playlist_tree.selection_set(new_selection)


def clear_playlist():
    if popup_yes_no("Oh, do you really want me to clear the playlist...?"):
        playlist.clear()
        playlist_tree.delete(*playlist_tree.get_children())

def update_playlist_tree():
    playlist_tree.delete(*playlist_tree.get_children())
    for i, track in enumerate(playlist):
        rel = os.path.relpath(track, music_root).replace("\\", "/")
        playlist_tree.insert("", "end", values=(rel,), tags=("even" if i % 2 == 0 else "odd",))

def save_playlist():
    if not playlist:
        popup_with_image(f"Oh, hold on a bit... You haven't selected any tracks yet. I can't really make a playlist for you...")
        return
    name = filedialog.asksaveasfilename(
        defaultextension=".m3u",
        initialdir=music_root,
        filetypes=[("M3U playlist", "*.m3u")],
        title="Save playlist as"
    )
    if not name:
        return
    try:
        selected_display = encoding_var.get()
        selected_encoding = ENCODING_OPTIONS[selected_display]
        with open(name, "w", encoding=selected_encoding, newline="\r\n") as f:

            f.write("#EXTM3U\r\n")
            for track in playlist:
                file_name = os.path.basename(track)
                rel_path = os.path.relpath(track, music_root).replace("/", "\\")
                f.write(f"#EXTINF:0,{file_name}\r\n")
                f.write(rel_path + "\r\n\r\n")


        popup_with_image(f"I've saved your playlist for you. \nYou can find it at \n{name}. Have fun!")
      
    except Exception as e:
        popup_with_image(f"Ah, something seems to have gone wrong... \nI wasn't able to save your playlist. I'm sorry. \n{e} ")
    

def popup_with_image(msg):
 
    win = tk.Toplevel()
    win.configure(bg="#1e1e1e")
    win.resizable(False, False)
    win.grab_set()  
    win.iconbitmap(resource_path("icon.ico")) 
    frame = tk.Frame(win, bg="#1e1e1e", padx=10, pady=10)
    frame.pack()
 
    img = Image.open(resource_path("suhail.png"))
    photo = ImageTk.PhotoImage(img)
    label_img = tk.Label(frame, image=photo, bg="#1e1e1e")
    label_img.image = photo
    label_img.pack(side="left", padx=10)

    label_text = tk.Label(frame, text=msg, font=("MS Gothic", 12), fg="white", bg="#1e1e1e", justify="left")
    label_text.pack(side="left", padx=10)

    btn = tk.Button(win, text="OK", command=win.destroy, bg="#53C4B1", fg="white", width=10)
    btn.pack(pady=10)

    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")


def popup_yes_no(msg):
    result = {"answer": None}
    win = tk.Toplevel()
    win.configure(bg="#1e1e1e")
    win.resizable(False, False)
    win.grab_set()
    win.iconbitmap(resource_path("icon.ico"))  
    frame = tk.Frame(win, bg="#1e1e1e", padx=10, pady=10)
    frame.pack()
    img = Image.open(resource_path("suhail.png"))
    photo = ImageTk.PhotoImage(img)
    label_img = tk.Label(frame, image=photo, bg="#1e1e1e")
    label_img.image = photo
    label_img.pack(side="left", padx=10)

    label_text = tk.Label(frame, text=msg, font=("MS Gothic", 12), fg="white", bg="#1e1e1e", justify="left")
    label_text.pack(side="left", padx=10)

    def yes(): result["answer"] = True; win.destroy()
    def no(): result["answer"] = False; win.destroy()

    btn_frame = tk.Frame(win, bg="#1e1e1e")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Yes", command=yes, bg="#53C4B1", fg="white", width=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text="No", command=no, bg="#214157", fg="white", width=10).pack(side="left", padx=5)

    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

    win.wait_window()
    return result["answer"]

def on_image_click(event=None):
    popup_with_image(
        random.choice([
            "If you need help with something, \nplease consult the developer. \nI'm sure she'd be happy to help. ",
            "Ah.. Be sure to pay attention to \nthe encoding when exporting playlists...",
            "What kind of music do you like?\nI like rock.",
            "My Walkman is a NW-S13. \nIt's a bit banged up, \nbut I take it with me everywhere.",
            "If you run into any bugs, please let the developer know... \nShe'd be very sad if anyone's playlists got messed up because \nshe decided to make me during an all-nighter.",
            "Did you know I was made because the developer \nonce spent three hours crying after she couldn't \nfigure out why her Walkman wasn't reading her playlists? \nIt was an encoding issue.",
            "Old technology is neat, but it is \na bit of a hassle sometimes.",
            "Wouldn't you rather be making playlists right now?",
            "I'd like to make a mixtape right now...",
            "This is the developer's first Python project.\nPlease show mercy to her.",
            "There's no way you'll catch me paying\nfor a music streaming platform now...",
            "I like to collect CDs too,\nbut they're harder to carry around...\n",
            "How's the storage on your MP3 Player doing?",
            "I hope you have a nice day today!",
            "My Walkman is in Japanese, \nso I don't actually understand any of \nthe user interface...",
            "Music makes me really happy! \nIt always cheers me up when \nI'm having a tough time.",
            "Oh, no... I lost my Walkman charger again...",
            "You should listen to some of \nyour old playlists today.\nIt's fun to rediscover old favorites.",
            "The developer is a broke student...\nIf you'd like to support her, you can\ndo so at https://ko-fi.com/catskulls.",
            "You can pry these .mp3 files from my cold, dead hands!",
            "If you have a feature you'd like to suggest,\nlet the developer know!\nShe'll try her best... probably...",
            "I got my Walkman used.\nIt had hours of foreign audio books on it...\n",
            "It's nice to disconnect from the internet\nevery once in a while.",

        ])
    )

def load_playlist():


    global playlist, music_root, current_playlist_file
    file_path = filedialog.askopenfilename(
        title="Open Playlist",
        filetypes=[("M3U Playlist", "*.m3u"), ("All Files", "*.*")]
    )
    if not file_path:
        return

    encodings_to_try = ["utf-8", "utf-8-sig", "shift_jis", "cp932", "latin1"]
    success = False
    lines = []

    for enc in encodings_to_try:
        try:
            with open(file_path, "r", encoding=enc) as f:
                lines = f.readlines()
            success = True
            break
        except UnicodeDecodeError:
            continue

    if not success:
        popup_with_image(f"I'm sorry, I have no idea what kind of encoding this is...!")
        return

    playlist.clear()
    playlist_tree.delete(*playlist_tree.get_children())

    playlist_dir = os.path.dirname(file_path)
    if not music_root:
        music_root = playlist_dir
        label_root.config(text=f"root: {music_root}")

    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        abs_path = os.path.join(playlist_dir, line) if not os.path.isabs(line) else line
        rel = os.path.relpath(abs_path, music_root) if os.path.exists(abs_path) else line

        playlist.append(abs_path)
        tag = "even" if i % 2 == 0 else "odd"
        playlist_tree.insert("", "end", values=(rel,), tags=(tag,))


root = tk.Tk()
root.title("Suhail")
root.geometry("1000x600")
root.configure(bg="#1e1e1e")
root.iconbitmap(resource_path("icon.ico"))

FONT_LIST = tkFont.Font(root=root, family="MS Sans Serif", size=12)
FONT_LABEL = tkFont.Font(root=root, family="MS Gothic", size=12)

frame_top = tk.Frame(root, bg="#1e1e1e")
frame_top.pack(fill="x", pady=5)
tk.Button(frame_top, text="Select Music Root Folder", command=choose_root, bg="#53C4B1", fg="white").pack(side="left", padx=5)
label_root = tk.Label(frame_top, text="Root: (none selected)", font=FONT_LABEL, fg="white", bg="#1e1e1e")
label_root.pack(side="left")

frame_main = tk.Frame(root, bg="#1e1e1e")
frame_main.pack(fill="both", expand=True, padx=10, pady=10)

frame_main.grid_rowconfigure(0, weight=1)
frame_main.grid_columnconfigure(0, weight=1)
frame_main.grid_columnconfigure(1, weight=0)
frame_main.grid_columnconfigure(2, weight=1)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                rowheight=25,
                font=("MS Gothic", 12),
                foreground="white",
                background="#2e2e2e",
                fieldbackground="#2e2e2e")
style.map("Treeview",
          background=[("selected", "#53C4B1")],
          foreground=[("selected", "white")])
style.configure("Treeview.Heading", font=("MS Gothic", 12))


file_tree = ttk.Treeview(frame_main, columns=("track",), show="headings")
file_tree.heading("track", text="Tracks")
file_tree.column("track", anchor="w", width=500, stretch=True)
file_tree.grid(row=0, column=0, sticky="nsew")

scrollbar_files = ttk.Scrollbar(frame_main, command=file_tree.yview)
scrollbar_files.grid(row=0, column=0, sticky="nse")
file_tree.config(yscrollcommand=scrollbar_files.set)

file_tree.tag_configure("even", background="#2e2e2e")
file_tree.tag_configure("odd", background="#383838")

frame_buttons = tk.Frame(frame_main, bg="#1e1e1e")
frame_buttons.grid(row=0, column=1, sticky="ns", padx=5)

img = Image.open(resource_path("suhail.png"))
photo = ImageTk.PhotoImage(img)
label_img = tk.Label(frame_buttons, image=photo, bg="#1e1e1e")
label_img.image = photo
label_img.pack(pady=10)
label_img.bind("<Button-1>", on_image_click)

ENCODINGS = ["shift_jis", "utf-8", "cp932", "latin-1"]

ENCODING_OPTIONS = {
    "Shift_JIS (Japanese Walkman)": "shift_jis",
    "UTF-8 (Global / Newer Models)": "utf-8",
    "CP932 (Windows Japanese)": "cp932",
    "Latin-1 (Western Europe)": "latin-1",
}

encoding_var = tk.StringVar(value="Shift_JIS (Japanese Walkman)")

frame_encoding = tk.Frame(root, bg="#1e1e1e")
frame_encoding.pack(fill="x", padx=10, pady=(5, 0))

tk.Label(
    frame_encoding,
    text="Encoding:",
    font=("MS Gothic", 10),
    fg="white",
    bg="#1e1e1e"
).pack(side="left", padx=(5, 10))

encoding_menu = tk.OptionMenu(frame_encoding, encoding_var, *ENCODING_OPTIONS.keys())
encoding_menu.config(
    bg="#2e2e2e",
    fg="white",
    activebackground="#3a3a3a",
    activeforeground="white",
    font=("MS Gothic", 10),
    relief="flat",
    width=28
)
encoding_menu["menu"].config(bg="#2e2e2e", fg="white", font=("MS Gothic", 10))

encoding_menu.pack(side="left", padx=5)


tk.Button(frame_buttons, text="Add →", command=add_selected, width=15).pack(pady=2)
tk.Button(frame_buttons, text="Remove", command=remove_selected, width=15).pack(pady=2)
tk.Button(frame_buttons, text="Move Up", command=move_up, width=15).pack(pady=2)
tk.Button(frame_buttons, text="Move Down", command=move_down, width=15).pack(pady=2)
tk.Button(frame_buttons, text="Clear Playlist", command=clear_playlist, width=15).pack(pady=2)
btn_load = tk.Button(frame_buttons, text="Load Playlist", command=load_playlist, bg="#1F2020", fg="white", state="disabled", width=15)
btn_load.pack(pady=2)


tk.Button(frame_buttons, text="Save Playlist", command=save_playlist, bg="#53C4B1", fg="white", width=15).pack(pady=10)


playlist_tree = ttk.Treeview(frame_main, columns=("track",), show="headings")
playlist_tree.heading("track", text="Playlist")
playlist_tree.column("track", anchor="w", width=500, stretch=True)
playlist_tree.grid(row=0, column=2, sticky="nsew")

scrollbar_playlist = ttk.Scrollbar(frame_main, command=playlist_tree.yview)
scrollbar_playlist.grid(row=0, column=2, sticky="nse")
playlist_tree.config(yscrollcommand=scrollbar_playlist.set)
playlist_tree.tag_configure("even", background="#2e2e2e")
playlist_tree.tag_configure("odd", background="#383838")

root.mainloop()
