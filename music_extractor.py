import csv
import eyed3
import librosa
import numpy as np
import sys

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

def extract_music_content(directory):
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
        print('Extracting ', file, '...')
        music_metadata = []

        title, artist, album = load_editorial_metadata(file)
        
        music_metadata.append(file)
        music_metadata.append(title)
        music_metadata.append(artist)
        music_metadata.append(album)

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

def extract_music_frames(directory):
    '''Extracts mp3 metadata by frame

    Args:
        directory (string): directory that contains mp3 files

    Returns:
        metadata ([string]): all frames metadata
    '''
    all_metadata = [['title', 'artist', 'mean_thirteen_first_mfcc', 'zcr', 'max_chroma']]

    files = librosa.util.find_files(directory, ext='mp3')

    for file in files:
        print('Extracting ', file, '...')

        title, artist, _ = load_editorial_metadata(file)

        wf, sr = librosa.load(file)

        mfcc = librosa.feature.mfcc(y=wf, sr=sr)
        mfcc = np.mean(mfcc[:13], axis=0) # take the first 13 mfcc values
        # print(mfcc.shape)

        zcr = librosa.feature.zero_crossing_rate(y=wf)
        zcr = np.mean(zcr, axis=0)
        # print(zcr.shape)

        chroma_stft = librosa.feature.chroma_stft(y=wf, sr=sr)
        chroma_stft_max = np.argmax(chroma_stft, axis=0)
        # print(chroma_stft_max.shape)

        for i in range(len(mfcc)):
            music_frame_metadata = []
            music_frame_metadata.append(title)
            music_frame_metadata.append(artist)
            music_frame_metadata.append(mfcc[i])
            music_frame_metadata.append(zcr[i])
            music_frame_metadata.append(chroma_stft_max[i])

            all_metadata.append(music_frame_metadata)
    
    return all_metadata

def save_to_csv(data, csv_file):
    '''Saves data (list) to a csv file

    Args:
        data ([object]): list of metadata to be saved
    '''
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def exit_with_msg(msg):
    '''Exit with a custom message

    Args:
        msg (string): exit message
    '''
    print(msg)
    sys.exit()

def check_arguments(argv):
    '''Check arguments when running the program

    Args:
        argv ([string]): list of arguments
    '''
    if (len(argv) != 4):
        exit_with_msg('Need 4 arguments to continue')
    else:
        extraction_type = sys.argv[1]
        music_folder = sys.argv[2]
        csv_file = sys.argv[3]
        return extraction_type, music_folder, csv_file

# Main program
if __name__ == '__main__':
    extraction_type, music_folder, csv_file = check_arguments(sys.argv)
    if (extraction_type == 'extract_music'):
        metadata = extract_music_content(music_folder)
        save_to_csv(metadata, csv_file)
    elif (extraction_type == 'extract_music_frame'):
        metadata = extract_music_frames(music_folder)
        save_to_csv(metadata, csv_file)
    else:
        exit_with_msg('Extraction type invalid, please use only \'extract_music\' or \'extract_music_frame\'')
