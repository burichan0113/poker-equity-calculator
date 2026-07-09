import tkinter as tk
from PIL import Image, ImageTk
import os


class CardImage:

    cache = {}


    @staticmethod
    def load(card, width, height):

        key = f"{card}_{width}_{height}"

        if key in CardImage.cache:
            return CardImage.cache[key]


        path = os.path.join(
            "cards",
            f"{card}.png"
        )


        if os.path.exists(path):

            img = Image.open(path)

            img = img.resize(
                (width,height),
                Image.Resampling.LANCZOS
            )

        else:

            img = Image.new(
                "RGB",
                (width,height),
                "white"
            )


        photo = ImageTk.PhotoImage(img)

        CardImage.cache[key] = photo

        return photo



class CardWidget(tk.Label):

    def __init__(
        self,
        parent,
        width=80,
        height=120
    ):

        super().__init__(
            parent,
            bg="white",
            relief="solid",
            borderwidth=2
        )


        self.width = width
        self.height = height
        self.image = None


        self.show_card("back")



    def show_card(self, card):

        self.image = CardImage.load(
            card,
            self.width,
            self.height
        )

        self.config(
            image=self.image
        )



class ActionButton(tk.Button):

    def __init__(
        self,
        parent,
        text,
        command=None
    ):

        super().__init__(
            parent,
            text=text,
            command=command,
            width=12,
            height=2,
            font=("Arial",14,"bold"),
            bg="#111",
            fg="white",
            relief="raised",
            borderwidth=3
        )