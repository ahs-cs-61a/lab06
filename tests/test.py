# lab05 tests


# IMPORTS

import labs.lab05 as lab
import tests.wwpd_storage as s
from io import StringIO 
import sys
import git

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

def test_keyboard():
    b1 = lab.Button(0, "H")
    b2 = lab.Button(1, "I")
    k = lab.Keyboard(b1, b2)
    assert k.buttons[0].key == 'H'
    assert k.press(1) == 'I'
    assert k.press(2) == ''
    assert k.typing([0, 1]) == 'HI'
    assert k.typing([1, 0]) == 'IH'
    assert b1.times_pressed == 2
    assert b2.times_pressed == 3


def test_minty_coin():
    mint = lab.Minty()
    assert mint.year == 2021
    dime = mint.create('Dime')
    assert dime.year == 2021
    lab.Minty.present_year = 2101
    nickel = mint.create('Nickel')
    assert nickel.year == 2021
    assert nickel.worth() == 35
    mint.update() 
    lab.Minty.present_year = 2176
    assert mint.create('Dime').worth() == 35
    assert lab.Minty().create('Dime').worth() == 10
    assert dime.worth() == 115


def test_smart_fridge():
    fridgey = lab.SmartFridge()
    assert fridgey.add_item('Mayo', 1) == 'I now have 1 Mayo'
    assert fridgey.add_item('Mayo', 2) == 'I now have 3 Mayo'
    assert fridgey.use_item('Mayo', 2.5) == 'I have 0.5 Mayo left'
    assert fridgey.use_item('Mayo', 0.5) == 'Oh no, we need more Mayo!'
    assert fridgey.add_item('Eggs', 12) == 'I now have 12 Eggs'
    assert fridgey.use_item('Eggs', 15) == 'Oh no, we need more Eggs!'
    assert fridgey.add_item('Eggs', 1) == 'I now have 1 Eggs'


def test_vending_machine():
    v = lab.VendingMachine('candy', 10)
    assert v.vend() == 'Nothing left to vend. Please restock.'
    assert v.add_funds(15) == 'Nothing left to vend. Please restock. Here is your $15.'
    assert v.restock(2) == 'Current candy stock: 2'
    assert v.vend() == 'Please update your balance with $10 more funds.'
    assert v.add_funds(7) == 'Current balance: $7'
    assert v.vend() == 'Please update your balance with $3 more funds.'
    assert v.add_funds(5) == 'Current balance: $12'
    assert v.vend() == 'Here is your candy and $2 change.'
    assert v.add_funds(10) == 'Current balance: $10'
    assert v.vend() == 'Here is your candy.'
    assert v.add_funds(15) == 'Nothing left to vend. Please restock. Here is your $15.'

    w = lab.VendingMachine('soda', 2)
    assert w.restock(3) == 'Current soda stock: 3'
    assert w.restock(3) == 'Current soda stock: 6'
    assert w.add_funds(2) == 'Current balance: $2'
    assert w.vend() == 'Here is your soda.'


def test_cat():
    print("\n\nCat('Thomas', 'Tammy').talk() prints:")
    with Capturing() as thomas_output:
        lab.Cat('Thomas', 'Tammy').talk()  
    thomas = ["Thomas says meow!"]
    if thomas_output != thomas:
        print_error("Incorrect prints from Cat('Thomas', 'Tammy').talk()")
    assert thomas_output == thomas


def test_noisy_cat():
    print("\n\nNoisyCat('Magic', 'James').talk() prints:")
    with Capturing() as magic_output:
        lab.NoisyCat('Magic', 'James').talk()
    magic = ["Magic says meow!", "Magic says meow!"]
    if magic_output != magic:
        print_error("Incorrect prints from NoisyCat('Magic', 'James').talk()")
    assert magic_output == magic


def test_account():
    a = lab.Account('John')
    assert a.deposit(10) == 10
    assert a.balance == 10
    assert a.interest == 0.02
    assert a.time_to_retire(10.25) == 2 
    assert a.balance == 10
    assert a.time_to_retire(11) == 5
    assert a.time_to_retire(100) == 117


def test_free_checking():
    ch = lab.FreeChecking('Jack')
    ch.balance = 20
    assert ch.withdraw(100) == 'Insufficient funds'
    assert ch.withdraw(3) == 17
    assert ch.balance == 17
    assert ch.withdraw(3) == 13
    assert ch.withdraw(3) == 9
    ch2 = lab.FreeChecking('John')
    ch2.balance = 10
    assert ch2.withdraw(3) == 7
    assert ch.withdraw(3) == 5
    assert ch.withdraw(5) == 'Insufficient funds'


# CHECK WWPD? IS ALL COMPLETE

wwpd_complete = True

def test_wwpd():
    if len(st) != 20 or not all([i[4] for i in st]):
        print_error("WWPD? is incomplete.")
        wwpd_complete = False
    assert len(st) == 20
    assert all([i[4] for i in st])


# AUTO-COMMIT WHEN ALL TESTS ARE RAN

user = []

def test_commit():
    try:
        # IF CHANGES ARE MADE, COMMIT TO GITHUB
        user.append(input("\n\nWhat is your GitHub username (exact match, case sensitive)?\n"))
        repo = git.Repo("/workspaces/lab05-" + user[0])
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