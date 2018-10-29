# Project Inventory Manager

# Have products that can be added, sold etc

import os

class Product:
    def __init__(self, ID, quantity, price):
        self.price = price
        self.id = ID
        self.quantity = quantity

    def get_ID(self):
        return(self.id)

    def get_quantity(self):
        return(self.quantity)

    def get_price(self):
        return(self.price)

class Inventory:
    def __init__(self):
        self.budget = 0
        self.products = []
        self.IDs = {}
        self.import_inv()
    
    def import_inv(self):
        try:
            f = open("History","r")
        except:
            return("")
        lines = f.readlines()
        if lines != []:
            for line in lines[2:]:
                line = line.split()
                product = Product(line[0], line[1], line[2])
                self.products.append(product)
                self.IDs[line[0].capitalize()] = product
        f.close()

    def write_inv(self):
        inventory = self.get_inventory()
        if len(inventory.split("\n")) > 1:
            f = open("History", "w")
            f.write(inventory)
            f.close()
        else:
            open("History", "w").close()


    def add_items(self, ID, quantity, price):
        if ID.capitalize() not in self.IDs:
            product = Product(ID, quantity, price)
            self.products.append(product)
            self.IDs[ID.capitalize()] = product
            self.write_inv()
        else:
            print("Ce produit est déjà dans votre inventaire")
        self.get_inventory()

    def del_items(self, name_product):
        if name_product.capitalize() in self.IDs:
            self.products.remove(self.IDs[name_product])
            del(self.IDs[name_product.capitalize()])
            self.write_inv()
        else:
            print("Vous n'avez pas ce produit dans votre inventaire")
        self.get_inventory()

    def sell_items(self, name_product, nbSold):
        if name_product.capitalize() in self.IDs:
            self.IDs[name_product.capitalize()].quantity -= nbSold
            self.write_inv()
        else:
            print("Vous n'avez pas ce produit dans votre inventaire")
        self.get_inventory()

    def get_inventory(self):
        if self.products == []:
            return("The inventory is empty")
        else:
            res = "Product\tQuantity (in Kg)\tPrice (in €)\n\n"
            for p in self.products:
                res += "{}\t{}\t{}\n".format(p.get_ID(), p.get_quantity(), p.get_price())
        return(res)

if __name__ == "__main__":
    inv = Inventory()
    # inv.add_items("Banana", 1, 1)
    # inv.add_items("Noisette", 2, 4)
    inv.import_inv()
    print(inv.get_inventory())