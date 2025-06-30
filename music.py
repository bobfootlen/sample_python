import pygame

# Initialize Pygame and the mixer
pygame.mixer.init()

# Load the MP3 file
try:
    pygame.mixer.music.load("BeepBox.mp3")  # Replace with your file path
except pygame.error:
    print("Error loading music file")
    exit()

# Play the music
pygame.mixer.music.play()

# Keep the music playing until it finishes or another command is given
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)  # Optional: controls how often the loop checks