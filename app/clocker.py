from kivy.clock import Clock


class Clocker(object):
    def __init__(self, stream, dt=0.25, func=None):
        self.dt = dt
        self.stream_res = stream
        self.func = func

    def start(self):
        print("clock start!")
        self.clock = Clock.schedule_interval(
            lambda x: self.callback(), self.dt)

    def callback(self):
        code = self.stream_res.returncode
        if code:
            if self.stream_res.returncode == 0:
                self.destroy()
            else:
                print('failed')

    def destroy(self):
        Clock.unschedule(self.clock)
        print("clock destroyed!")

        if self.func:
            self.func()


class PlaceholderSerialPort(object):
    def __init__(self):
        self.device = "no device available"
