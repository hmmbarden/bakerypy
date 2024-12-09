import random       # Random Discount
import time

import mysql.connector
connection = mysql.connector.connect(
    user="root",
    host="localhost",
    password="admin",
    database="shop",
    port="3306"
)


# Items in shop (dictionary):
shop = {"Chocolate Cake": 20, "Butterscotch Cream Cake": 20, "Sponge Cake": 30, "Salad": 40}
order = {}

def init_database():
    item_id = 1
    database_cursor = connection.cursor()
    database_cursor.execute("create table items(ID int, NAME varchar(255), PRICE int);")
    connection.commit()     # gotta do this because stack overflow said to
    for i in shop:
        query = f"insert into items (ID, NAME, PRICE) values ({item_id},'{i}',{shop[i]})"
        item_id += 1
        database_cursor.execute(query)
        connection.commit()

init_database()

menuActive = 1  # menuActive variable decides if the Menu is active/being used or not.
pageActive = 1  # pageActive variable decides if which Page is active/being used. 0 = null/no page

if menuActive == 0:
    print("menuActive variable is set to zero.")


def showmenu():
    # establish connection to database:
    database_cursor = connection.cursor()
    database_cursor.execute('select * from items;')
    data = database_cursor.fetchall()

    # display items in database:
    for item_data in data:
        item_info = f"ID: {str(item_data[0])}, \"{str(item_data[1])}\", ${str(item_data[2])}"
        print(item_info)


def add_item(item_name, cost):
    # establish connection to database.
    database_cursor = connection.cursor()
    database_cursor.execute('select ID from items;')
    total_items = len(database_cursor.fetchall())
    # QUERY TO ADD ITEM:
    database_cursor.execute(f'insert into items (ID, NAME, PRICE) values ({total_items+1},\'{item_name}\',{cost})')
    connection.commit()
    # send message for successful operation.
    print(f"New item '{item_name}' for the price of ${cost} was added successfully!")


def remove_item(item_id):
    # establish connection to database.
    database_cursor = connection.cursor()

    # get name of the item that was deleted.
    database_cursor.execute(f'select NAME from items where ID={item_id}')
    data = database_cursor.fetchall()
    name = data[0][0]
    # delete item from database
    database_cursor.execute(f'delete from items where ID={item_id}')
    connection.commit()

    # send message for successful
    print(f'Item \'{name}\' removed from the database!')


def place_order(item_name, quantity):
    # establish database connection.
    database_cursor = connection.cursor()
    database_cursor.execute(f'select * from items where NAME=\'{item_name}\'')
    data = database_cursor.fetchall()
    item_id = int(data[0][0])
    item_price = int(data[0][2])
    quantity = int(quantity)

    # if similar order already exists, add quantity:
    if item_name in order.keys():
        # add to existing quantity:
        quantity = int(order[item_name]['quantity']) + quantity
        price = 0
        # recalculate price:
        price = quantity * item_price
        order[item_name]['item_id'] = item_id
        order[item_name]['single_item_price'] = item_price
        order[item_name]['total_price'] = price
        order[item_name]['quantity'] = quantity
    else:
        price = quantity * item_price
        # order = {'Item Name':{'quantity':10,'total_price':price}}
        order[item_name] = {'quantity': quantity, 'total_price': price}
        order[item_name]['item_id'] = item_id
        order[item_name]['single_item_price'] = item_price

    # Message sent if item is successfully added in shopping cart.
    message = "Added " + str(quantity) + " " + item_name + " to shopping cart."
    print(message)


def remove_from_order(item_name, new_quantity):
    new_quantity = int(new_quantity)
    # remove completely:
    if new_quantity == int(order[item_name]['quantity']):
        order.pop(item_name)
    # reduce quantity:
    elif new_quantity < int(order[item_name]['quantity']):
        order[item_name]['quantity'] -= new_quantity
    # send warning:
    elif new_quantity > int(order[item_name]['quantity']):
        print("You cannot remove more than the number of items you have put in your cart!")

    # Message sent if item was removed from cart.
    message = str(quantity) + "x " + item_name + " was/were removed from the shopping cart."
    print(message)


