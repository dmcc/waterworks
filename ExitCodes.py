"""Interpret exit statuses."""
__author__ = "David McClosky (dmcc AT cs.brown.edu)"

import os, signal

def signum_to_name(signum):
    for obj in dir(signal):
        if obj.startswith('SIG') and signum == getattr(signal, obj):
            return obj
    else:
        return None

def describe_exit_status(exitstatus, exitcodedescs=None):
    desc = []
    if os.WIFSIGNALED(exitstatus):
        signum = os.WTERMSIG(exitstatus)
        signame = signum_to_name(signum)
        if signame:
            signame = " (%s)" % signame
        else:
            signame = ""
        desc.append("Killed by signal %d%s" % (signum, signame))
    if os.WIFEXITED(exitstatus):
        exitcode = os.WEXITSTATUS(exitstatus)
        if exitcodedescs and exitcodedescs.get(exitcode):
            codedesc = " (%s)" % exitcodedescs.get(exitcode)
        else:
            codedesc = ''
        desc.append("Exited with code %d%s" % (exitcode, codedesc))
    if os.WIFSTOPPED(exitstatus):
        desc.append("Stopped by signal %d" % os.WSTOPSIG(exitstatus))
    if os.WCOREDUMP(exitstatus):
        desc.append("coredumped")
    return desc

class ExitCode(Exception):
    """Represents the exit code of a spawned command."""
    def __init__(self, exitcode, message=''):
        """exitcode is the exit status of a command, message is a
        description which will be prepended in the str() of this."""
        self.exitcode = exitcode
        self.message = message
        self.exitstatus = None
        if os.WIFEXITED(exitcode):
            self.exitstatus = os.WEXITSTATUS(exitcode)
    def __repr__(self):
        return "<%s: %s, message=%r>" % (self.__class__.__name__, 
                                         self.exitcode,
                                         self.message)
    def __str__(self):
        return "%s%s (exit status %s)" % \
               (self.message, 
                ', '.join(describe_exit_status(self.exitcode)),
                self.exitcode)

# a shorter version
describe = describe_exit_status

if __name__ == "__main__":
    import sys
    for status in sys.argv[1:]:
        print status, describe_exit_status(int(status))
