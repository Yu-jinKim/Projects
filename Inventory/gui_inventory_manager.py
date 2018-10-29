import tkinter as tk
import inventory_manager

# Create the app with the switching function (copied from internet)
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Manager)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

# Class for every frame: here the home frame
class Manager(tk.Frame):
    def __init__(self, master):

        tk.Frame.__init__(self, master, height = 1000, width = 2000)

        inventory_label = inv.get_inventory()
        tk.Label(self, text = "\n{}\n".format(inventory_label)).grid(columnspan = 3, padx = 5, pady = 5)

        add = tk.Button(self, text="Add product",
                        command=lambda: master.switch_frame(Add_Product))
        add.grid(row = 1, column = 0, padx = 5, pady = 5)

        delete = tk.Button(self, text="Delete product",
                        command=lambda: master.switch_frame(Del_Product))
        delete.grid(row = 1, column = 1, padx = 5, pady = 5)

# Add product frame
class Add_Product(tk.Frame, App):
    def __init__(self, master):
        self.entries = []

        tk.Frame.__init__(self, master)

        # Every entry and label to have the information necessary of the produce
        tk.Label(self, text = "Name of the product", anchor = "w").grid(row = 1, column = 0, padx = 5, pady = 5)
        e1 = tk.Entry(self)
        e1.grid(row = 1, column = 1, padx = 5, pady = 5)
        self.entries.append(e1)

        tk.Label(self, text = "Quantity to be added (in kg)", anchor = "w").grid(row = 2, column = 0, padx = 5, pady = 5)
        e2 = tk.Entry(self)
        e2.grid(row = 2, column = 1, padx = 5, pady = 5)
        self.entries.append(e2)

        tk.Label(self, text = "Price (€) per kg", anchor = "w").grid(row = 3, column = 0, padx = 5, pady = 5)
        e3 = tk.Entry(self)
        e3.grid(row = 3, column = 1, padx = 5, pady = 5)
        self.entries.append(e3)

        tk.Button(self, text="Add product",
                  command=lambda:[self.add(), master.switch_frame(Manager)]).grid(row = 4, column = 0, pady = 5)
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(Manager)).grid(row = 4, column = 1, pady = 5)

    # Call the inventory function to add items
    def add(self):
        inv.add_items(self.entries[0].get(), self.entries[1].get(), self.entries[2].get())
        inv.write_inv()

# deletion frame
class Del_Product(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        options = list(inv.IDs.keys())
        v = tk.StringVar()
        v.set(options[0])

        tk.OptionMenu(self, v, *options).pack()

        tk.Button(self, text="Delete product",
                  command=lambda: [self.delete(v.get()), master.switch_frame(Manager)]).pack()
        tk.Button(self, text="Back",
                  command=lambda: master.switch_frame(Manager)).pack()

    # call the inventory function to delete produce
    def delete(self, product):
        inv.del_items(product)
        inv.write_inv()


if __name__ == "__main__":
    inv = inventory_manager.Inventory()
    app = App()
    app.mainloop()