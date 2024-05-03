"""Final GUI for Chatbot

    Sets up and displays the graphical UI for the Chatbot.
    Uses customtkinter - to allow for consistency over systems (Windows vs. MacOS)
    
"""

import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import customtkinter

import os
import sys

from Models.newlb_model import rec_letterbox

# import chatbot
sys.path.append(os.path.abspath(".."))
from controller import handle_msg

# basic version with tkinter created using
# https://medium.com/@vishwanathmuthuraman_92476/building-a-chatbot-with-python-and-tkinter-library-for-the-gui-390a747dadf6


##################################### GENERAL GUI DEFINITION #############################
root = customtkinter.CTk()
root.title("Movie Recommendation Chatbot")

# Logo
logo = Image.open("GUI/images/logo.jpeg").resize((300, 100))
photo = ImageTk.PhotoImage(logo)
Button(
    root,
    image=photo,
).grid(row=0, columnspan=3, pady=(10, 0))

# Scrollbar
scrollbar = Scrollbar(root, orient="vertical")

# Chat text area
text_area = tkinter.Text(
    root,
    bg="white",
    fg="black",
    width=82,
    height=20,
    wrap="word",
    relief=FLAT,
    font=("Helvetica" + "bold"),
    yscrollcommand=scrollbar.set,
)
text_area.grid(row=2, columnspan=3)
text_area.yview_scroll

# User input field
user_field = customtkinter.CTkEntry(root, corner_radius=3, width=325, exportselection=0)
user_field.grid(row=4, column=1, padx=(10, 10), pady=(10, 10), sticky="news")
user_field.bind("<Return>", (lambda event: send_message()))

# Enter button
# MUST attribute license
# "https://www.flaticon.com/free-icons/paper-plane by smashicons"
send = customtkinter.CTkImage(
    light_image=Image.open("GUI/images/plane.png"), size=(32, 32)
)
button = customtkinter.CTkButton(
    master=root,
    fg_color=("#4995ff", "#4995ff"),
    image=send,
    text="",
    corner_radius=10,
    width=50,
    height=50,
    command=lambda: send_message(),
).grid(row=4, column=2, pady=(10, 10), padx=(0, 10))

# Letterboxd button
pic_lib = customtkinter.CTkImage(
    light_image=Image.open("GUI/images/lb.png"), size=(114, 50)
)
lb_button = customtkinter.CTkButton(
    root,
    text="",
    image=pic_lib,
    compound=BOTTOM,
    command=lambda: letterbox_connect(),
    width=114,
    height=50,
    corner_radius=0,
    fg_color="black",
    hover_color="#6e6e6e",
).grid(row=4, column=0, pady=(10, 10), padx=(10, 0))

# text config for chat labels
text_area.tag_configure(
    "boldtextuser",
    background="#4995ff",
    font=("Helvetica" + "bold"),
    foreground="white",
)
text_area.tag_configure(
    "boldtextbot",
    background="#d30000",
    font=("Helvetica" + "bold"),
    foreground="white",
)

# text config for chat content
text_area.tag_configure("hang", lmargin1=106, lmargin2=106, rmargin=20)
text_area.config(spacing1=5)
text_area.config(spacing2=5)
text_area.config(spacing3=5)

# Displaying Letterboxd button
text_area.window_create(END, window=lb_button, padx=200, pady=20)
text_area.config(state=DISABLED)

# open at the center of the screen
root.eval("tk::PlaceWindow . center")
root.configure(fg_color="#303030")

w = 750  # width for the Tk root
h = 1000
# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

# set the dimensions of the screen
# and where it is placed
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

############################## STREAMING SERVICE BUTTONS #######################
streaming_toggles = {
    "Amazon Prime": True,
    "Disney Plus": True,
    "HBO Max": True,
    "Hulu": True,
    "Netflix": True,
    "Paramount": True,
}
toggle_buttons = []  # this needs to be populated after the buttons are determined


