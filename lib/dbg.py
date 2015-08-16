import sys


class Dbg():
    def __init__(self, verbose, bar_length=50):
        self._verbose = verbose
        self._bargraph_msg = None
        self._bargraph_min = None
        self._bargraph_max = None
        self._newline = True
        self._bar_length = bar_length
        self._prev_percent = None

    def debug(self, msg, level=2):
        if self._verbose >= level:
            if not self._newline:
                sys.stderr.write('\n')
                self._newline = True
            sys.stderr.write('%s\n' % msg)
            sys.stderr.flush()

    def msg(self, msg, level=1):
        if self._verbose >= level:
            if not self._newline:
                sys.stderr.write('\n')
                self._newline = True
            sys.stderr.write('%s\n' % msg)
            sys.stderr.flush()

    def print_bargraph(self, percent):
        if percent == self._prev_percent:
            return
        bar = (percent * self._bar_length) // 100
        sys.stderr.write('\r%s: [%s%s] %3d%%' % (
            self._bargraph_msg,
            '=' * bar,
            ' ' * (self._bar_length - bar),
            percent,
        ))
        sys.stderr.flush()
        self._prev_percent = percent
        self._newline = False

    def bargraph_start(self, msg, value_min=0, value_max=100, level=1):
        if self._verbose < level:
            return
        self._bargraph_msg = msg
        self._bargraph_min = value_min
        self._bargraph_max = value_max
        if not self._newline:
            sys.stderr.write('\n')
            self._newline = False
        sys.stderr.write('%s')
        self._prev_percent = None
        self._newline = False

    def bargraph_update(self, value=0, percent=None):
        if not self._bargraph_msg:
            return
        if percent is None:
            percent = 100 * (value - self._bargraph_min) // (self._bargraph_max - self._bargraph_min)
        self.print_bargraph(percent)

    def bargraph_done(self):
        if not self._bargraph_msg:
            return
        sys.stderr.write('\r%s: [%s] done\n' % (self._bargraph_msg, '=' * self._bar_length))
        sys.stderr.flush()
        self._newline = True
        self._bargraph_msg = None

    def set_verbose(self, verbose):
        self._verbose = verbose
