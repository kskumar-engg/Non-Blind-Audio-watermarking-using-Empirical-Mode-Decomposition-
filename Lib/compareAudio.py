import matplotlib.pyplot as plt
import numpy as np
import wave

class CompareAudioFiles:
    def __init__(self, original_file_path, watermarked_file_path):          #Original and watermarked audios are passed as parameters
        self.original_file_path = original_file_path
        self.watermarked_file_path = watermarked_file_path

    def read_wav(self, filename):
        with wave.open(filename, 'rb') as file:
            frame_rate = file.getframerate()
            nframes = file.getnframes()
            frame_data = file.readframes(nframes)
            # Converting binary data to numpy array
            signal = np.frombuffer(frame_data, dtype=np.int16)
        return signal, frame_rate

    def plot_waveforms(self):
        # Reading the audio files
        signal_original, frame_rate_original = self.read_wav(self.original_file_path)
        signal_watermarked, frame_rate_watermarked = self.read_wav(self.watermarked_file_path)

        # Validating if the frame rates are different
        if frame_rate_original != frame_rate_watermarked:
            raise ValueError("The frame rates of the audio files are different!")

        '''# Check if the lengths of the signals are different
        if len(signal_original) != len(signal_watermarked):
            raise ValueError("The audio files have different lengths!")'''

        # Plotting the original and watermarked signals
        plt.figure(figsize=(10, 5))     #Here 10 and 5 are the inches occupied on the screen.

        # Plotting original audio waveform
        plt.subplot(2, 1, 1)
        plt.title('Original Audio Waveform')
        plt.plot(signal_original)
        plt.xlabel('Sample Number')
        plt.ylabel('Amplitude')

        # Plotting watermarked audio waveform
        plt.subplot(2, 1, 2)
        plt.title('Watermarked Audio Waveform')
        plt.plot(signal_watermarked, color='yellow')
        plt.xlabel('Sample Number')
        plt.ylabel('Amplitude')

        # Showing the plots
        plt.tight_layout()
        plt.show()
        
if __name__ == "__main__":
    # For standalone testing
    compare = CompareAudioFiles('D:/2-1/OOAD/inputs/test_audio.wav', 'D:/2-1/OOAD/watermarked_audio.wav')
    compare.plot_waveforms()
