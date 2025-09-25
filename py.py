import tkinter as tk
from tkinter import ttk, messagebox



class MenuItem:
    def __init__(self, name, ingredients, price, available=True):
        self.name = name
        self.ingredients = ingredients
        self.price = price
        self.available = available

    def __str__(self):
        return f"{self.name} - Rupees{self.price:.2f}"


class FoodItem(MenuItem):
    def __init__(self, name, ingredients, price, is_vegetarian, available=True):
        super().__init__(name, ingredients, price, available)
        self.is_vegetarian = is_vegetarian

    def __str__(self):
        return f"{super().__str__()} - {'Vegetarian' if self.is_vegetarian else 'Non-Vegetarian'}"


class BeverageItem(MenuItem):
    def __init__(self, name, ingredients, price, is_hot, available=True):
        super().__init__(name, ingredients, price, available)
        self.is_hot = is_hot

    def __str__(self):
        return f"{super().__str__()} - {'Hot' if self.is_hot else 'Cold'}"


class RestaurantMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Menu System")

        self.menu_items = [
            FoodItem("Chole Bhature", ["White Flour", "Chole", "Curd"], 200, False),
            FoodItem("Rajma Chawal", ["Rajma", "Chawal", ], 150, True),
            BeverageItem("Iced Coffee", ["Coffee", "Ice", "Milk", "Sugar"], 110, False),
            BeverageItem("Green Tea", ["Green Tea Leaves", "Hot Water", "Honey"], 120, True)
        ]

        self.order_items = []

        # Create and set up the tabs
        self.tabControl = ttk.Notebook(root)
        self.menuTab = ttk.Frame(self.tabControl)
        self.orderTab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.menuTab, text='Menu')
        self.tabControl.add(self.orderTab, text='Order')

        self.tabControl.pack(expand=1, fill="both")

        # Call methods to set up UI for each tab
        self.setup_menu_tab()
        self.setup_order_tab()

    def setup_menu_tab(self):
        # Treeview to display the menu
        self.menu_tree = ttk.Treeview(self.menuTab, columns=("Name", "Price"), show="headings")
        self.menu_tree.heading("Name", text="Name")
        self.menu_tree.heading("Price", text="Price (Rupees)")
        self.menu_tree.grid(column=0, row=0, padx=10, pady=10)

        # Populate the menu Treeview
        for item in self.menu_items:
            self.menu_tree.insert("", "end", values=(item.name, item.price))

        # Button to add selected item to the order
        add_to_order_button = ttk.Button(self.menuTab, text="Add to Order", command=self.add_to_order)
        add_to_order_button.grid(column=0, row=1, padx=10, pady=10)

    def setup_order_tab(self):
        # Treeview to display the order
        self.order_tree = ttk.Treeview(self.orderTab, columns=("Name", "Price"), show="headings")
        self.order_tree.heading("Name", text="Name")
        self.order_tree.heading("Price", text="Price (Rupees)")
        self.order_tree.grid(column=0, row=0, padx=10, pady=10)

        # Button to place the order
        place_order_button = ttk.Button(self.orderTab, text="Place Order", command=self.place_order)
        place_order_button.grid(column=0, row=1, padx=10, pady=10)

    def add_to_order(self):
        # Get the selected item from the menu Treeview
        selected_item = self.menu_tree.selection()

        if selected_item:
            item_index = int(selected_item[0][1:]) - 1
            menu_item = self.menu_items[item_index]

            # Check if the item is available
            if menu_item.available:
                # Add the item to the order
                self.order_items.append(menu_item)

                # Update the order Treeview
                self.update_order_tree()

                messagebox.showinfo("Item Added", f"{menu_item.name} added to the order.")
            else:
                messagebox.showwarning("Item Unavailable", f"{menu_item.name} is not available.")
        else:
            messagebox.showwarning("No Item Selected", "Please select an item from the menu.")

    def update_order_tree(self):
        # Clear existing items in the order Treeview
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)

        # Add items to the order Treeview
        total_price = 0
        for item in self.order_items:
            self.order_tree.insert("", "end", values=(item.name, item.price))
            total_price += item.price

        # Update total price label
        total_price_label = ttk.Label(self.orderTab, text=f"Total Price: Rupees{total_price:.2f}")
        total_price_label.grid(column=0, row=2, padx=10, pady=10)

    def place_order(self):
        # Check if the order is not empty
        if not self.order_items:
            messagebox.showwarning("Empty Order", "Please add items to the order.")
            return

        # Mark items as unavailable in the menu
        for item in self.order_items:
            item.available = False

        # Show confirmation message
        messagebox.showinfo("Order Placed", "Order placed successfully.")

        # Clear the order
        self.order_items = []

        # Update the order Treeview
        self.update_order_tree()


if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantMenuApp(root)
    root.mainloop()