def change_cost(item_id, cost):
    database_cursor = connection.cursor()
    database_cursor.execute(f'update items set PRICE={cost} where ID={item_id}')
    connection.commit()
    database_cursor.execute(f'select * from items where ID={item_id}')
    data = database_cursor.fetchall()
    print(f'Price of item \'{data[0][1]}\' has been set to ${cost}')


def create_bill():
    # order variable is the dictionary "order"
    bill = open('bill.txt',"w")
    bill.write("-------------[BAKERY BILL]------------\n\nFollowing are the details of bill generated.\n\n")
    item_count = 0
    for item in order:
        item_count += 1
        bill.write(f"[{item_count}] {order[item]['quantity']}x {item}   -    ${order[item]['total_price']}  |   ${order[item]['single_item_price']} x {order[item]['quantity']}\n")
    bill.write('------------------------------------------\n\n')
    bill.write(f"Total Amount      -     {old_total}\n")
    bill.write(f"After Discount ({discount}%)    -     {total}")
    bill.close()
    print('Your Bill has been printed successfully.')


while(menuActive > 0):
    if pageActive == 1:
        # main menu text.
        # Main Menu = 1, Shop = 2, Cart = 3, Checkout = 4, Exit = 5, 6 = Admin Panel
        main_menu = "\n Type 'shop' to view shop.\n Type 'cart' to view items in your cart. \n Type 'checkout' to place an order.\n Type 'exit' to exit the menu. \n Type 'admin' for admin access. \n\n Input: "
        print("------------[ BAKERY ]------------\n\nWelcome to the Bakery!")
        # navigation:
        response = input(main_menu)

        if response == "shop":
            pageActive = 2
            # If user chooses to visit SHOP:
            # show all items in shop.
        elif response == "cart":
            # if user chooses to view cart
            pageActive = 3
        elif response == "checkout":
            # if user chooses to checkout
            pageActive = 4
        elif response == "exit":
            # if user chooses to checkout
            pageActive = 5
        elif response == "admin":
            # if user chooses to checkout
            pageActive = 6
        
    elif pageActive == 2:
        # USER IS CHECKING SHOP:
        # show all items in shop.
        print("------------[ Menu ]------------")
        showmenu()
        print("\n")

        new_response = input("Type: \n'return' => return to main menu.\n'order <item_id> <quantity>': place an order for an item.\n'cart': check your shopping cart\n Input: ")
        new_response = new_response = new_response.split(" ") # split by words
        print(new_response)
        if new_response[0] == "return":
            pageActive = 1
        elif new_response[0] == "cart":
            pageActive = 3
        elif new_response[0] == "order":
            # establish database conenction
            database_cursor = connection.cursor()
            bool_1 = new_response[1].isnumeric
            bool_2 = new_response[2].isnumeric
            if bool_1 and bool_2:
                provided_id  = int(new_response[1])
                database_cursor.execute(f'select * from items where ID={provided_id}')
                data = database_cursor.fetchall()
                item_name = data[0][1]
                quantity = new_response[2]
                place_order(item_name, quantity)
        else:
            print(new_response)

    elif pageActive == 3:
        # USER IS CHECKING THEIR SHOPPING CART:
        if len(order) == 0:
            print("There are no items in the shopping cart! Visit the 'shop' to add items. Returning to Menu.")
            pageActive = 1
        else:
            print("\n------------[ SHOPPING CART ]------------\n")
            total = 0
            for item in order:
                bill_item_format = "ID: " + str(order[item_name]['item_id']) + ", " + item + " : $" + str(order[item]['single_item_price']) + " * " + str(order[item]['quantity']) + " = $" + str(order[item]['total_price'])
                total += int(order[item]['total_price'])
                print(bill_item_format)
            
            print(f"Total Bill: ${total}. Discount applied while checkout.")
            print("\n------------[ SHOPPING CART ]------------\n")

            new_response = input("Type: \n'return' => return to main menu.\n'shop': check the shop.\n 'remove <item_id> <quantity>': remove an item from cart. \n'checkout': proceed to checkout\n Input: ")
            new_response = new_response.split(" ") # split by words
            
            if new_response[0] == "return":
                pageActive = 1
            elif new_response[0] == "shop":
                pageActive = 2
            elif new_response[0] == "remove":
                item_id = int(new_response[1])
                new_quantity = int(new_response[2])
                item_name = list(shop)[item_id]
                remove_from_order(item_name, new_quantity)
                # refresh the Menu:
                pageActive = 0
                pageActive = 3
            elif new_response[0] == "checkout":
                pageActive = 4

    elif pageActive == 4:
        if len(order) == 0:
            print("There are no items in the shopping cart! Visit the 'shop' to add items. Returning to Menu.")
            pageActive = 1
        else:
            print("\n-----------------[ CHECKOUT ]-----------------")
            # USER IS CHECKING OUT:
            # print the order:
            item_count = 0
            total = 0
            for item in order:
                item_count += 1
                # [1] 10x Strawberry Cake for $200, ($20 each)
                order_item_details = "[" + str(item_count) + "] " + str(order[item]['quantity']) + "x " + item + " for $" + str(order[item]['total_price']) + " ($" + str(order[item]['single_item_price']) + " each, " + "ID: " + str(order[item_name]['item_id']) + ")"
                print(order_item_details)
                total += int(order[item]['total_price'])
            
            # apply some kind of discount:
            old_total = total
            discount = random.randint(1, 15)
            total -= (discount/100) * total 

            print("------------------------------------------------")
            # send final message:
            total_bill_message = "Your bill was $" + str(old_total) + ". New total, after " + str(discount) + "% discount is $" + str(total) + ". Type 'ok' to proceed, 'cancel' to opt out. \n Type 'cart' to view cart and make changes. \n Input: "
            new_response = input(total_bill_message)
            if new_response == 'ok':
                print("Payment being processed..")
                time.sleep(1)
                print("Generating bill..")
                time.sleep(3)
                create_bill()
                print("Thank you for purchasing! Do come again!")
                time.sleep(5)
                pageActive = 1
            if new_response == 'cancel':
                print("Opting out of Checkout Menu. Entering Main Menu...")
                pageActive = 1
            if new_response == 'cart':
                pageActive = 3

    elif pageActive == 5:
        # USER HAS EXITED THE MENU:
        # print goodbye message
        print('Emptying the shopping cart...')
        print('Exiting the application. Thank you, Visit again!')
        # shut down the menu:
        menuActive = 0
    
    elif pageActive == 6:
        print("\n------------[ ADMIN PANEL / AUTHORISED PERSONNEL ONLY ]------------\n")
        new_response = input("Welcome, admin. Type 'password <password>' to login. Type 'return' to return to main menu.\n\n Input: ")
        new_response = new_response.split(" ")
        if new_response[0] == "password":
            if new_response[1] == "123":
                print("Login successful.")
                pageActive = 7
            else:
                print("Wrong password!")
        elif new_response[0] == "return":
            pageActive = 1


    elif pageActive == 7:
        showmenu()
        menu = "\n Type 'add <item_name> <cost_per_unit>' to add an item (To add 'Vanilla Ice Cream', write it as 'Vanilla-Ice-Cream')." + "\n Type 'delete <item_id>' to delete an item. \n Type 'new_cost <item_id> <cost>' to change cost of item. \n Type 'return' to return to the main menu\n\nInput: "
        response = input(menu)
        response = response.split(" ")
        if response[0] == "add":
            name = " ".join(response[1].split('-'))
            cost = int(response[2])   
            add_item(name, cost)
        elif response[0] == "delete":
            item_id = int(response[1])
            remove_item(item_id)
        elif response[0] == "new_cost":
            # change the cost
            id = int(response[1])
            cost = int(response[2])
            change_cost(id, cost)
        elif response[0] == "return":
            pageActive = 1
            print(pageActive)
        else:
            print("Wrong input. Please try again!")
