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

play_mp3("intro_l.mp3")
play_mp3("sounds.mp3")
play_mp3("display.mp3")
# play_mp3("temp.mp3")
# play_mp3("tilt.mp3")
# play_mp3("sense_distance.mp3")
# play_mp3("lights.mp3")
# play_mp3("temp.mp3")
# play_mp3("yipee.mp3")
# play_mp3("UM_respond.mp3")
# play_mp3("hope.mp3")
