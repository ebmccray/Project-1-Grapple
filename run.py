# ======================================
# DESCRIPTION
# ======================================
# This is the primary executable file for the program.


# ======================================
# IMPORT
# ======================================
from command_handling import *
from main_menu import *
from event_handler import EventHandler


# ======================================
# EXECUTE
# ======================================
# Create an Event Handler for this session
app = EventHandler()

# Run the welcome script.
welcome()

# Run the main menu.
main_menu(app)

# Whenever the app is currently running and not in the middle of executing another function, get input from the user.
while app.running:
    get_input(app)