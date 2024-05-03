"""FlixREC: Movie Recommendation Chatbot
    
    This script allows the Chatbot to be run from the terminal.
    
"""

import threading

## run gui
from GUI.chat_gui import run as run_gui
from GUI.chat_gui import get_root
from Models.movie_models import load as movie_model_load


root = get_root()


def import_():
    # load model data
    root.event_generate("<<loading>>", when="tail")
    import Chatbot.moviebot

    Chatbot.moviebot.load()
    movie_model_load()
    root.event_generate("<<greet>>", when="tail")


import_thread = threading.Thread(target=import_)
import_thread.start()


def main():
    run_gui()
    # wait for the chatbot model to finish loading
    import_thread.join()


if __name__ == "__main__":
    main()
