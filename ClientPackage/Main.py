import tkinter as tk

class ChatApp:

    def __init__(self, master):
        self.master = master
        master.title("Chat App")

        self.message_listbox = tk.Listbox(master, width=50, height=10)
        self.message_listbox.pack()

        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack()

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack()

    def send_message(self):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        self.message_listbox.insert(tk.END, message)

root = tk.Tk()
app = ChatApp(root)
root.mainloop()
