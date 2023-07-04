import re
import os
from datetime import date

# Tells you if you are running wangblows OS
def is_wangblows():
    return os.name == "nt"

# A generalized class for a knowledge base configuration across different OSs
class KBConfig:
    name = ""
    WINDOWS_ROOT = ""
    LINUX_ROOT = ""
    OSX_ROOT = ""
    def __init__(self, name, WINDOWS_ROOT, LINUX_ROOT, OSX_ROOT):
        self.name = name
        self.WINDOWS_ROOT = WINDOWS_ROOT
        self.LINUX_ROOT = LINUX_ROOT
        self.OSX_ROOT = OSX_ROOT
    def __str__(self):
        return f"{self.name}{self.WINDOWS_ROOT}{self.LINUX_ROOT}{self.OSX_ROOT}"
    def get_root(self):
        if is_wangblows():
            return self.WINDOWS_ROOT
        else:
            return self.LINUX_ROOT

# parses a KBconfig
def get_config():
    with open("myosotis.config", "r") as f:
        config_lines = f.readlines()
        #find the line containing WINDOWS_ROOT
        name = ""
        WINDOWS_ROOT = ""
        LINUX_ROOT = ""
        OSX_ROOT = ""
        for line in config_lines:
            if "NAME" in line:
                name = line.split("=")[1].strip()
            if "WINDOWS_ROOT" in line:
                WINDOWS_ROOT = line.split("=")[1].strip()
            if "LINUX_ROOT" in line:
                LINUX_ROOT = line.split("=")[1].strip()
            if "OSX_ROOT" in line:
                OSX_ROOT = line.split("=")[1].strip()
            if "JOURNAL" in line:
                JOURNAL = line.split("=")[1].strip()
        config =  KBConfig(name, WINDOWS_ROOT, LINUX_ROOT, OSX_ROOT)

        return config
    

# returns the filename of today's entry from your journal
def get_todays_dailynote(path_to_journal_entries):
    today = date.today()
    latest_file = path_to_journal_entries + today.strftime("%Y-%m-%d.md")
    return latest_file

# returns TRUE if a string is the title of a date note
# i.e. 1970-01-01
def is_dailynote(title):
    dailynote_regex = "\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])"
    if re.match(dailynote_regex, title):
        return True
    else:
        return False

# find every markdown note in a directory
# fullpath: returns the full path to the file
def find_every_instance_of_note(directory, fullpath=False):
    list_of_notes = []
    for path, subdirs, files in os.walk(directory):
        for found_file in files:
            if found_file.endswith(".md"):
                if fullpath:
                    list_of_notes.append(str(path) + "/" + found_file)
                else:
                    list_of_notes.append(found_file)
    return list_of_notes

# Returns the most likely match for a note name
def search_for_filename(title):
    top_level_directory = get_config().get_root()
    yournotes = find_every_instance_of_note(top_level_directory, True)
    # Exact match
    # TODO - these are doing the wrong kind of comparisons - 
    # they should be comparing the title to the note name,
    # not the filename
    for note in yournotes:
        DEBUG = False
        if DEBUG:
            print(note.split("\\")[-1].split("/")[-1].split(".md")[0].upper())
        if note.split("\\")[-1].split("/")[-1].upper() == title.upper():
            if ".part" not in note:
                print("returning " + note)
                return note
    print("No exact match found for " + title)
    # Partial match
    for note in yournotes:
        if title.upper() in note.upper():
            if ".part" not in note:
                print("returning " + note)
                return note
    print("No match found for " + title)
    return None

# forms a connection between two notes
def form_connection(note1, note2, joke=""):
    # Check if a connection exists between the two notes
    n1reader = open(note1, "r")
    n2reader = open(note2, "r")
    n1string = n1reader.read()
    n2string = n2reader.read()
    if (note1 in n2string) or (note2 in n1string):
        pass
    else:
        print(f"Forming a connection between {note1} and {note2}")
        n1writer = open(note1, "a")
        n2writer = open(note2, "a")
        n1writer.write(f"\n\n{joke}[[{note2}]]")
        n2writer.write(f"\n\n{joke}[[{note1}]]")
    n1reader.close()
    n2reader.close()

# outputs the zen of Myosotis
def this():
    # Note 2023-07-06: Writing the zen for your own package 
    # is a mistake but I have to do it
    # TODO: Please submit a pull request on this function
    zen = '''
    Privacy first.
    Privacy second.
    Safety third.
    Security and so forth as additional considerations.
    Remembering is better than not remembering.
    Everything not saved will be lost.
    Forgetting is okay.
    Not everything needs to be remembered.
    Spelling counts -- names really want to be spelled correctly.
    Typographical errors often contain important semantic data.
    Avoid adding tags and special markings to notes.
    Organization can be both implicit and explicit.
    Creating links between notes requires a human touch.
    Research isn't supposed to be easy.
    Uncovering knowledge takes an infuriating amount of time.
    Unless you have the patience of a python.
    If it's been done before, it's a boring idea to do it the same way again.
    If it's never been done, it might be an interesting thing to do.
    Named entity recognition is a fantastic idea -- let's do more of that!
    '''
    print(zen)