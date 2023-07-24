# unified intake for knowledgebase

import random
import os, webbrowser, datetime
from myosotis import *


def predictions():
    prediction = input("Make a prediction about something: ")
    resodate = input(
        "Enter a date that this prediction will be resolved by (YYYY-MM-DD): "
    )
    todays_date = datetime.datetime.now().strftime("%Y-%m-%d")
    confidence = input("How confident are you in this prediction, as a percentage? ")
    assert len(resodate) == 10
    assert resodate[4] == "-"
    assert int(resodate[5:7]) <= 12
    assert int(resodate[8:10]) <= 31
    description = input("Additional description of your prediction: ")
    # Append to a new file in the parts directory
    partsfile = open(parts_directory + f"{resodate}.md.part", "a+")
    partsfile.write(
        f"Prediction from [[{todays_date}]]: {prediction} (confidence: {confidence}%)\n"
    )
    if description:
        partsfile.write(f"- {description}\n")
    # todo - append to predictions csv spreadsheet(?)
    print("✨ Added to " + partsfile.name + " ✨\n")


# Paper receipt intake
def receipts():
    exit = False
    while not exit:
        place = input("Enter the place you went, or type 'x' to exit: ")
        if "x" in place and len(place) <= 2:
            exit = True
            break
        else:
            date = input("Enter a date (YYYY-MM-DD): ")
            assert len(date) == 10
            assert date[4] == "-"
            assert int(date[5:7]) <= 12
            assert int(date[8:10]) <= 31
            description = input('Additional description: "Went to ' + place + " ... ")
            if random.randint(0, 10) == 7:
                description = description + " " + input("Elaborate just a bit more: ")
            amount = input("Enter an amount in USD (or hit Enter): ")
        # Append to a new file in the parts directory
        partsfile = open(parts_directory + f"{date}.md.part", "a+")
        partsfile.write(f"Went to {place}")
        if description:
            partsfile.write(f" {description}")
        if amount != "":
            partsfile.write(f" (${amount})")
        partsfile.write("\n")
        print("✨ Added to " + partsfile.name + " ✨\n")
        partsfile.close()


# TODO
# Browser bookmark intake
def bookmarks():
    # copied from https://codereview.stackexchange.com/questions/246002/parse-html-bookmarks-file-to-json-using-python
    from bs4 import BeautifulSoup
    import requests

    exit = False
    while not exit:
        url = input("Enter the URL of a bookmark, or type 'exit': ")
        if len(url) < 6:
            exit = True
            break
        assert "http" in url
        # get the title of the page
        try:
            req = requests.get(url)
            soup = BeautifulSoup(req.text, "html.parser")
            title = soup.title.string
            # TODO - this is a hacky way to force manual entry of reddit titles
            if "reddit" in url:
                title = None
        except:
            title = None
        if title:
            print(f"Found title: {title}")
        else:
            title = input("Unable to find a title, please enter one: ")
        partnote_title = input("Enter the title of the note to append to: ")
        assert ".md" not in partnote_title
        assert len(partnote_title) > 2
        description = input("Enter a description of the bookmark: ")
        partnote_text = f"\n[{title}]({url})"
        if description:
            partnote_text += f"\n - {description}"
        else:
            ADD_TODO = input("Add a TODO? (Y/N): ")
            if ADD_TODO.upper() == "Y":
                partnote_text += " - TODO\n"

        partnote_file = os.path.join(
            get_config().get_root(), "shop/parts/" + partnote_title + ".md.part"
        )
        with open(partnote_file, "a+", encoding="utf-8") as f:
            f.write(partnote_text)
        print("✨ Added to " + partnote_file + " ✨\n")


def runs():
    exit = False
    while not exit:
        # TODO strava API (?)
        # we could get info from the Strava API, but that wouldn't really tell us where the runs were
        distance = input("How many miles did you run? ")
        location = input(f"Enter the location of the run: Ran {distance} miles ... ")
        date = input("Enter a date (YYYY-MM-DD): ")
        assert len(date) == 10
        assert date[4] == "-"
        assert int(date[5:7]) <= 12
        assert int(date[8:10]) <= 31
        description = input("Additional description: ")
        # Append to a new file in the parts directory
        partsfile = open(parts_directory + f"{date}.md.part", "a+")
        partsfile.write(f"Ran {distance} miles {location}")
        if description:
            partsfile.write(f" {description}")
        print("✨ Added to " + partsfile.name + " ✨\n")


