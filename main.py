# imports all the necessary requirements
# Tkinter (GUI), requests (API), re (regular expression), open_words (verb tool)
import tkinter as tk
import requests
import re
from open_words.parse import Parse

# sets the function Parse() from open_words equal to the variable parser
parser = Parse()


# creates the class for the Tkinter GUI
class MyApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # creates a static label that serves as the title, and sets font to Helvetica, size 26, and bold
        title = tk.Label(self, text="\nLatin Verb Tool", font='Helvetica 26 bold')
        title.pack()
        # sets the text background colour to match the background, and set text colour to white
        title.config(bg="#5589ad", fg="white")

        # code that adds a gap between two elements
        fill = tk.Label(self, text="", font="Helvetica 4")
        fill.pack()
        # sets the text background colour to match the background, and set text colour to white
        fill.config(bg="#5589ad")

        # creates a static label instructing the user to enter a verb, and sets font to Helvetica, size 18, and bold
        w = tk.Label(self, text="\nPlease enter a verb in Latin.", font='Helvetica 18 bold')
        w.pack()
        # sets the text background colour to match the background, and set text colour to white
        w.config(bg="#5589ad", fg="white")

        # code that adds a gap between two elements
        fill2 = tk.Label(self, text="", font="Helvetica 4")
        fill2.pack()
        # sets the text background colour to match the background, and set text colour to white
        fill2.config(bg="#5589ad")

        # creates an entry field that allows the user to enter a verb
        self.entry = tk.Entry(self)
        self.entry.pack()

        # in order for the mainloop to run properly, it needs to return something
        # this empty string is something for the mainloop to return without affecting the actual output
        self.string = ""

        # code that adds a gap between two elements (entry field and button)
        fill3 = tk.Label(self, text="", font="Helvetica 4")
        fill3.pack()
        # sets the text background colour to match the background, and set text colour to white
        fill3.config(bg="#5589ad")

        # creates a button that submits the user entry and runs it in the conjugate function defined below
        button = tk.Button(self, text="Go!", command=self.conjugate, font='Helvetica 18 bold')
        button.pack()

        # creates the first of the many output labels
        self.label = tk.Label(self, text="", font='Helvetica 18 bold')
        self.label.pack()
        # sets the text background colour to match the background, and set text colour to white
        self.label.config(bg="#5589ad", fg="white")

        # creates a label that provides the user with the definition of the word they entered
        self.deflabel = tk.Label(self, text="", font='Helvetica 18 bold')
        self.deflabel.pack()
        # sets the text background colour to match the background, and set text colour to white
        self.deflabel.config(bg="#5589ad", fg="white")

        # creates a label that tells the user that the following labels are for tense, voice, mood, etc.
        self.tvmintro = tk.Label(self, text="", font='Helvetica 18 bold')
        self.tvmintro.pack()
        # sets the text background colour to match the background, and set text colour to white
        self.tvmintro.config(bg="#5589ad", fg="white")

        # creates a label that gives the tense of the verb the user entered
        self.tense = tk.Label(self, text="", font='Helvetica 18 bold')
        self.tense.pack()
        # sets the text background colour to match the background, and set text colour to white
        self.tense.config(bg="#5589ad", fg="white")

        # creates a label that gives the voice of the verb the user entered
        self.voice = tk.Label(self, text="", font='Helvetica 18 bold')
        self.voice.pack()
        # sets the text background colour to match the background, and set text colour to white
        self.voice.config(bg="#5589ad", fg="white")

        # creates a label that gives the mood of the verb the user entered
        self.mood = tk.Label(self, text="", font='Helvetica 18 bold')
        self.mood.pack()
        # sets the text background colour to match the background, and set text colour to white
        self.mood.config(bg="#5589ad", fg="white")

        # creates a label that gives the person of the verb the user entered
        self.person = tk.Label(self, text="", font='Helvetica 18 bold')
        self.person.pack()
        # sets the text background colour to match the background, and set text colour to white
        self.person.config(bg="#5589ad", fg="white")

        # creates a label that gives the number of the verb the user entered
        self.number = tk.Label(self, text="", font='Helvetica 18 bold')
        self.number.pack()
        # sets the text background colour to match the background, and set text colour to white
        self.number.config(bg="#5589ad", fg="white")

        # sets self.output equal to nothing (will be updated depending on user input)
        self.output = None

        self.outputlabel = tk.Label(self, text="")

    # creates a function called conjugate that processes the verb the user entered by running it through the API
    def conjugate(self):
        # automatically deletes all the output labels once the function is called to avoid duplication/stacking
        self.label.pack_forget()
        self.deflabel.pack_forget()
        self.tvmintro.pack_forget()
        self.tense.pack_forget()
        self.voice.pack_forget()
        self.mood.pack_forget()
        self.person.pack_forget()
        self.number.pack_forget()

        # sets a variable called user_word equal to the verb the user entered in the field
        user_word = self.entry.get()

        # sets a variable called defoutput equal to nothing
        defoutput = None

        # sets the variables tense, voice, mood, person, number equal to nothing
        tense = None
        voice = None
        mood = None
        person = None
        number = None

        # uses a regular expression to check if the user input contains the letter v, as it confuses the API
        if re.search('v', user_word):
            # if a v is detected, the program then tests to see if the last two letters of the user word are 're'
            if user_word.endswith('re'):
                # if the user word ends with 're', parse the word using the method below
                data = parser.parse_line(user_word)

                # checks to see if it is able to process the word - if it can't, move to except
                try:
                    # set the output variable equal to the principal parts of the verb the user entered
                    self.output = data[0]["defs"][0]["orth"][0] + ", " + data[0]["defs"][0]["orth"][1] + ", " + \
                                  data[0]["defs"][0]["orth"][2] + ", " + data[0]["defs"][0]["orth"][3]

                    # sets the variable definition equal to all the provided definitions of the verb the user entered
                    definition = data[0]["defs"][0]["senses"]

                    # uses a loop to add all definitions of the verb the user entered to a string
                    deflen = len(definition) - 1
                    orig_deflen = len(definition) - 2
                    defoutput = ""
                    for i in range(-1, deflen):
                        if i == int(orig_deflen):
                            # if the loop is on the final iteration, do not add an unnecessary comma to the end
                            defoutput = defoutput + data[0]["defs"][0]["senses"][deflen]
                        else:
                            # if there are more iterations to be completed, add a comma to separate the definitions
                            defoutput = defoutput + data[0]["defs"][0]["senses"][deflen] + ", "
                        deflen = deflen - 1

                    # set the variables for tense, voice, mood, person, number equal to values pulled from the JSON data
                    tense = data[0]["defs"][0]["infls"][0]["form"]["tense"]
                    voice = data[0]["defs"][0]["infls"][0]["form"]["voice"]
                    mood = data[0]["defs"][0]["infls"][0]["form"]["mood"]
                    person = str(data[0]["defs"][0]["infls"][0]["form"]["person"])
                    number = data[0]["defs"][0]["infls"][0]["form"]["number"]

                # if the verb cannot be processed, inform the user that their input was invalid
                except:
                    self.output = "Invalid input. Please try again."

            # if the verb does not end with 're', process the verb using the method below
            else:
                data = parser.parse_line(user_word)

                # checks to see if it is able to process the word - if it can't, move to except
                try:
                    # set the output variable equal to the principal parts of the verb the user entered
                    self.output = data[0]["defs"][0]["orth"][0] + ", " + data[0]["defs"][0]["orth"][1] + ", " + \
                                  data[0]["defs"][0]["orth"][2] + ", " + data[0]["defs"][0]["orth"][3]

                    # sets the variable definition equal to all the provided definitions of the verb the user entered
                    definition = data[0]["defs"][0]["senses"]

                    # uses a loop to add all definitions of the verb the user entered to a string
                    deflen = len(definition) - 1
                    orig_deflen = len(definition) - 2
                    defoutput = ""
                    for i in range(-1, deflen):
                        if i == int(orig_deflen):
                            # if the loop is on the final iteration, do not add an unnecessary comma to the end
                            defoutput = defoutput + data[0]["defs"][0]["senses"][deflen]
                        else:
                            # if there are more iterations to be completed, add a comma to separate the definitions
                            defoutput = defoutput + data[0]["defs"][0]["senses"][deflen] + ", "
                        deflen = deflen - 1

                    # set the variables for tense, voice, mood, person, number equal to values pulled from the JSON data
                    tense = data[0]["defs"][0]["infls"][0]["form"]["tense"]
                    voice = data[0]["defs"][0]["infls"][0]["form"]["voice"]
                    mood = data[0]["defs"][0]["infls"][0]["form"]["mood"]
                    person = str(data[0]["defs"][0]["infls"][0]["form"]["person"])
                    number = data[0]["defs"][0]["infls"][0]["form"]["number"]

                # if the verb cannot be processed, inform the user that their input was invalid
                except:
                    self.output = "Invalid input. Please try again."

        # if a v is not found in the word, process the word using the method below
        else:
            # request the JSON data from the API for the verb the user entered (user_word)
            r = requests.get('https://latinwordnet.exeter.ac.uk/lemmatize/' + user_word)
            r_data = r.json()

            # checks to see if it is able to process the word - if it can't, move to except
            try:
                # takes data from the API, sorts it, and parses it
                data1 = r_data[0]['lemma']['lemma']
                data2 = parser.parse_line(data1)

                # set the output variable equal to the principal parts of the verb the user entered
                self.output = data2[0]["defs"][0]["orth"][0] + ", " + data2[0]["defs"][0]["orth"][1] + ", " + \
                         data2[0]["defs"][0]["orth"][2] + ", " + data2[0]["defs"][0]["orth"][3]

                # sets the variable definition equal to all the provided definitions of the verb the user entered
                definition = data2[0]["defs"][0]["senses"]

                # uses a loop to add all definitions of the verb the user entered to a string
                deflen = len(definition) - 1
                orig_deflen = len(definition) - 2
                defoutput = ""
                for i in range(-1, deflen):
                    if i == int(orig_deflen):
                        # if the loop is on the final iteration, do not add an unnecessary comma to the end
                        defoutput = defoutput + data2[0]["defs"][0]["senses"][deflen]
                    else:
                        # if there are more iterations to be completed, add a comma to separate the definitions
                        defoutput = defoutput + data2[0]["defs"][0]["senses"][deflen] + ", "
                    deflen = deflen - 1

                data3 = parser.parse_line(user_word)

                # set the variables for tense, voice, mood, person, number equal to values pulled from the JSON data
                tense = data3[0]["defs"][0]["infls"][0]["form"]["tense"]
                voice = data3[0]["defs"][0]["infls"][0]["form"]["voice"]
                mood = data3[0]["defs"][0]["infls"][0]["form"]["mood"]
                person = str(data3[0]["defs"][0]["infls"][0]["form"]["person"])
                number = data3[0]["defs"][0]["infls"][0]["form"]["number"]

            # if the verb cannot be processed, inform the user that their input was invalid
            except:
                self.output = "Invalid input. Please try again."

        # updates the label that displays the principal parts of the verb (self.output)
        self.label = tk.Label(self, text="\nPrincipal Parts: " + self.output, font='Helvetica 18 bold')
        self.label.pack()
        # sets the text background colour to match the background, and set text colour to white
        self.label.config(bg="#5589ad", fg="white")

        # updates the label that displays the definitions of the verb (defoutput)
        self.deflabel = tk.Label(self, text="\nDefinitions: " + defoutput, font='Helvetica 18 bold')
        self.deflabel.pack()
        # sets the text background colour to match the background, and set text colour to white
        self.deflabel.config(bg="#5589ad", fg="white")

        # updates the label that displays the introduction to the tense, voice, mood, person, number section
        self.tvmintro = tk.Label(self, text="\nThe following are the tense, voice, mood, person, and number for the "
                                            "verb you entered.", font='Helvetica 18 bold')
        self.tvmintro.pack()
        # sets the text background colour to match the background, and set text colour to white
        self.tvmintro.config(bg="#5589ad", fg="white")

        # updates the label that displays the tense of the verb the user entered
        self.tense = tk.Label(self, text="\nTense: " + tense, font='Helvetica 18 bold')
        self.tense.pack()
        # sets the text background colour to match the background, and set text colour to white
        self.tense.config(bg="#5589ad", fg="white")

        pre_last = str(user_word)
        check_last = pre_last[-2:]

        # checks again to see if the last two letters of the user word are 're'
        if check_last == "re":
            # words ending with re are infinitives, and the voice, mood, person, and number should be updated
            # updates the label that displays the voice of the verb the user entered
            self.voice = tk.Label(self, text="Voice: active or passive", font='Helvetica 18 bold')
            self.voice.pack()
            # sets the text background colour to match the background, and set text colour to white
            self.voice.config(bg="#5589ad", fg="white")

            # updates the label that displays the mood of the verb the user entered
            self.mood = tk.Label(self, text="Mood: infinitive", font='Helvetica 18 bold')
            self.mood.pack()
            # sets the text background colour to match the background, and set text colour to white
            self.mood.config(bg="#5589ad", fg="white")

            # updates the label that displays the person of the verb the user entered
            self.person = tk.Label(self, text="Person (1st, 2nd, 3rd): N/A", font='Helvetica 18 bold')
            self.person.pack()
            # sets the text background colour to match the background, and set text colour to white
            self.person.config(bg="#5589ad", fg="white")

            # updates the label that displays the number of the verb the user entered
            self.number = tk.Label(self, text="Number (sg. or plr.): N/A", font='Helvetica 18 bold')
            self.number.pack()
            # sets the text background colour to match the background, and set text colour to white
            self.number.config(bg="#5589ad", fg="white")

        # if the last two letters of the word are not 're', do the following
        else:
            # updates the label that displays the voice of the verb the user entered
            self.voice = tk.Label(self, text="Voice: " + voice, font='Helvetica 18 bold')
            self.voice.pack()
            # sets the text background colour to match the background, and set text colour to white
            self.voice.config(bg="#5589ad", fg="white")

            # updates the label that displays the mood of the verb the user entered
            self.mood = tk.Label(self, text="Mood: " + mood, font='Helvetica 18 bold')
            self.mood.pack()
            # sets the text background colour to match the background, and set text colour to white
            self.mood.config(bg="#5589ad", fg="white")

            # updates the label that displays the person of the verb the user entered
            self.person = tk.Label(self, text="Person (1st, 2nd, 3rd): " + person, font='Helvetica 18 bold')
            self.person.pack()
            # sets the text background colour to match the background, and set text colour to white
            self.person.config(bg="#5589ad", fg="white")

            # updates the label that displays the number of the verb the user entered
            self.number = tk.Label(self, text="Number (sg. or plr.): " + number, font='Helvetica 18 bold')
            self.number.pack()
            # sets the text background colour to match the background, and set text colour to white
            self.number.config(bg="#5589ad", fg="white")

    # tkinter mainloop that runs the GUI
    def mainloop(self, n=0):
        tk.Tk.mainloop(self)
        # see lines 44 and 45 for explanation
        return self.string


# sets the class MyApp(), defined above, equal to the variable app
app = MyApp()
# sets the title of the GUI window to 'Latin Verb Tool'
app.title('Latin Verb Tool')
# sets the default size of the GUI window to 1000x600
app.geometry("1000x600")
# sets the default background colour of the GUI to the hex color
app.configure(background="#5589ad")
result = app.mainloop()
