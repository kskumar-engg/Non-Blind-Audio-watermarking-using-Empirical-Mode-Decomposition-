from scipy.io import wavfile
import sys
from PyEMD import EMD
import numpy as np


class watermarkEMD:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.audio_data = None
        self.sample_rate = None
        self.IMFs = None

    def read_audio(self):
        self.sample_rate, audio_data = wavfile.read(self.audio_path)
        # Convertion to float32 for EMD and normalizing the data
        audio_data = audio_data.astype(np.float32) / np.max(np.abs(audio_data))
        # Conversion to mono if necessary
        if audio_data.ndim == 2:
            audio_data = np.mean(audio_data, axis=1)
        self.audio_data = audio_data

    def perform_emd(self):
        emd = EMD(max_imfs=2)
        # Check if NaN or infinite values exists and handle them
        if np.any(np.isnan(self.audio_data)) or np.any(np.isinf(self.audio_data)):
            self.audio_data = np.nan_to_num(self.audio_data)
        print("start IMFs")
        self.IMFs = emd.emd(self.audio_data)
        print("End IMFs")       # Using this as it takes a lot of time for EMD and IMFs

    def convert_watermark_to_signal(self, watermark_string, length):
        binary_watermark = ''.join(format(ord(char), '08b') for char in watermark_string)
        repeated_watermark = (binary_watermark * (length // len(binary_watermark) + 1))[:length]
        watermark_signal = np.array([1 if bit == '1' else -1 for bit in repeated_watermark], dtype=np.float32)
        return watermark_signal

    '''def embed_watermark(self, imf_index, watermark_string):
        watermark_signal = self.convert_watermark_to_signal(watermark_string, len(self.IMFs[imf_index]))
        self.IMFs[imf_index] += watermark_signal'''
    def embed_watermark(self, imf_index, watermark_string, strength=0.01):
        watermark_signal = self.convert_watermark_to_signal(watermark_string, len(self.IMFs[imf_index]))
        # Scaling the watermark signal by the desired strength
        watermark_signal *= strength
        # Ensuring the watermark amplitude does not exceed a certain threshold. Else this would cause a noise that is audible to the listener.
        max_amplitude = np.max(np.abs(self.IMFs[imf_index])) * strength
        watermark_signal = np.clip(watermark_signal, -max_amplitude, max_amplitude)
        self.IMFs[imf_index] += watermark_signal


    def reconstruct_audio(self):
        reconstructed_signal = np.sum(self.IMFs, axis=0)
		# Normalizing the reconstructed signal before converting to int16
        reconstructed_signal = np.int16(reconstructed_signal / np.max(np.abs(reconstructed_signal)) * 32767)
        return reconstructed_signal

    def save_watermarked_audio(self, output_path, watermarked_signal):
        wavfile.write(output_path, self.sample_rate, watermarked_signal)

    def process(self, imf_index, watermark_string):
        print("Reading audio")
        self.read_audio()
        print("Audio read complete. Starting EMD")
        self.perform_emd()
        print("Embedding watermark.")
        self.embed_watermark(imf_index, watermark_string)
        print("Watermark embedded. Reconstructing audio.")
        watermarked_signal = self.reconstruct_audio()
        print("Audio reconstructed. Saving watermarked audio.")
        self.save_watermarked_audio('watermarked_audio.wav', watermarked_signal)
        print("Process complete. Watermarked audio saved.")
        return 'h2022H1030113P_D2_op7_watermarked_audio.wav'

if __name__ == "__main__":
    # For standalone testing
    audio_path = 'D:/2-1/OOAD/inputs/test_audio.wav'  
    watermark_string = "Test Audio Processing"
    imf_index = 0  #This is the index where watermarking occurs

    watermark_emd = watermarkEMD(audio_path)
    output_audio_path = watermark_emd.process(imf_index, watermark_string)

    print(f"Watermarked audio saved as {output_audio_path}")
