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
    l1 = lab.Link(0, lab.Link(2, lab.Link(2, lab.Link(3, lab.Link(1, lab.Link(2, lab.Link(3)))))))
    lab.remove_all(l1, 2)
    assert str(l1) == '<0 3 1 3>'
    lab.remove_all(l1, 3)
    assert str(l1) == '<0 1>'


def test_slice_link():
    link = lab.Link(3, lab.Link(1, lab.Link(4, lab.Link(1, lab.Link(5, lab.Link(9))))))
    new = lab.slice_link(link, 1, 4)
    assert str(new) == '<1 4 1>'


def test_store_digits():    
    s = lab.store_digits(1)
    assert str(s) == str(lab.Link(1))
    assert str(lab.store_digits(2345)) == str(lab.Link(2, lab.Link(3, lab.Link(4, lab.Link(5)))))
    assert str(lab.store_digits(876)) == str(lab.Link(8, lab.Link(7, lab.Link(6))))

    # ban str and reversed
    search = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(lab.store_digits)))
    print_error("str and/or reversed detected; please implement wihtout using.") if any([r in search for r in ["str", "reversed"]]) else None
    

def test_every_other():
    l = lab.Link('a', lab.Link('b', lab.Link('c', lab.Link('d'))))
    lab.every_other(l)
    assert l.first == 'a'
    assert l.rest.first == 'c'
    assert l.rest.rest is lab.Link.empty
    s = lab.Link(1, lab.Link(2, lab.Link(3, lab.Link(4))))
    lab.every_other(s)
    assert str(s) == str(lab.Link(1, lab.Link(3)))
    odd_length = lab.Link(5, lab.Link(3, lab.Link(1)))
    lab.every_other(odd_length)
    assert str(odd_length) == str(lab.Link(5, lab.Link(1)))
    singleton = lab.Link(4)
    lab.every_other(singleton)
    assert str(singleton) == str(lab.Link(4))


def test_duplicate_link():
    x = lab.Link(5, lab.Link(4, lab.Link(3)))
    lab.duplicate_link(x, 5)
    assert str(x) == str(lab.Link(5, lab.Link(5, lab.Link(4, lab.Link(3)))))
    y = lab.Link(2, lab.Link(4, lab.Link(6, lab.Link(8))))
    lab.duplicate_link(y, 10)
    assert str(y) == str(lab.Link(2, lab.Link(4, lab.Link(6, lab.Link(8)))))
    z = lab.Link(1, lab.Link(2, (lab.Link(2, lab.Link(3)))))
    lab.duplicate_link(z, 2)
    assert str(z) == str(lab.Link(1, lab.Link(2, lab.Link(2, lab.Link(2, lab.Link(2, lab.Link(3)))))))


def test_deep_map():
    l = lab.Link(1, lab.Link(lab.Link(2, lab.Link(3)), lab.Link(4)))
    assert str(lab.deep_map(lambda x: x * x, l)) == '<1 <4 9> 16>'
    assert str(l) == '<1 <2 3> 4>'
    assert str(lab.deep_map(lambda x: 2 * x, lab.Link(l, lab.Link(lab.Link(lab.Link(5)))))) == '<<2 <4 6> 8> <<10>>>'


def test_link_pop():
    lnk = lab.Link(1, lab.Link(2, lab.Link(3, lab.Link(4, lab.Link(5)))))
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