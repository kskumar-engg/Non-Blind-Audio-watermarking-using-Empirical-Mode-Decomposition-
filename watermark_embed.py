#If you are cloning my project, update the paths before testing on your local system.
import tkinter as tk
from tkinter import filedialog, Label, messagebox, ttk, Text, font as tkfont
from PIL import Image, ImageTk
import sys
sys.path.append("D:\\2-1\\OOAD\\Lib")
from nonBlind_EMD import watermarkEMD
from compareAudio import CompareAudioFiles


global_image = None
global_audio = None
global_watermarked_audio = None

def import_audio():
    global global_audio
    global_audio = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")]) # "*.wav *.mp3 *.aac"  are options but as wav is uncompressed format. we will prefer using it.
    if global_audio:
        imported_file_name.config(text=f"Selected: {global_audio}")   #print(f"Audio file {audio_file} selected.")
    else:
        imported_file_name.config(text="No file was selected.")

def import_watermarked_audio():
    global global_watermarked_audio
    global_watermarked_audio = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")]) # "*.wav *.mp3 *.aac"  are options but as wav is uncompressed format. we will prefer using it.
    if global_watermarked_audio:
        messagebox.showinfo("Selected File", f"Selected file: {global_watermarked_audio}")
    else:
        messagebox.showinfo("No File", "No file was selected.")
def import_watermark_image():
    global global_image
    global_image = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg")])
    if global_image:
        selected_image = Image.open(global_image)
        #display(selected_image) or selected_image.show()
        messagebox.showinfo("Selected File", f"Selected file: {global_image}")
    else:
        messagebox.showinfo("No File", "No file was selected.")



def initiate_watermarking():
    '''print("audio path:")
    print(global_audio)'''
    watermark_string = "OOAD Audio Processing"
    input_watermark = watermark_input.get("1.0", "end-1c")
    if input_watermark != "" or input_watermark != None:
        watermark_string = input_watermark
    imf_index = 0  # IMF where the watermark is embedded into
    '''print("audio path:")
    print(global_audio)'''
    watermark_emd = watermarkEMD(global_audio)
    output_audio_path = watermark_emd.process(imf_index, watermark_string) # 1.0 = line 1, character 0 . end-1c =  which corresponds to the position of the last character in the widget, excluding the newline character that Tkinter automatically adds to the end of the text content.
    messagebox.showinfo("File Saved", f"Saved file path: {output_audio_path}")
    
def compare_files():
    '''print("audio path:")
    print(global_audio)'''
    compare_audio_files = CompareAudioFiles(global_audio, global_watermarked_audio)
    compare_audio_files.plot_waveforms()


# Initialization of the main window
root = tk.Tk()
root.title("Non-Blind Audio Watermarking Scheme Based on Empirical Mode Decomposition")
root.geometry("1080x720")  # Setting the window size

image_path = "D:/2-1/OOAD/inputs/audioImage.jpg"       # Background image for GUI
background_image  = Image.open(image_path)
background_image  = background_image.resize((1080, 720), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Creation of main frames
left_frame = tk.Frame(root, width=514, height=720)
right_frame = tk.Frame(root, width=514, height=720)
left_frame.pack(side="left", padx=20, pady=20)
right_frame.pack(side="right", padx=20, pady=20)

left_frame_title = tk.Label(left_frame, text="Audio & Watermark Import", font=("Helvetica", 16))
left_frame_title.pack()
right_frame_title = tk.Label(right_frame, text="Audio Watermarking", font=("Helvetica", 16))
right_frame_title.pack()

#  Creation of sub-frames for import and watermarking sections
left_top_frame = tk.Frame(left_frame, padx=10, pady=10)
left_middle_frame = tk.Frame(left_frame, padx=10, pady=10, height=200)
left_bottom_frame = tk.Frame(left_frame, padx=10, pady=10, height=100)


left_top_frame.pack(fill="both", expand=True)
left_middle_frame.pack(fill="both", expand=True)
left_middle_frame.pack_propagate(0)        #Prevents automatic resizing. Else width and height would be ignored. 
left_bottom_frame.pack(fill="both", expand=True)

# Adding import button under audio import section. This will be also used for compare files as to prevent asking user to import same file multiple times.
import_button = tk.Button(left_top_frame, text="Import Audio", command=import_audio)
# file label defined here allows to 
imported_file_name = Label(left_top_frame, text="", wraplength=300)
import_button.pack(pady=10)
imported_file_name.pack()


# Populate the left bottom frame with watermark options
watermark_type_label = tk.Label(left_middle_frame, text="Select Watermark Type:")
default_value_combobox = tk.StringVar(value="Text")
watermark_type_combobox = ttk.Combobox(left_middle_frame, textvariable=default_value_combobox, values=["Text", "Image"])
watermark_input = tk.Text(left_middle_frame, height=2, width=20)
import_image_button = tk.Button(left_middle_frame, text="Import Image", command=import_watermark_image)

# Logic to show or hide watermark input based on combobox selection
def watermark_type_selected(event):
    selection = watermark_type_combobox.get()
    if selection == "Image":
        watermark_input.pack_forget()
        import_image_button.pack(pady=10)
    elif selection == "Text":
        watermark_input.pack(pady=10)
        import_image_button.pack_forget()

watermark_type_label.pack(pady=10)
watermark_type_combobox.pack(pady=10)
watermark_input.pack(pady=10)
import_image_button.pack(pady=10)
watermark_type_selected(event=None)
watermark_type_combobox.bind("<<ComboboxSelected>>", watermark_type_selected)


initiate_button = tk.Button(left_bottom_frame, text="Initiate Watermarking", command=initiate_watermarking)
initiate_button.pack(pady=30)
imported_file_name_watermarked = Label(left_bottom_frame, text="")
imported_file_name_watermarked.pack()

# The right hand side helps user to compare the original audio with watermarked audio.
import_watermarked_button = tk.Button(right_frame, text="Import Watermarked Audio", command=import_watermarked_audio)
compare_button = tk.Button(right_frame, text="Compare Files(with original)", command=compare_files)

import_watermarked_button.pack(pady=15)
compare_button.pack(pady=10)

root.mainloop()     #Donot remove this, else GUI would fail to start
