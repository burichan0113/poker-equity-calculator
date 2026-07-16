import tkinter as tk

from ui import PokerUI


def main():
    root = tk.Tk()
    PokerUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()