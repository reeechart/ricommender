import csv
import eyed3
import librosa
import numpy as np

def load_editorial_metadata(audiofile):
    '''Loads an audio file and extract its editorial metadata

    Args:
        audiofile (string): audio file to be extracted.

    Returns:
        title (string): title of the mp3 file
        artist (string): artist/singer of the song in mp3 file
        album (string): name of album of the mp3 file
    '''
    audio = eyed3.load(audiofile)
    # print(audio.tag.artist)
    # print(audio.tag.title)
    # print(audio.tag.album)
    # print(audio.tag.images.get('image/jpeg')) # not working

    return audio.tag.title, audio.tag.artist, audio.tag.album

def with_quote(string):
    '''Adds quote to a string

    Args:
        string (string): to be quoted string

    Returns:
        string (string): quoted string
    '''
    return '"'+string+'"'

def extract_content(directory):
    '''Extracts mp3 metadata from a specified directory

    Args:
        directory (string): directory that contains the mp3 files

    Returns:
        metadata ([string]): list of mp3 metadata with a structure of 
            (file, title, artist, album, mfcc, zcr, tempo, chroma_stft)
    '''
    all_metadata = [['file', 'title', 'artist', 'album', 'mfcc', 'zcr', 'tempo', 'pitch', 'chroma']]

    files = librosa.util.find_files(directory, ext='mp3')

    for file in files:
        music_metadata = []

        title, artist, album = load_editorial_metadata(file)
        
        music_metadata.append(file)
        music_metadata.append(title)
        music_metadata.append(artist)
        music_metadata.append(album)

        # music_metadata.append(with_quote(file))
        # music_metadata.append(with_quote(title))
        # music_metadata.append(with_quote(artist))
        # music_metadata.append(with_quote(album))

        wf, sr = librosa.load(file)

        mfcc = librosa.feature.mfcc(y=wf, sr=sr)
        music_metadata.append(np.mean(mfcc))

        zcr = librosa.feature.zero_crossing_rate(y=wf)
        music_metadata.append(np.mean(zcr))

        tempo = librosa.beat.tempo(y=wf, sr=sr)
        music_metadata.append(tempo[0])

        # Get pitches array and its corresponding power (magnitude)
        pitches, magnitudes = librosa.piptrack(y=wf, sr=sr)

        # Select pitches with high energy (bigger than its median)
        pitches = pitches[magnitudes > np.median(magnitudes)]
        pitch = librosa.pitch_tuning(pitches)
        music_metadata.append(pitch)

        # Extract beat
        # beat_times = librosa.frames_to_time(beat_frames, sr=sampling_rate[0])
        # print(beat_frames)
        # print(beat_times)

        chroma_stft = librosa.feature.chroma_stft(y=wf, sr=sr)
        music_metadata.append(np.mean(chroma_stft))

        all_metadata.append(music_metadata)
    
    return all_metadata

def save_to_csv(data):
    '''Saves data (list) to a csv file

    Args:
        data ([object]): list of metadata to be saved
    '''
    with open('music_metadata.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

if __name__ == '__main__':
    metadata = extract_content('musics_test')
    save_to_csv(metadata)
