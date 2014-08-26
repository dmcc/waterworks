import sys
from cmd import Cmd
import ansi

class BetterCmdShell(Cmd):
    """An extension to cmd.Cmd which includes a lot of new features:

    - enable readline completion by default
    - Control-D quits
    - catch all exceptions and print them in red
    - expand unambiguous commands, report when expansions are ambiguous
    - help is better formatted
    - help all prints out help of all commands

    This code is not especially modular (i.e., you may only want some
    of these features) but some can be disabled/changed with proper
    subclassing.
    """
    def __init__(self, set_readline_completer=True):
        Cmd.__init__(self)
        if set_readline_completer:
            import readline
            readline.set_completer_delims(' \t\n')

    def do_quit(self, arg):
        """Exit the program."""
        print "\nBye!"
        return True

    def onecmd(self, line):
        try:
            return Cmd.onecmd(self, line)
        except SystemExit:
            raise
        except:
            from waterworks.Tools import get_current_traceback_tuple
            exc_class, exc, desc = get_current_traceback_tuple()
            print ansi.RED + ''.join(desc).strip() + ansi.BOLD
            if exc is None:
                print exc_class
            else:
                print "%s: %s" % (exc_class.__name__, exc)
            sys.stdout.write(ansi.RESET)

    def default(self, line):
        """Called when an unknown command is entered."""
        if line == 'EOF':
            return self.onecmd('quit')
        else:
            pieces = line.split(' ', 1)
            command = pieces[0]
            rest = pieces[1:] or ['']
            matches = [d.replace('do_', '')
                for d in dir(self) if d.startswith('do_') and \
                    d.replace('do_', '').startswith(command)]
            if len(matches) == 1:
                newcommand = '%s %s' % (matches[0], rest[0])
                print "expanded>", newcommand
                self.onecmd(newcommand)
            elif matches:
                def highlight(text):
                    l = len(command)
                    text = text[:l] + ansi.RESET + text[l:]
                    text = ansi.RED + ansi.BOLD + text
                    return text
                print "Possible matches:"
                print '\t' + '\n\t'.join(highlight(match) for match in matches)
                print "Type a longer prefix to clarify."
            else:
                Cmd.default(self, line)

    def cmdloop(self, intro=None):
        try:
            Cmd.cmdloop(self, intro)
        except KeyboardInterrupt:
            self.onecmd('quit')

    def do_help(self, line):
        """I think you know what this does."""
        # this works around a misfeature in cmd.py
        # getdoc is better at docs than the raw (cleans them up)
        line = line.strip()
        try:
            if line and not getattr(self, 'help_' + line, None):
                from pydoc import getdoc
                docs = getdoc(getattr(self, 'do_' + line))
                if not docs:
                    docs = '(to be documented)'
                self.stdout.write("%s: %s\n" % (ansi.BOLD + line + ansi.RESET,
                                                str(docs)))
                return
        except:
            pass

        return Cmd.do_help(self, line)

    def help_all(self):
        print "All documented commands:"
        undocumented = []
        for attr in dir(self):
            if attr.startswith('do_'):
                method = getattr(self, attr)
                attr = attr.replace('do_', '')
                if not getattr(method, '__doc__'):
                    undocumented.append(attr)
                    continue
                self.do_help(attr)
        print
        print 'Undocumented:', ' '.join(undocumented)

    @staticmethod
    def make_completer(*possible_values):
        """This helps you build complete_* functions:
        complete_x = BetterCmdShell.make_completer('val1', 'val2', ...)"""
        def completer(self, text, *ignored):
            return [v for v in possible_values if v.startswith(text)]
        return completer