def toggle(btn, label, e_color):
    streaming_toggles[label] = not streaming_toggles[label]
    if streaming_toggles[label]:
        btn.configure(fg_color=e_color)
    else:
        btn.configure(fg_color="#4a4949")
    print(streaming_toggles[label])


# toggle button frame
bottom_frame = tkinter.Frame(root)
bottom_frame.grid(row=1, column=0, columnspan=3, pady=(10, 10))

bw = round(650 / len(streaming_toggles))

AMAZON_PRIME = "Amazon Prime"
ap_color = "#007BFF"
amazon_prime = customtkinter.CTkButton(
    bottom_frame,
    text=AMAZON_PRIME,
    command=lambda: toggle(amazon_prime, AMAZON_PRIME, ap_color),
    width=bw,
    corner_radius=0,
    fg_color=ap_color,
)
amazon_prime.grid(row=0, column=0)

DISNEY_PLUS = "Disney Plus"
dp_color = "#3362CC"
disney_plus = customtkinter.CTkButton(
    bottom_frame,
    text=DISNEY_PLUS,
    command=lambda: toggle(disney_plus, DISNEY_PLUS, dp_color),
    width=bw,
    corner_radius=0,
    fg_color=dp_color,
)
disney_plus.grid(row=0, column=1)

HBO_MAX = "HBO Max"
hbo_color = "#664A99"
hbo_max = customtkinter.CTkButton(
    bottom_frame,
    text=HBO_MAX,
    command=lambda: toggle(hbo_max, HBO_MAX, hbo_color),
    width=bw,
    corner_radius=0,
    fg_color=hbo_color,
)
hbo_max.grid(row=0, column=2)

HULU = "Hulu"
hulu_color = "#993166"
hulu = customtkinter.CTkButton(
    bottom_frame,
    text=HULU,
    command=lambda: toggle(hulu, HULU, hulu_color),
    width=bw,
    corner_radius=0,
    fg_color=hulu_color,
)
hulu.grid(row=0, column=3)

NETFLIX = "Netflix"
n_color = "#CC1933"
netflix = customtkinter.CTkButton(
    bottom_frame,
    text=NETFLIX,
    command=lambda: toggle(netflix, NETFLIX, n_color),
    width=bw,
    corner_radius=0,
    fg_color=n_color,
)
netflix.grid(row=0, column=4)

PARAMOUNT = "Paramount"
p_color = "#FF0000"
paramount = customtkinter.CTkButton(
    bottom_frame,
    text=PARAMOUNT,
    command=lambda: toggle(paramount, PARAMOUNT, p_color),
    width=bw,
    corner_radius=0,
    fg_color=p_color,
)
paramount.grid(row=0, column=5)


