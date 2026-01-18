
from rich import print
import pyfiglet

def secure_mind_team_format():

    print(f"\n[bold italic white on red]{"-" * 30} Live Host Machine {"-" * 30}")
    print("[blue]*" * 79)
    print(pyfiglet.figlet_format("SecureMind Team", justify="center"))
    print("[blue]*" * 79)

