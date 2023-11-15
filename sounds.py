# don't need to use that, the sounds are already made.

from gtts import gTTS

text1 = 'turn left'
text2 = 'turn right'
text3 = 'move forward'

tts = gTTS(text1)
tts.save("left.mp3")
tts = gTTS(text2)
tts.save("right.mp3")
tts = gTTS(text3)
tts.save("ok.mp3")
