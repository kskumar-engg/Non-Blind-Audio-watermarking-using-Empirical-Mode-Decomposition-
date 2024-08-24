#If you are cloning my project, update the paths before testing on your local system.
import tkinter as tk
from tkinter import filedialog, Label, messagebox, ttk, Text, font as tkfont
from PIL import Image, ImageTk
import numpy as np
from PyEMD import EMD
from scipy.signal import find_peaks
import sys
import librosa
sys.path.append("D:\\2-1\\OOAD\\Lib")

'''
We are using two methods to make sure watermark is extracted with more probability
method 1) Standard EMD
method 2)Non Blind EMD
'''
class WatermarkExtraction:
    def __init__(self, original_audio_path, watermarked_audio_path, imf_index=None, strength=None, S=None, segment_size=441, total_samples=88200):
        self.original_audio_path = original_audio_path
        self.watermarked_audio_path = watermarked_audio_path
        self.imf_index = imf_index  # Used for the first method
        self.strength = strength    # Used for the first method
        self.S = S                  # Used for the second method, this is also strength. S is used to recollect the formula defined for non blinding EMD
        self.segment_size = segment_size
        self.total_samples = total_samples

    def read_audio(self, path):
        # Reads the audio file and returns its samples
        signal, _ = librosa.load(path, sr=None)  # Load with the original sample rate
        return signal

    def extract_imfs(self, signal):
        # Performs EMD on the signal and returns IMFs
        print("start EMD - IMFs")
        emd = EMD(max_imfs=2)
        IMFs = emd(signal)
        print("End EMD - IMFs")
        return IMFs

    def get_extrema(self, imf):
        # Finds the extrema (maxima and minima) of the given IMF
        derivative = np.diff(imf)
        extrema_indexes = np.where(np.diff(np.sign(derivative)))[0] + 1
        return imf[extrema_indexes]

    def convert_bits_to_string(self, bits):
        # We assume watermark_bits is a list of integers (e.g., [1, 0, 1, 1, ...])
        chars = [chr(int(''.join(str(bit) for bit in bits[i:i+8]), 2)) for i in range(0, len(bits), 8)]
        return ''.join(chars)

    def extract_watermark_method_1(self):
        # This method concentrates on standard EMD, i.e extraction without segments
        original_signal = self.read_audio(self.original_audio_path)
        watermarked_signal = self.read_audio(self.watermarked_audio_path)
        
        original_imfs = self.extract_imfs(original_signal)
        watermarked_imfs = self.extract_imfs(watermarked_signal)
        
        watermark_imf = watermarked_imfs[self.imf_index]
        original_imf = original_imfs[self.imf_index]
        
        watermark_signal = watermark_imf - original_imf
        watermark_bits = np.round(watermark_signal / self.strength).astype(int)
        watermark_bits = np.clip(watermark_bits, 0, 1)  # This addition of 0 and 1 makes sure that bits are also of 0 and 1
        
        return self.convert_bits_to_string(watermark_bits)

    def extract_watermark_method_2(self):
        # This uses the non blinding method with segments
        original_signal = self.read_audio(self.original_audio_path)[:self.total_samples]
        watermarked_signal = self.read_audio(self.watermarked_audio_path)[:self.total_samples]
        
        watermark_bits = []
        for i in range(0, self.total_samples, self.segment_size):
            original_segment = original_signal[i:i+self.segment_size]
            watermarked_segment = watermarked_signal[i:i+self.segment_size]
            
            original_imfs = self.extract_imfs(original_segment)
            watermarked_imfs = self.extract_imfs(watermarked_segment)
            
            original_extrema = self.get_extrema(original_imfs[0])
            watermarked_extrema = self.get_extrema(watermarked_imfs[0])
            
            for j, (orgExt, waterExt) in enumerate(zip(original_extrema, watermarked_extrema)):
                if abs(waterExt - orgExt) >= self.S / (2 ** (j + 1)):
                    watermark_bits.append(1)
                else:
                    watermark_bits.append(0)

        return self.convert_bits_to_string(watermark_bits)

    def extract_watermark(self):
        possible_watermarks = {}

        # Attempt to extract watermark using the first method(standard EMD)
        try:
            watermark_a = self.extract_watermark_method_1()
            if watermark_a:
                possible_watermarks['a'] = watermark_a
        except Exception as e:
            print(f"Method 1 failed: {e}")

        # Attempt to extract watermark using the second method( Non Blind EMD)
        try:
            watermark_b = self.extract_watermark_method_2()
            if watermark_b:
                possible_watermarks['b'] = watermark_b
        except Exception as e:
            print(f"Method 2 failed: {e}")

        # Return the possible watermarks
        return possible_watermarks

