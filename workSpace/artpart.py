import uasyncio as asyncio


class ArtPart():
    """base class for logical and physical components of an art project"""

    def __init__(self, name=None, duration=None):
        """ duration: msec for one cycle. if None, then run forever (e.g. a button)"""
        if name is None:
            self.name = "unknown"
        else:
            self.name = name
        self.duration = duration
        self.cmds = {}

    async def update(self):
        """actually writes out pixel info every self.refresh_rate msecs
        runs asynchronously and should only be one running"""
        self.seq_start = ticks_ms()
        while self.running:
            self.seq_ms = ticks_diff(ticks_ms(), self.start)
            if self.seq_ms > self.seq_duration:
                self.seq_start = ticks_ms()
                self.seq_ms = 0
            if self.refresh_rate <= 0:
                await asyncio.sleep_ms(200)
            else:
                logging.debug("duration={}, seq_ms={},seq_start={}".format( \
                    self.seq_duration, self.seq_ms, self.seq_start))
                logging.debug("self[0]={}".format(self[0]))
                if self.need_update:
                    self.write()
                    self.need_update = False
                await asyncio.sleep_ms(self.refresh_rate)

    def stop(self):
        self.running = False

    async def wait_for_start(self, start_ms):
        delay = start_ms - self.seq_ms
        # may need to put bounds on this difference so it starts close to correct start time but not too far off
        if delay > 0:
            await asyncio.sleep_ms(delay)