###################################### LETTERBOXD CONNECTION #############################
def letterbox_connect():
    """Connects Letterboxd to Chatbot"""

    global lb_button
    popup_window = tkinter.Toplevel(root)
    popup_window.title("Connect Letterboxd")

    popup_width = 450
    popup_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - popup_width) // 2
    y = (screen_height - popup_height) // 2
    popup_window.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    icon = Image.open("GUI/images/foldericon.jpg").resize((350, 310))
    folder_icon = ImageTk.PhotoImage(icon)
    label_icon = tkinter.Label(popup_window, image=folder_icon)
    label_icon.image = folder_icon  # Keep a reference to the image
    label_icon.pack(pady=10)

    label_username = tkinter.Label(popup_window, text="Enter your username:")
    label_username.pack()

    # Add an entry widget for the user to input their username
    entry_username = tkinter.Entry(popup_window, width=40, font=("Arial", 12))
    entry_username.pack()

    # Function to handle when the user clicks the "Submit" button
    def submit_username():
        """Get Letterboxd data given a username"""

        username = entry_username.get()
        if username:
            popup_window.destroy()
            text_area.config(state=NORMAL)
            text_area.insert(tkinter.END, f"\n   ")
            text_area.insert(tkinter.END, f"  FLIX Rec:  ", "boldtextbot")
            text_area.insert(
                tkinter.END,
                f"\t Collecting data for Username: '{username}'...",
                "hang",
            )
            text_area.config(state=DISABLED)
            root.update()  # Update the GUI to show changes immediately
            try:
                movies = rec_letterbox(username)
            except Exception as e:
                messagebox.showerror("Error", f"This Username is not valid: {str(e)}")
                root.update()  # Update the GUI to show changes immediately
            genres = list(movies.keys())

            text_area.config(state=NORMAL)
            text_area.insert(tkinter.END, f"\n   ")
            text_area.insert(tkinter.END, f"  FLIX Rec:  ", "boldtextbot")
            text_area.insert(
                tkinter.END,
                f"\t Here are your personalized movie recs according to your letterboxd: \n"
                + f"'{genres[0]}': '{movies[genres[0]][0]}'... Description: '{movies[genres[0]][1]}' \n"
                + f"'{genres[1]}': '{movies[genres[1]][0]}'... Description: '{movies[genres[1]][1]}' \n "
                + f"'{genres[2]}': '{movies[genres[2]][0]}'... Description: '{movies[genres[2]][1]}' \n",
                "hang",
            )
            text_area.config(state=DISABLED)
            root.update()  # Update the GUI to show changes immediately
        else:
            messagebox.showerror("Error", "Please enter a username.")

    # Add a button to submit the username
    button_submit = tkinter.Button(popup_window, text="Submit", command=submit_username)
    button_submit.pack()


###################################### TKINTER FUNCTIONS #########################################
def get_root():
    return root


def chat_response(user_input):
    """Generates a Chatbot response, given some user input

    Args:
        user_input (str): user's text input

    Returns:
        str: Chatbot's response
    """

    # Normalize the user's input
    user_input = user_input.lower()
    streaming = [s for s in streaming_toggles.keys() if streaming_toggles[s]]

    # Send input to controller
    response = handle_msg(user_input, streaming)

    return response


def loading_message(_):
    """Displays loading message while data for Chatbot loads"""

    text_area.config(state=NORMAL)
    text_area.insert(tkinter.END, f"\n   ")
    text_area.insert(
        tkinter.END,
        f"\t One second, data is still loading...\n",
        "hang",
    )
    text_area.config(state=DISABLED)


def greeting_message(_):
    """Displays a greeting message from the Chatbot once data has loaded"""

    text_area.config(state=NORMAL)
    text_area.insert(tkinter.END, f"\n   ")
    text_area.insert(tkinter.END, f"  FLIX Rec:  ", "boldtextbot")
    text_area.insert(
        tkinter.END,
        f"\t Hi! Welcome to the FLIX Rec Movie Recommendation Engine.\n"
        + f"Please enter a short plot description of a movie you would like to see "
        + f"or your preferred genre, "
        + f"or click the button below to connect your Letterboxd for a personalized recommendation!\n",
        "hang",
    )
    text_area.config(state=DISABLED)


def send_message():
    """When a user has inputted something and hits the send button, takes the input and displays Chatbot's response"""

    # Get user input
    user_input = user_field.get()

    # Clear input fields
    user_field.delete(0, tkinter.END)

    # Create response
    response = chat_response(user_input)

    # Display response
    text_area.config(state=NORMAL)
    text_area.insert(tkinter.END, f"\n   ")
    text_area.insert(tkinter.END, f"      User:     ", "boldtextuser")
    text_area.insert(
        tkinter.END,
        f"\t {user_input}\n\n",
        "hang",
    )
    text_area.insert(tkinter.END, f"   ")
    text_area.insert(tkinter.END, f"  FLIX Rec:  ", "boldtextbot")
    text_area.insert(tkinter.END, f"\t {response}\n\n", "hang")
    text_area.config(state=DISABLED)
    text_area.see(tkinter.END)


############################# EVENTS TO BE CALLED FROM MAIN ####################

root.bind("<<loading>>", loading_message)
root.bind("<<greet>>", greeting_message)


############################## run func #########################################
def run():
    root.mainloop()