global_image = None
global_audio = None
global_audio_watermarked = None

def import_audio():
    global global_audio
    global_audio = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")]) # "*.wav *.mp3 *.aac" are options but as wav is uncompressed format. we will prefer using it.
    if global_audio:
        file_label_originalAudio.config(text=f"Selected: {global_audio}")   #print(f"Audio file {audio_file} selected.")
    else:
        file_label_originalAudio.config(text="No file was selected.")

def import_watermarked_audio():
    global global_audio_watermarked
    global_audio_watermarked = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")]) # "*.wav *.mp3 *.aac"  are options but as wav is uncompressed format. we will prefer using it.
    if global_audio_watermarked:
        file_label_watermarkedAudio.config(text=f"Selected: {global_audio_watermarked}")   #print(f"Audio file {audio_file} selected.")
    else:
        file_label_watermarkedAudio.config(text="No file was selected.")

def extract_watermark():
    # Initialization of the WatermarkExtraction with the necessary parameters

    imf_index = 0  # Index of the IMF that contains the watermark 
    strength = 0.5  # Strength of the watermark(method 1)
    S = 0.5  # Optimum embedding strength(method 2)
    total_samples = 88200  # Total samples to consider for the watermark extraction

    extractor = WatermarkExtraction(global_audio, global_audio_watermarked, imf_index=imf_index, strength=strength, S=S, total_samples=total_samples)

    possible_watermarks = extractor.extract_watermark()         #Extraction using both techniques

    # Checks the watermarks retrieved and displays on both console and GUI
    if 'a' in possible_watermarks and 'b' in possible_watermarks:
        print("Possible watermarks:")
        print(f"a: {possible_watermarks['a']}")
        print(f"b: {possible_watermarks['b']}")
        messagebox.showinfo("Possible watermarks:", f"Possible watermarks:: {possible_watermarks['a'], possible_watermarks['b']}")
    elif 'a' in possible_watermarks:
        print(f"Watermark from method 1: {possible_watermarks['a']}")
        messagebox.showinfo("Watermark Output:", f"Watermark:: {possible_watermarks['a']}")
    elif 'b' in possible_watermarks:
        print(f"Watermark from method 2: {possible_watermarks['b']}")
        messagebox.showinfo("Watermark Output:", f"Watermark:: {possible_watermarks['b']}")
    else:
        print("No watermark could be extracted.")
        messagebox.showinfo("No Watermark found", "No watermark could be extracted.")


# Initializing the main window
root = tk.Tk()
root.title("Non-Blind Audio Watermarking Scheme Based on Empirical Mode Decomposition")
root.geometry("1080x720")  # Setting the window size

image_path = "D:/2-1/OOAD/inputs/audioImage.jpg"          #Please update the Image Path if working on a different system.
background_image  = Image.open(image_path)
background_image  = background_image.resize((1080, 720), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Creation of the main frames.
left_frame = tk.Frame(root, width=320, height=350)
left_frame.pack(side="left", padx=20, pady=20)
left_frame.pack_propagate(0)

# Creation of the sub frames. This prevents in overlapping of one name with another after file import.
left_top_frame = tk.Frame(left_frame, padx=10, pady=10)
left_middle_frame = tk.Frame(left_frame, padx=10, pady=10, height=200)
left_bottom_frame = tk.Frame(left_frame, padx=10, pady=10, height=100)
left_top_frame.pack(fill="both", expand=True)
left_middle_frame.pack(fill="both", expand=True)
left_bottom_frame.pack(fill="both", expand=True)

import_original_button = tk.Button(left_top_frame, text="Import Original Audio", command=import_audio)
file_label_originalAudio = Label(left_top_frame, text="", wraplength=300)
import_original_button.pack(pady=15)
file_label_originalAudio.pack()

import_watermarked_button = tk.Button(left_middle_frame, text="Import Watermarked Audio", command=import_watermarked_audio)
file_label_watermarkedAudio = Label(left_middle_frame, text="", wraplength=300)
import_watermarked_button.pack(pady=15)
file_label_watermarkedAudio.pack()

extract_watermark_button = tk.Button(left_bottom_frame, text="Extract Watermark", command=extract_watermark)
extract_watermark_button.pack(pady=15)

root.mainloop() #Donot remove this, else GUI would fail to start
