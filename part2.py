from types import *

class NotAnItemError(Exception):
    pass

class Item:
    global item_store
    item_store = []

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

        assert self not in item_store, "Item already exists: {}".format(self)
        item_store.append(self)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{} - ${} - {}'.format(self.name, self.price, self.uom)

    def __eq__(self, other):
        return (self.name == other.name and self.price == other.price and self.uom == other.uom)

class Order:
    def __init__(self):
        self.items = []

    # def add_item(self, item):
    #     if isinstance(item, Item):
    #         self.items.append(item)
    #
    # def add_items(self, items):
    #     for item in items:
    #         self.add_item(item)

    def add(self, items):
        if isinstance(items, (list,)):
            for item in items:
                self.items.append(item)
        elif isinstance(items, Item):
            self.items.append(items)
        else:
            raise NotAnItemError('Must be an Item')

    def orderTotal(self):
        total = 0
        for item in self.items:
            if item.uom.lower() == 'per lb':
                total += item.price * item.weight
            else: #need the else, or we end up totalling more times than we need too
                total += item.price
        return total

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.items)

p1 = Item('banana', 0.69, 'count')
print(p1)

p2 = Item('milk', 2.29, 'carton')
print(p2)

o1 = Order()

orderList = [p1, p2]
o1.add(orderList)

print(o1)


class MeatItem(Item):
    def __init__(self, name, price, weight, uom):
        super(MeatItem, self).__init__(name, price, uom)
        #UOM for meat must be 'per lb' otherwise Order Total calculations will be incorrect -- casing shouldn't matter
        assert uom.lower() == 'per lb', "UOM for meat items must be set to 'per lb': {}".format(uom)
        #New weight parameter must be float
        assert type(weight) is float, "Weight is not a float: {}".format(weight)
        assert weight > 0, "Weight is not greater than zero: {}".format(weight)
        self.weight = weight

    def __repr__(self):
        return '{} - ${} - {}lb(s) - {}'.format(self.name, self.price, self.weight, self.uom)
