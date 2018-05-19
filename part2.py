from types import *

class Item:
    #store all created items for a uniqueness check
    _item_store = []


    def __init__(self, name, price, uom):
        #Name cannot be NULL and must be a string
        assert type(name) is str, "Name is not a string: {}".format(name)
        assert len(name) > 0, "Name is NULL"
        #UOM cannot be NULL and must be a string
        assert type(uom) is str, "UOM is not a string: {}".format(uom)
        assert len(uom) > 0, "UOM is NULL"
        #Price should be greater than zero and must be a float
        assert type(price) is float, "Price is not a float: {}".format(price)
        assert price > 0, "Price is not greater than 0: {}".format(price)

        self.name = name
        self.price = price
        self.uom = uom

        #Check that the item does not already exist
        assert self not in Item._item_store, "Item already exists: {}".format(self)
        #If it exists, then the item will not be created
        Item._item_store.append(self)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{} - ${} - {}'.format(self.name, self.price, self.uom)

    def __eq__(self, other):
        return (self.name == other.name and self.price == other.price and self.uom == other.uom)

class Order:
    def __init__(self):
        self.items = []

    #Check that the object being passed in is an Item instance or list of Item instances and that the list is not empty
    def isValidItem(self,items):
        if isinstance(items, (list,)):
            assert len(items)>0, "Item is empty: {}.".format(items)
            for item in items:
                assert isinstance(item, Item), "Object in list not an Item: {}. Items will not be added.".format(item)
        else:
            assert isinstance(items, Item), "Object is not an Item: {}. Item will not be added.".format(items)

    #New add method was created. Can handle single item or list of items
    #A warning will be thrown if the oject is not an item
    def add(self, items):
        self.isValidItem(items)
        if isinstance(items, (list,)):
            for item in items:
                self.items.append(item)
        else:
            self.items.append(items)

    #Compute the cost of an order. Tax not included.
    def orderTotal(self):
        total = 0
        for item in self.items:
            if isinstance(item, MeatItem):
                total += item.price * item.weight
            else:
                total += item.price
        return total

    #Wanted to be able to see a friendly string representation of the Items in an order
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.items)

class MeatItem(Item):
    def __init__(self, name, price, weight, uom):
        #UOM for meat must be 'per lb' since MeatItem is sold by weight.
        assert uom.lower() == 'per lb', "UOM for meat items must be set to 'per lb': {}".format(uom)
        #New weight parameter must be float and greater than zero
        assert type(weight) is float, "Weight is not a float: {}".format(weight)
        assert weight > 0, "Weight is not greater than zero: {}".format(weight)

        #If assertions pass, then inherit the parent classes parameters and define weight
        #Weight goes first or else uniqueness breaks since it looks at MeatIteams repr methods which requires a weight
        self.weight = weight
        super(MeatItem, self).__init__(name, price, uom)


    #Created a new repr method to account for the addition of the Weight parameter in a Meat Item
    def __repr__(self):
        return '{} - ${} - {}lb(s) - {}'.format(self.name, self.price, self.weight, self.uom)


##############################################
#####################QC#######################
##############################################

p1 = Item('banana', 0.69, 'count')
print("Creating Item: {}".format(p1))

p2 = Item('milk', 2.29, 'carton')
print("Creating Item: {}".format(p2))

o1 = Order()
orderList = [p1, p2]
o1.add(orderList)
print("Currently in order: {}".format(o1))
print("Your total is: {}".format(o1.orderTotal()))

p3 = MeatItem('beef',5.00,2.00,'per lb')
print("Creating Item: {}".format(p3))

o1.add(p3)
print("Currently in order: {}".format(o1))
print("Your total is: {}".format(o1.orderTotal()))
