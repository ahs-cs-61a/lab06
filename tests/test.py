# lab06 tests


# IMPORTS

import labs.lab06 as lab, tests.wwpd_storage as s
import re, inspect, sys, git
from io import StringIO 

st = s.wwpd_storage


# CAPTURING PRINTS (STDOUT) - https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


# COLORED PRINTS - custom text type to terminal: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal, ANSI colors: http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html

class bcolors:
    HIGH_MAGENTA = '\u001b[45m'
    HIGH_GREEN = '\u001b[42m'
    HIGH_YELLOW = '\u001b[43m'
    MAGENTA = ' \u001b[35m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33;1m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\u001b[0m'
    
def print_error(message):
    print("\n" + bcolors.HIGH_YELLOW + bcolors.BOLD + "ERROR:" + bcolors.RESET + bcolors.YELLOW + bcolors.BOLD + " " + message + bcolors.ENDC)

def print_message(message):
    print("\n" + bcolors.HIGH_MAGENTA + bcolors.BOLD + "MESSAGE:" + bcolors.RESET + bcolors.MAGENTA + bcolors.BOLD + " " + message + bcolors.ENDC)

def print_success(message):
    print("\n" + bcolors.HIGH_GREEN + bcolors.BOLD + "SUCCESS:" + bcolors.RESET + bcolors.GREEN + bcolors.BOLD + " " + message + bcolors.ENDC)


# TESTS

def test_remove_all():
    l1 = Link(0, Link(2, Link(2, Link(3, Link(1, Link(2, Link(3)))))))
    lab.remove_all(l1, 2)
    assert str(l1) == '<0 3 1 3>': 
    lab.remove_all(l1, 3)
    assert str(l1) == '<0 1>'
    lab.remove_all(l1, 3)
    assert assert(l1) == '<0 1>'


def test_slice_link():
    link = Link(3, Link(1, Link(4, Link(1, Link(5, Link(9))))))
    new = lab.slice_link(link, 1, 4)
    assert str(new) == '<1 4 1>'


def test_store_digits():    
    s = lab.store_digits(1)
    assert s == Link(1)
    assert lab.store_digits(2345) == Link(2, Link(3, Link(4, Link(5))))
    assert lab.store_digits(876) == Link(8, Link(7, Link(6)))

    # ban str and reversed
    search = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(lab.store_digits)))
    print_error("str and/or reversed detected; please implement wihtout using.") if any([r in search for r in ["str", "reversed"]]) else None
    

def test_every_other():
    l = Link('a', Link('b', Link('c', Link('d'))))
    lab.every_other(l)
    assert l.first == 'a'
    assert l.rest.first == 'c'
    assert l.rest.rest is Link.empty
    s = Link(1, Link(2, Link(3, Link(4))))
    lab.every_other(s)
    assert s == Link(1, Link(3))
    odd_length = Link(5, Link(3, Link(1)))
    lab.every_other(odd_length)
    assert odd_length == Link(5, Link(1))
    singleton = Link(4)
    lab.every_other(singleton)
    assert singleton == Link(4)


def test_duplicate_link():
    x = Link(5, Link(4, Link(3)))
    lab.duplicate_link(x, 5)
    assert x == Link(5, Link(5, Link(4, Link(3))))
    y = Link(2, Link(4, Link(6, Link(8))))
    lab.duplicate_link(y, 10)
    assert y == Link(2, Link(4, Link(6, Link(8))))
    z = Link(1, Link(2, (Link(2, Link(3)))))
    lab.duplicate_link(z, 2)
    assert z == Link(1, Link(2, Link(2, Link(2, Link(2, Link(3))))))


def test_deep_map():
    s = Link(1, Link(Link(2, Link(3)), Link(4)))
    assert str(lab.deep_map(lambda x: x * x, s)) == '<1 <4 9> 16>'
    assert str(s) == '<1 <2 3> 4>'
    assert str(lab.deep_map(lambda x: 2 * x, Link(s, Link(Link(Link(5)))))) == '<<2 <4 6> 8> <<10>>>'


def test_link_pop():
    lnk = Link(1, Link(2, Link(3, Link(4, Link(5)))))
    removed = lab.link_pop(lnk)
    assert removed == 5
    assert str(lnk) == '<1 2 3 4>'
    assert lab.link_pop(lnk, 2) == 3
    assert str(lnk) == '<1 2 4>'
    assert lab.link_pop(lnk) == 4
    assert lab.link_pop(lnk) == 2
    assert str(lnk) == '<1>'


# CHECK WWPD? IS ALL COMPLETE

wwpd_complete = True

def test_wwpd():
    if len(st) != 7 or not all([i[4] for i in st]):
        print_error("WWPD? is incomplete.")
        wwpd_complete = False
    assert len(st) == 7
    assert all([i[4] for i in st])


# AUTO-COMMIT WHEN ALL TESTS ARE RAN

user = []

def test_commit():
    try:
        # IF CHANGES ARE MADE, COMMIT TO GITHUB
        user.append(input("\n\nWhat is your GitHub username (exact match, case sensitive)?\n"))
        repo = git.Repo("/workspaces/lab06-" + user[0])
        repo.git.add('--all')
        repo.git.commit('-m', 'update lab')
        origin = repo.remote(name='origin')
        origin.push()
        print_success("Changes successfully committed.")  
    except git.GitCommandError: 
        # IF CHANGES ARE NOT MADE, NO COMMITS TO GITHUB
        print_message("Already up to date. No updates committed.")
    except git.NoSuchPathError:
        # IF GITHUB USERNAME IS NOT FOUND
        print_error("Incorrect GitHub username; try again.")
        raise git.NoSuchPathError("")


# linked list class

class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s  # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)  # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'