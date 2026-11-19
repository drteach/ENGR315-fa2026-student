"""
CULMINATING ASSIGNMENT 3: Musical Note Detection

Create a program which detects the note being played from the given audio file based on its frequency.
It is up to you to employ an appropriate methodology to process the audio signal and detect the note.
The relevant data file is named "Guitar-note-1.wav" and is located in data > musical-notes.
In the same directory, we also provide a reference for the corresponding frequencies of each note.

Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
We have provided a possible method for converting the .wav file to usable data below.
All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os


# Read the note names and frequencies from the reference file.
note_names = []
note_frequencies = []
data_dir = os.path.join("..", "..", "data", "musical-notes")
reference_file = open(os.path.join(data_dir, "note-frequencies-reference.csv"))
reference_lines = reference_file.readlines()
reference_file.close()

for line in reference_lines[2:]:
    values = line.strip().split(",")
    note_names.append(values[0])
    note_frequencies.append(float(values[1]))


file_names = [
    "Guitar-note-1.wav",
    "Guitar-note-2.wav",
    "Guitar-note-3.wav",
    "Guitar-note-4.wav",
    "Guitar-note-5.wav",
]

print("File name           Frequency (Hz)   Note")

for file_name in file_names:
    sample_rate, audio = wavfile.read(os.path.join(data_dir, file_name))

    # These supplied recordings are mono. Remove the average value.
    original_audio = audio
    audio = audio - np.mean(audio)

    # Compare the signal with delayed copies to find its repeating period.
    # Using a section from the middle of the recording: it skips the pluck at the start and the quiet decay at the end.
    section_start = len(audio) // 3
    section = audio[section_start:section_start + 5000]
    scores = []
    lags = []


    # Lags of 10 to 1600 samples cover about 27 Hz to 4400 Hz at 44.1 kHz.
    for lag in range(10, 1601):
        first_part = section[:-lag]
        second_part = section[lag:]
        score = np.sum(first_part * second_part) / (
            np.sum(first_part * first_part) * np.sum(second_part * second_part)
        ) ** 0.5
        scores.append(score)
        lags.append(lag)


    # Take the FIRST strong peak, not the highest, so we get the fundamental period instead of a multiple of it.
    threshold = 0.85 * max(scores)
    best_lag = lags[0]
    for i in range(1, len(scores) - 1):
        if scores[i] >= threshold and scores[i] > scores[i - 1] and scores[i] >= scores[i + 1]:
            best_lag = lags[i]
            break

    frequency = sample_rate / best_lag

    # Match the detected frequency to the closest note in the reference.
    note_index = 0
    for i in range(len(note_frequencies)):
        if abs(note_frequencies[i] - frequency) < abs(
            note_frequencies[note_index] - frequency
        ):
            note_index = i
    note = note_names[note_index]
    print(file_name, round(frequency, 2), note)

    # Name used for plot titles and saved image files.
    base_name = file_name.replace(".wav", "")
    time = np.arange(len(original_audio)) / sample_rate

    # Task 1: plot the complete recording.
    plt.figure()
    plt.plot(time, original_audio, label="Original audio")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title(base_name + ": Full Audio Signal")
    plt.legend()
    plt.savefig(base_name + "-full.png")

    # Task 2: show five periods, starting where the period was measured.
    # The window length comes from the detected period (best_lag), so it
    # adapts to any note.
    start = section_start
    stop = section_start + 5 * best_lag
    detail_time = np.arange(start, stop) / sample_rate * 1000

    # Smooth the plotted region with a 15-sample moving average.
    # The original (not mean-removed) audio is smoothed so both lines match.
    processed = []
    for i in range(start, stop):
        samples = original_audio[i - 7 : i + 8]
        processed.append(np.mean(samples))

    plt.figure()
    plt.plot(detail_time, original_audio[start:stop], label="Original audio")
    plt.plot(detail_time, processed, label="Processed audio")
    plt.xlabel("Time (milliseconds)")
    plt.ylabel("Amplitude")
    plt.title(base_name + ": Five Periods")
    plt.legend()
    plt.savefig(base_name + "-periods.png")

plt.show()
