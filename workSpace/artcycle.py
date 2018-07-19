# artcycle.py
# copyright 2018 Kent Hutson - MIT License
#
# subclass of artpart that implements cycling.
# Track time in the cycle so that functions that depend on time
# are more easily implemented

import uasyncio as asyncio
from time import ticks_ms, ticks_diff
from artpart import ArtPart, launch
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("ArtPart")


class ArtCycle(ArtPart):
    """base class for logical and physical components of an art project"""

    def __init__(self, name=None, duration=None, director=None):
        """ duration: msec for one cycle/song. if None, then run forever (e.g. a button)"""
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
        self.update_coro = None
        self.update_coro = self.start()

    async def update(self, cycles=None):
        """update the part
        The default method is meant to be used with something that needs refreshing,
        like lights. Can be overridden for simpler parts. Update is where any action
        needed by your part should take place. self.update_coro is the instance of the
        update coroutine - there should only be one update coro running."""
        if cycles is None:
            cycles = self.num_cycles
        cur_cycle = 0
        log.debug("running for %d cycles", cycles)
        self.running = True
        await asyncio.sleep_ms(0)
        while True: # self.running and ((cycles is None) or (cur_cycle < cycles)):
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
                    log.debug("duration={}, cycle_time={},cycle_start={}".format(
                              self.duration, self.cycle_time, self.cycle_start))
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
        #  add code to update the part here.
        log.warning("update function not implemented")  # remove this line
        return False        # return False if update successful


    def run(self):
        """ run this part only. for dev purposes. normally, the artdirector starts the loop
        use self.start() to start/restart the part"""
        loop = asyncio.get_event_loop()
        self.running = True
        log.debug("starting update task")
        log.debug("run: before start self.update_coro: %s", self.update_coro )
        self.start()
        log.debug("run: after start self.update_coro: %s", self.update_coro )
        # loop.run_until_complete(asyncio.sleep_ms(self.duration*self.num_cycles+1000))
        loop.run_until_complete(asyncio.sleep(15))

    def start(self, restart=False):
        """ensures that the update coroutine is alive
        restart: clear all tasks also"""
        if restart:
            self.stop()
        if self.update_coro is None:
            loop = asyncio.get_event_loop()
            self.update_coro = self.update()
            loop.create_task(self.update_coro)
        log.debug("start: self.update_coro: %s", self.update_coro )
        return self.update_coro

    def stop(self):
        self.running = False
        log.info("{}: stopping".format(self.name))
        while self.tasks:
            asyncio.cancel(self.tasks.pop())
        if self.update_coro:
            asyncio.cancel(self.update_coro)
        self.update_coro = None

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
        # loop = asyncio.get_event_loop()
        self.tasks.append(cmd_task)
        # loop.create_task(cmd_task)
        launch(cmd_func, cmd_dict)

    async def alive(self, beat=3000, **kwargs): # xxx why doesn't it cactch the cancellederor'
        try:
            while self.running:
                log.info("%s is alive. cycle_time=%d", self.name, self.cycle_time)
                await asyncio.sleep_ms(beat)
        except asyncio.CancelledError:
                log.debug("alive cancelled")

def test():
    duration = 10000
    print("TEST: test artpart with duration {}", duration)
    ap = ArtPart(name='test', duration=duration)
    ap.cmd(cmd="alive")
    print("TEST: running alive")
    ap.run()
    # print("TEST:canceling alive")
    # asyncio.cancel(ap.tasks[0])
    # ap.run()

if __name__ == '__main__':
    test()
