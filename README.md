# guitar-tuner
This is a Python guitar tuner set to mechanically tune a guitar using a Raspberry Pi and DC motor. The [sounddevice](https://python-sounddevice.readthedocs.io/en/0.3.12/) package (providing  bindings for the PortAudio library) was used to import audio data into NumPy arrays. An autocorrelation algorithm is then used to identify the audio frequencies from which note correction can be calculated.

The physical requirements of this project also included a custom 3D printed mount which attaches to the DC motor to allow it to turn a guitar tuning peg. As the user continues to play the guitar string as it is being tuned, to indicate that the correct note pitch has been attained the motor 'shakes' (turns back and forth a small amount repeatedly). An example of the program's execution and hardware use can be found in the following video:

https://youtu.be/53lJ8EAVHaI

##### This project was completed using self-taught programming skills during my A-level studies as something to write about on my university applications.
