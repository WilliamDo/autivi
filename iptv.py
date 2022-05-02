import vlc

from time import sleep
 
if __name__ == '__main__':
    media = vlc.MediaPlayer("video.mp4") 
    media.play()

    sleep(5) # Or however long you expect it to take to open vlc
    while media.is_playing():
        sleep(1)
    
    
