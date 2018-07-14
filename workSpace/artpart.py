import uasyncio as asyncio
from time import ticks_ms, ticks_diff
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
        self.cycle_time = 0
        self.cycle_start = ticks_ms()
        self.num_cycles = 1
        self.need_update = True
        self.cmds = {"stop": self.stop,
                     "alive": self.alive}
        self.director = director
        self.running = True
        self.tasks = []
        loop = asyncio.get_event_loop()
        self.update_coro = self.update()
        loop.create_task(self.update_coro)

    async def update(self, cycles=None):
        if cycles is None:
            cycles = self.num_cycles
        cur_cycle = 0
        log.debug("running for %d cycles", cycles)
        self.running = True
        await asyncio.sleep_ms(0)
        while self.running and (cycles is None or cur_cycle < cycles):
            self.cycle_start = ticks_ms()
            log.debug("starting cycle %d at %d", cur_cycle, self.cycle_start)
            while True:
                self.cycle_time = ticks_diff(ticks_ms(), self.cycle_start)
                if self.duration is not None and self.cycle_time > self.duration:
                    # start the cycle back at 0
                    self.cycle_start = ticks_ms()
                    self.cycle_time = 0

                    log.debug("duration={}, cycle_time={},cycle_start={}".format(
                              self.duration, self.cycle_time, self.cycle_start))

                    break
                if self.refresh_rate < 0:
                    await asyncio.sleep_ms(200)
                else:
                    # log.debug("duration={}, cycle_time={},cycle_start={}".format(
                    #           self.duration, self.cycle_time, self.cycle_start))
                    if self.need_update:
                        self.need_update = self.do_update()
                    await asyncio.sleep_ms(self.refresh_rate)
            log.debug("duration={}, cycle_time={},cycle_start={}".format(
                self.duration, self.cycle_time, self.cycle_start))
            log.debug("end of cycle %d", cur_cycle)
            cur_cycle += 1

        self.running = False
        for t in self.tasks:
            asyncio.cancel(t)
        log.debug("exiting update coro at %d",ticks_ms())

    def do_update(self):
        # xxx add code to update the part here.
        # return False if update successful
        log.warning("update function not implemented")  # remove this line

    def run(self):
        """ run this part only. for dev purposes. normally, the artdirector starts the loop"""
        loop = asyncio.get_event_loop()
        self.running = True
        log.debug("starting update task")
        loop.run_until_complete(self.update_coro)

    async def stop(self):
        self.running = False
        log.info("{}: stopping".format(self.name))

    async def wait_for_start(self, start=None):
        if start is None or start <= 0:
            return
        delay = start - self.cycle_time
        # xxx may need to put bounds on this difference so it starts close to correct start time but not too far off
        if delay > 0:
            log.debug("waiting for %d msecs", delay)
            await asyncio.sleep_ms(delay)

    def cmd(self, cmd_dict=None, **kwargs):
        if cmd_dict is None:
            cmd_dict = kwargs
        else:
            cmd_dict = dict(cmd_dict, **kwargs)
        if 'cmd' not in cmd_dict or cmd_dict['cmd'] not in self.cmds:
            log.warning("{}: Command not found".format(self.name))
            log.warning(cmd_dict)
            return
        cmd_str = cmd_dict['cmd']
        cmd_func = self.cmds[cmd_str]
        cmd_task = cmd_func(**cmd_dict)

        log.debug("{}: received cmd: {}".format(self.name, cmd_str))
        log.debug("{}: params: {}".format(self.name, cmd_dict))
        loop = asyncio.get_event_loop()
        self.tasks.append(cmd_task)
        loop.create_task(cmd_task)

    async def alive(self, beat=3000, **kwargs): # xxx why doesn't it cactch the cancellederor'
        try:
            while self.running:
                log.info("%s is alive. cycle_time=%d", self.name, self.cycle_time)
                await asyncio.sleep_ms(beat)
        except asyncio.CancelledError:
                log.debug("alive cancelled")


if __name__ == '__main__':
    ap = ArtPart(name='test')
    ap.cmd({"cmd":"stop"})


