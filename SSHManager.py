import tkinter as tk
from tkinter import ttk

class ConsoleText(tk.Text):

    def __init__(self, master=None, **kw):
        tk.Text.__init__(self, master, **kw)
        self.insert('1.0', '>>> ') # first prompt
        # create input mark
        self.mark_set('input', 'insert')
        self.mark_gravity('input', 'left')
        # create proxy
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        # binding to Enter key
        self.bind("<Return>", self.enter)


    def _proxy(self, *args):
        largs = list(args)

        if args[0] == 'insert':
            if self.compare('insert', '<', 'input'):
                # move insertion cursor to the editable part
                self.mark_set('insert', 'end')  # you can change 'end' with 'input'
        elif args[0] == "delete":
            if self.compare(largs[1], '<', 'input'):
                if len(largs) == 2:
                    return # don't delete anything
                largs[1] = 'input'  # move deletion start at 'input'
        result = self.tk.call((self._orig,) + tuple(largs))
        return result

    def enter(self, event):
        command = self.get('input', 'end')
        # execute code
        print(command)
        # display result and next promp
        self.insert('end', '\nCommand result\n\n>>> ')
        # move input mark
        self.mark_set('input', 'insert')
        return "break" # don't execute class method that inserts a newline

class Mainapp:
    def __init__(self, master):
        self.master = master
        master.title("Tabbed window")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.add_button = tk.Button(master, text="Add Tab", command=self.add_tab)
        self.add_button.pack(side=tk.BOTTOM)
        self.add_tab()
    def add_tab(self):
        # Create a new frame to hold the content of the tab
        new_frame = tk.Frame(self.notebook)
        
        # Add some content to the frame
        label = tk.Label(new_frame)
        label.pack(padx=10, pady=10)
        
        # Add the new frame to the notebook as a new tab
        self.notebook.add(new_frame, text="New Tab")
        
root = tk.Tk()
root.geometry("800x650")
app = Mainapp(root)
# tfield = ConsoleText(root, bg='black', fg='white', insertbackground='white')
# tfield.pack()
root.mainloop()