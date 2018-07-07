import uasyncio as asyncio
from time import ticks_ms
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("ArtPart")

class ArtPart():
    """base class for logical and physical components of an art project"""

    def __init__(self, name=None, duration=None, director=None):
        """ duration: msec for one cycle. if None, then run forever (e.g. a button)"""
        if name is None:
            self.name = "unknown" + str(ticks_ms())
        else:
            self.name = name
        self.duration = duration
        self.refresh_rate = 15
        self.cmds = {"stop":self.stop}
        self.director = director

    async def update(self):
        self.seq_start = ticks_ms()
        while self.running:
            self.seq_ms = ticks_diff(ticks_ms(), self.start)
            if self.seq_ms > self.duration:
                self.seq_start = ticks_ms()
                self.seq_ms = 0
            if self.refresh_rate <= 0:
                await asyncio.sleep_ms(200)
            else:
                log.debug("duration={}, seq_ms={},seq_start={}".format(
                            self.duration, self.seq_ms, self.seq_start))
                if self.need_update:
# add code to update the part here
                    log.error("update not implemented")  # remove this line
                    self.need_update = False
                await asyncio.sleep_ms(self.refresh_rate)

    async def stop(self):
        self.running = False
        log.info("{}: stopping".format(self.name))

    async def wait_for_start(self, start_ms):
        delay = start_ms - self.seq_ms
        # may need to put bounds on this difference so it starts close to correct start time but not too far off
        if delay > 0:
            await asyncio.sleep_ms(delay)

    def cmd(self, e):
        if 'cmd' not in e or e['cmd'] not in self.cmds:
            log.warning("{}: Command not found".format(self.name))
            log.warning(e)
            return
        cmd_str = e['cmd']
        cmd_func = self.cmds[cmd_str]
        del e['cmd']
        log.debug("{}: received cmd: {}".format(self.name, cmd_str))
        log.debug("{}: params: {}".format(self.name, e))
        loop = asyncio.get_event_loop()
        loop.create_task(cmd_func(**e))


if __name__ == '__main__':
    ap = ArtPart(name='test')
    ap.cmd({"cmd":"stop"})

