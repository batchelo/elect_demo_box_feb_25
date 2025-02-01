import time, board, digitalio
from audiomp3 import MP3Decoder
from audiopwmio import PWMAudioOut as AudioOut

audio = AudioOut(board.GP17)
path = "sounds/"

filename = "weee.mp3"
mp3_file = open(path + filename, "rb")
decoder = MP3Decoder(mp3_file)

def play_mp3(filename):
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)
    while audio.playing:
        pass

play_mp3("intro.mp3")