# Append one file to the other
# parameter 1: the whole filepath of the file to append to
# parameter 2: the file to append
# Returns true if two files were merged
def merge_files(wholefile, partfile):
    print(f"Attempting to merge {partfile} to {wholefile}")
    with open(wholefile, "r", encoding="utf-8") as f1:
        print("Attempting to open " + partfile)
        with open(partfile, "r", encoding="utf-8") as f2:
            contents1 = f1.read()
            contents2 = "\n" + f2.read()
    f1.close()
    f2.close()
    print(contents1)
    print("+" * 28)
    print(contents2)
    continuation_option = input(
        "Press ENTER to append at the end, (i) to insert, or (d) to delete: "
    )
    if continuation_option == "":
        # Optionally create a bullet point for each line
        # contents2 = contents2.replace("\n", "\n- ")
        with open(wholefile, "w", encoding="utf-8") as f1:
            if is_dailynote(wholefile):
                f1.write(contents1 + contents2)
            else:
                f1.write(contents1 + contents2)
        f1.close()
        print("Merged " + wholefile + " and " + partfile)
        return True
    elif continuation_option == "i":
        # reprint the contents with line numbers
        print("Contents of " + wholefile + ":\n")
        for i, line in enumerate(contents1.splitlines()):
            print(f"{i+1}: {line}")
        # get the line number to insert at
        int(input("Enter the line number to insert at: "))

        ## TODO
        with open(wholefile, "w", encoding="utf-8") as f1:
            f1.write(contents1)
        print("Merged " + wholefile + " and " + partfile)
        return True
    elif continuation_option == "d":
        # Delete the partfile
        os.remove(partfile)
        print("Deleted " + partfile)
        return False
    else:
        print("Aborting merge")
        return False


# Append a partfile to its corresponding file in the KB
# Input: Full URL of a partfile
def merge_part(partfile):
    partfile_shortname = partfile.split("/")[-1]
    partfile_shortname = partfile_shortname.replace(".part", "")
    print("searching for a matching file for " + partfile_shortname)
    note = search_for_filename(partfile_shortname)
    if note:
        print("Found a matching file for " + partfile_shortname + " in " + note)
        print("attempting to merge " + partfile + " to " + note)
        merge_file_success = merge_files(note, partfile)
        if merge_file_success:
            delete_file = True
            if delete_file:
                os.remove(partfile)
    else:
        print("No matching file found for " + partfile_shortname)
        create_new = input("Create a new note for " + partfile_shortname + "? (y/n) ")
        if create_new == "y":
            # The partfile becomes the new note (!)
            os.rename(partfile, partfile_shortname)
            print("Renamed " + partfile + " to " + partfile_shortname)
        else:
            print("Well alright, do you want to delete " + partfile + " then? (y/n)")
            if input() == "y":
                os.remove(partfile)
                print("Deleted " + partfile)
        return


def get_first_file(folder):
    found_files = os.listdir(folder)
    if found_files:
        for file in found_files:
            if file.endswith(".md.part"):
                return file
    else:
        return None


def merge_files_loop(interactive=True):
    user_wants_to_continue = True
    if interactive:
        while user_wants_to_continue:
            first_file = get_first_file(parts_directory)
            if first_file:
                partfile = parts_directory + first_file
                # print the partfile
                with open(partfile, "r", encoding="utf-8") as f:
                    print(f.read())
                f.close()
                merge_part(partfile)
            user_wants_to_continue = (
                input("Press ENTER to continue, or any other key to exit: ") == ""
            )
    else:
        first_file = get_first_file(parts_directory)
        while first_file:
            partfile = parts_directory + first_file
            merge_part(partfile)
            first_file = get_first_file(parts_directory)


parts_directory = os.path.join(get_config().get_root(), "shop/parts/")


def dispatcher():
    print("INTAKE")
    print("1. Receipts Intake Loop")
    print("2. Merge Partfiles")
    print("3. Bookmarks Intake Loop")
    print("4. Runs and jogs")
    print("5. Automatically merge partnotes")
    print("6. Predictions")
    choice = input("Enter your choice: ")
    if choice == "1":
        receipts()
    elif choice == "2":
        merge_files_loop()
    elif choice == "3":
        bookmarks()
    elif choice == "4":
        webbrowser.open("https://www.strava.com/athlete/training")
        runs()
    elif choice == "5":
        merge_files_loop(interactive=False)
    elif choice == "6":
        predictions()
    else:
        print("Invalid choice")
        dispatcher()


dispatcher()
