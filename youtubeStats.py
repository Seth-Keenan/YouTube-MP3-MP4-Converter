#Refer to readme.txt to download pytube, ssl, requests, and Pillow library
#Seth Keenan SKJGFR

import ssl
import tkinter as tk
import requests
import webbrowser
from pytube import YouTube
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import filedialog

def getDownloadOptions(yt):
    def downloadVideo(yt):
        filePath = filedialog.askdirectory()
        video = yt.streams.filter(file_extension='mp4').get_highest_resolution()

        if not filePath:
            status.config(text="Choose a valid directory", fg="red")

        else:
            video.download(filePath)
            opts.destroy()
            print(f"Video file saved to {filePath}")

        return
    
    def downloadAudio(yt):
        filePath = filedialog.askdirectory()
        video = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()

        if not filePath:
            status.config(text="Choose a valid directory", fg="red")

        else:
            video.download(filePath)
            opts.destroy()
            print(f"Audio file saved to {filePath}")


        return
    
    opts = tk.Toplevel()
    opts.geometry("400x200")
    opts.title("Downloads")

    opts.configure(bg="#333333")
    opts.rowconfigure((0,5), weight=1)
    opts.columnconfigure(0, weight=1)

    mp3Label = tk.Label(opts, text="Audio Download!", font=("Helvetica", 22, "bold"), bg="#333333", fg="white")
    mp3Label.grid(row=0, column=0, pady=5, padx=5, sticky="NESW")

    audioButton = tk.Button(opts, text="Download!", command=lambda: downloadAudio(yt), bg="grey", fg="white")
    audioButton.grid(row=1, column=0, pady=5, padx=5, sticky="NESW")

    mp4Label = tk.Label(opts, text="Video Download!", font=("Helvetica", 22, "bold"), bg="#333333", fg="white")
    mp4Label.grid(row=2, column=0, pady=5, padx=5, sticky="NESW")

    vidButton = tk.Button(opts, text="Download!", command=lambda: downloadVideo(yt), bg="grey", fg="white")
    vidButton.grid(row=3, column=0, pady=5, padx=5, sticky="NESW")

    status = tk.Label(opts, text="Downloads may take a few seconds!", bg="#333333", fg="gold")
    status.grid(row=5, column=0, pady=5, padx=5, sticky="NESW")

    opts.resizable(False, False)

def callback(url):
    webbrowser.open_new_tab(url)

def inputGUI():
    app = tk.Tk()
    app.geometry("400x150")
    app.title("YouTube Statistics")

    app.configure(bg="#333333")
    app.columnconfigure(0, weight=1)

    label = tk.Label(app, text="Input YouTube video's URL: ", bg="#333333", fg="white", font=("Helvetica", 18, "bold"))
    label.grid(row=0, column=0, pady=5, padx=5)

    entry = tk.Entry(app)
    entry.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

    result_label = tk.Label(app, text="", bg="#333333", fg="red")
    result_label.grid(row=2, column=0, pady=5, padx=5)

    def getYTObj():
        url = entry.get()
        try:
            #Check for and return a vaild video
            yt = YouTube(url)
            result_label.config(text="Valid URL")
            app.destroy()
            statsGUI(yt, url)
        except Exception as err:
            result_label.config(text=f"Error: Please enter a valid URL")
            print(err)

    button = tk.Button(app, text="Display Stats", bg="grey", fg="white", command=getYTObj)
    button.grid(row=3, column=0, pady=5, padx=5, sticky="ew", rowspan=3)

    app.resizable(False, False)

    app.mainloop()

def statsGUI(yt, url):
    app = tk.Tk()
    app.geometry("640x600")
    app.title(f"{yt.title} (Statistics)")
    app.configure(bg="#333333")

    app.columnconfigure((0,1), weight=1)
    app.rowconfigure((0,4), weight=1)

    #Thumbnail
    thumbnail_url = yt.thumbnail_url
    response = requests.get(thumbnail_url)

    image = Image.open(BytesIO(response.content))
    image = image.resize((640, 360), Image.LANCZOS)

    photo = ImageTk.PhotoImage(image)

    thumbnail_label = tk.Label(app)
    thumbnail_label.config(image=photo)
    thumbnail_label.image = photo
    thumbnail_label.grid(row=0, column=0, sticky="NESW",columnspan=2)
    thumbnail_label.bind("<Button-1>", lambda g:
                         callback(url))

    #Title
    title = tk.Label(app, text=yt.title, font=("Helvetica", 22, "bold", "underline"), wraplength=600, anchor="center", bg="#333333", fg="white")
    title.grid(row=1, column=0, sticky="NESW", padx=10, pady=5, columnspan=2)
    title.bind("<Button-1>", lambda g:
                         callback(url))

    #Author
    author = tk.Label(app, text=yt.author, font=("Helvetica", 18, "underline"), bg="#333333", fg="white")
    author.grid(row=2, column=0, sticky="NESW", padx=10, pady=5, columnspan=2)
    author.bind("<Button-1>", lambda e:
               callback(yt.channel_url))

    #Length
    seconds = yt.length
    minutes = seconds // 60
    seconds %= 60
    length = tk.Label(app, text=('Length: '+str(minutes) + ":" +str(seconds)), font=("Helvetica", 16),  bg="#333333", fg="white")
    length.grid(row=3, column=0, sticky="NESW", padx=10, pady=5)

    #Views
    views = tk.Label(app, text=('Views: ' + str('{:,}'.format(yt.views))), font=("Helvetica", 16), bg="#333333", fg="white")
    views.grid(row=4, column=0, sticky="NESW", padx=10, pady=5)

    #Downloads
    downbutton = tk.Button(app, text="Downloads", bg="grey", fg="white", command=lambda: getDownloadOptions(yt))
    downbutton.grid(row=3, column=1, sticky="NESW", pady=5, padx=5, columnspan=1)

    #New Entry
    newVid = tk.Button(app, text="New Entry", bg="grey", fg="white", command=lambda: [app.destroy(), main()])
    newVid.grid(row=4, column=1, sticky="NESW", pady=5, padx=5, columnspan=1)

    app.resizable(False, False)

    app.mainloop()

def main():
    ssl._create_default_https_context = ssl._create_stdlib_context

    inputGUI()
        
main()