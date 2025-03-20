#! python3

import pprint


def displayInventory(inventory):
    print("Inventory:")
    item_total = 0
    for k, v in inventory.items():
        item_total+=v
        print(str(v) + ' ' + str(k))
    print("Total number of items: " + str(item_total))


def addToInventory(inventory, add_items):
    for item in add_items:
        if item in inventory:
            inventory[item] += 1
        else:
            inventory[item] = 1
    return inventory

inv = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}
dragonLoot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
inv = addToInventory(inv, dragonLoot)
displayInventory(inv)