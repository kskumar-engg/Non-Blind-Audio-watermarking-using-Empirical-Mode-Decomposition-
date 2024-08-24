A sophisticated robust watermarking technique is capable of identifying modifications and preserving the integrity of the watermark, which enables the identification of the actual perpetrator. The proposed Non blind EMD is one technique that has demonstrated the capacity to preserve over 60% of the watermark even in the face of various attacks, such as filtering, cropping, and compression.

Requirements: Python 3.10 or latest version.

Install the following libraries: 
1. pip install numpy
2. pip install EMD-signal
3. pip install librosa
4. pip install matplotlib
5. pip install Wave


**Demo:
**

A.Please update all paths in all libraries and sys paths, image paths in main files(part 1 and part2).

B.watermark_embed.py file has to be executed first.

C.Import audio, give a text for watermarking(check output files for sample output).

D.Select “initiate watermarking”.

E.Watermarking will take some time and the audio will be saved in the main files folder.

F.Now we can compare the original and watermarked files.

G.Select import watermarked audio. As the original audio is already selected with ‘Import Audio’, proceed with next step.

H.Select ‘Compare files’ This will show if any significant changes took place in the audio file.

I.Waveforms are shown portraying a clear visual representation of small spikes or changes to the watermarked audio.

J.Alternately, user can make the modification to the watermarked audio as it is file that would be shared for distribution.  Now this file is selected for comparison with the original audio.

K.This would likely show a large amount of changes in waveforms compared to previous checks.


**Demo 2:
**

A.Lets see if the watermark can be recovered for the modified watermarked audio file.

B.watermark_extraction.py is executed.

C.Users have to select original and modified watermarked audio.

D.Extract watermark button is clicked.

E.It takes a while to process and the watermark will be extracted.


