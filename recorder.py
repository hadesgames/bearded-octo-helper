import pyaudio
import Queue


class Recorder:
    def __init__(self,
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            frames_per_buffer=1024,
            chunk=1024):
        self.pyaudio = pyaudio.PyAudio()
        self.chunk = chunk
        self.config = {
                'format': format,
                'channels': channels,
                'rate': rate,
                'frames_per_buffer': frames_per_buffer
        }


        self.blocks = Queue.Queue()



    def start(self):
        self.stream = self.pyaudio.open(input=True, **self.config)

    def pause(self):
        if self.stream.is_active():
            self.stream.stop_stream()

    def record(self, time):
        frames = []
        nr = int(self.config["rate"] / self.chunk * time)
        for i in range(0, nr):
            frames.append(self.stream.read(self.chunk))
        block = b''.join(frames)
        self.blocks.put(block)


    def unpause(self):
        if self.stream.is_stopped():
            self.stream.start_stream()

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()

    def sound_blocks(self):
        yield self.blocks.get()

    @property
    def channels(self):
        return self.config["channels"]

    @property
    def format(self):
        return self.config["format"]

    @property
    def samplewidth(self):
        return self.pyaudio.get_sample_size(self.format)

    @property
    def rate(self):
        return self.config["rate"]
