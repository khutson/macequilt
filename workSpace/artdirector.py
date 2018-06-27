

class ArtDirector():
    """manages mqtt messages and other commands between ArtProject components"""

    def __init__(self):
        pass

    def run(self,cycles=1):
        for c in range(cycles):
            await asyncio.sleep_ms(self.seq_duration)




class ArtPart():
    """base class for logical and physical components of an art project"""

    def __init__(self,duration=5000):
        self.duration = duration
