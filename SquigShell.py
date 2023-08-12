import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.scrolledtext as scrolledtext
import keyword
import tokenize
from io import BytesIO

# Black theme colors
BG_COLOR = "#000000"
FG_COLOR = "#FFFFFF"
LINE_NUMBER_COLOR = "#666666"
PROMPT_COLOR = "#00FF00"
OUTPUT_COLOR = "#00FFFF"
ERROR_COLOR = "#FF0000"
KEYWORD_COLOR = "#FF00FF"

class ShellApp:
    def __init__(self, master):
        self.master = master
        master.title("MyShell")
        master.configure(bg=BG_COLOR)

        self.menu_bar = tk.Menu(master, bg=BG_COLOR, fg=FG_COLOR, activebackground=BG_COLOR, activeforeground=FG_COLOR)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, bg=BG_COLOR, fg=FG_COLOR, activebackground=BG_COLOR,
                                 activeforeground=FG_COLOR)
        self.file_menu.add_command(label="New File", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        master.config(menu=self.menu_bar)

        self.input_text = scrolledtext.ScrolledText(master, height=10, bg=BG_COLOR, fg=FG_COLOR,
                                                    insertbackground=FG_COLOR, font=("Courier New", 12))
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.line_number_bar = tk.Text(master, width=4, bg=BG_COLOR, fg=LINE_NUMBER_COLOR, bd=0, font=("Courier New", 12))
        self.line_number_bar.pack(side=tk.LEFT, fill=tk.Y)

        self.input_text["yscrollcommand"] = self.on_scroll
        self.line_number_bar["yscrollcommand"] = self.on_scroll

        self.scrollbar = tk.Scrollbar(master, bg=BG_COLOR, troughcolor=FG_COLOR, width=12)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_frame = tk.Frame(master, bg=BG_COLOR)
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(self.output_frame, height=10, bg=BG_COLOR, fg=FG_COLOR,
                                                     state=tk.DISABLED, font=("Courier New", 12))
        self.output_text.pack(fill=tk.BOTH, expand=True)

        self.run_button = tk.Button(master, text="Run", command=self.execute_command, bg=BG_COLOR, fg=FG_COLOR,
                                    activebackground=BG_COLOR, activeforeground=FG_COLOR, font=("Courier New", 12))
        self.run_button.pack(pady=10)

        self.prompt = PROMPT_COLOR + ">>> " + FG_COLOR
        self.output_visible = False

    def new_file(self):
        self.input_text.delete("1.0", tk.END)
        self.line_number_bar.delete("1.0", tk.END)
        self.clear_output()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, content)
                self.update_line_numbers()

    def save_file(self):
        content = self.input_text.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)

    def execute_command(self):
        command = self.input_text.get("1.0", tk.END).strip()
        self.display_output(self.prompt + command, "input")
        self.input_text.delete("1.0", tk.END)

        if command == "exit()":
            self.master.destroy()
            return

        try:
            output = eval(command)
            if output is not None:
                self.display_output(repr(output), "output")
                self.show_output()
        except Exception as e:
            self.display_output("Error: " + str(e), "error")
            self.show_output()

    def display_output(self, output, output_type):
        self.output_text.config(state=tk.NORMAL)
        if output_type == "input":
            self.output_text.insert(tk.END, output + "\n", "prompt")
        elif output_type == "output":
            self.output_text.insert(tk.END, output + "\n", "output")
        elif output_type == "error":
            self.output_text.insert(tk.END, output + "\n", "error")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)

    def show_output(self):
        if not self.output_visible:
            self.output_visible = True
            self.output_frame.pack(fill=tk.BOTH, expand=True)

    def on_scroll(self, *args):
        self.input_text.yview(*args)
        self.line_number_bar.yview(*args)

    def update_line_numbers(self):
        line_count = self.input_text.get("1.0", tk.END).count("\n")
        line_numbers = "\n".join(str(i) for i in range(1, line_count + 2))
        self.line_number_bar.config(state=tk.NORMAL)
        self.line_number_bar.delete("1.0", tk.END)
        self.line_number_bar.insert(tk.END, line_numbers)
        self.line_number_bar.config(state=tk.DISABLED)

root = tk.Tk()
app = ShellApp(root)

# Configure dark theme colors
style = tk.ttk.Style()
style.configure(".", background=BG_COLOR, foreground=FG_COLOR)
style.configure("TEntry", fieldbackground=BG_COLOR, foreground=FG_COLOR)
style.configure("TScrollbar", background=BG_COLOR, troughcolor=FG_COLOR, gripcount=0, width=12)
style.configure("TText", background=BG_COLOR, foreground=FG_COLOR, insertbackground=FG_COLOR)
style.configure("TButton", background=BG_COLOR, foreground=FG_COLOR, activebackground=BG_COLOR, activeforeground=FG_COLOR)
style.configure("TMenu", background=BG_COLOR, foreground=FG_COLOR, activebackground=BG_COLOR, activeforeground=FG_COLOR)

# Configure tags for styling
app.output_text.tag_configure("prompt", foreground=PROMPT_COLOR)
app.output_text.tag_configure("output", foreground=OUTPUT_COLOR)
app.output_text.tag_configure("error", foreground=ERROR_COLOR)

# Bind the highlight_keywords method to KeyRelease event
app.input_text.bind("<KeyRelease>", app.highlight_keywords)

root.mainloop()
