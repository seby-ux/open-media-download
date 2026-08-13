from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from ttkbootstrap import Style
import ttkbootstrap as ttkb
import yt_dlp
import threading
import time

#to-do: 1. format selector (mp4/mp3), 2. download progress bar




def download_video():
    print("Downloading video...")
    status_var.set("Downloading video... Please wait.")
    # Placeholder function for downloading video

    URLS = [link_entry.get()]
    ydl_opts = {
     'format': 'mp3/bestaudio/best',
      'postprocessors': [{  # Extract audio using ffmpeg
         'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',  
        },
        {
        'key': 'FFmpegMetadata',
        },
        ],
     'outtmpl': f'{folder_var.get()}/%(title)s.%(ext)s'   
     }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)
    root.after(0, on_finished)

def start_download_thread():
    progress.start()
    download_thread = threading.Thread(target=download_video)
    download_thread.start()  
def on_finished():
    status_var.set("Fertig!")
    progress.stop()
    progress['value'] = 0
    progress.update_idletasks()

root = Tk()
root.title("Music Downloader")
root.columnconfigure(0, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("700x600")

frm = ttk.Frame(root, padding=10)
frm.grid(row=0, column=1)

folder_var = StringVar()

def choose_folder():
    folder_selected = filedialog.askdirectory()
    folder_var.set(folder_selected)

button_choose_folder = ttk.Button(frm, text="Ordner auswählen", command=choose_folder)
button_choose_folder.grid(column=1, row=2)

link_entry = ttk.Entry(frm)
link_entry.grid(column=1, row=1)

ttk.Button(frm, text="Download", command=start_download_thread).grid(column=1, row=4)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=8)

var = StringVar()
status_var = StringVar()
status_label = ttk.Label(frm, textvariable=status_var).grid(column=1, row=5)

chosen_file_label = ttk.Label(frm, textvariable=folder_var).grid(column=1, row=3)

progress = ttk.Progressbar(frm, orient=HORIZONTAL, length=200, mode='indeterminate')
progress.grid(column=1, row=6)

root.mainloop()