print("START")

import tkinter as tk
from ui import PokerUI


def main():

    print("OPEN GUI")

    root = tk.Tk()

    app = PokerUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()