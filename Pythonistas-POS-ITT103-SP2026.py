# Import pandas library for data handling
import pandas as pd
#Stores the name of the csv file that contains the product inventory data
File_Name = 'Product_Inventory.csv'
# Create product catalog as a dictionary
Catalog = {'Product_Name' : ['Keyboard', 'Mouse', 'Mouse Pad', 'Speakers', 'Laptop', 'Ipad', 'Flash Drive', 'Headphone', 'Type C Cable', 'Adapter'],
            'Quantity': [10,5,10,5,6,10,15,5,20,25],
            'Price': [2000,1500,1000,3500,70000,62000,1500,2500,2000,2000]
            }
 # Convert dictionary into a pandas DataFrame           
df = pd.DataFrame(Catalog)
#Saves the DataFrame to the csv file created 
df.to_csv('Product_Inventory.csv')
# Dictionary to store items added to cart
Cart = {}

def Store_Inventory():
#Saves the DataFrame to the csv file without the row number
  df.to_csv('Product_Inventory.csv', index = False)
# Function to display menu of products
def show_menu():
  print('** Best Buy Retail Store **')
  # Loop through all products
  for i in range(len(df)):
      # Display product number, name, price and stock
    print(f"{i+1}. {df.loc[i, 'Product_Name']} - Price: ${df.loc[i, 'Price']} - Stock: {df.loc[i, 'Quantity']}")

def Find_Product ( user_input):
  user_input = user_input.strip()
  
  if user_input.isdigit():
     Product_Number = int(user_input)
     #Validates if the number is within the product list range
     if 1<= Product_Number <= len(df):
         #Converts to index
       index = Product_Number-1
       #Returns the index and product name
       return index, df.loc[index, 'Product_Name']
  else:
      #If input is not a number, search for the product name 
    for index, row in df.iterrows(): # Loop through all product in the DataFrame
    #Compare names (Ignores spaces and case differences)
      if row['Product_Name'].strip().lower()==user_input.lower():
        #Returns index and matched product name
        return index, row['Product_Name']
  #If product is not found, return None values   
  return None, None
  
# Function to check stock availability
def stock_availability(Product_Name, requested_quantity):
    #Gets the index and correct product name from the users input
  index, Product_Name = Find_Product(Product_Name)
  #If product was not found
  if index is None:
      #Return failure with message
    return False, None, Product_Name, 'Product not found'
  #Get current stock from Dataframe using the index
  current_stock = int(df.loc[index, 'Quantity']) #Access the 'Quantity column for that product'
  #Check if enough stock is available
  if current_stock >= requested_quantity:
      #Enough stock 
        return True, index, Product_Name, f'In stock: {current_stock} units available'
  else:
        #Not enough stock
        return False, index, Product_Name, f'Out of stock: Only {current_stock} units available'
        
#Function to add item to cart
def add_item():
    # Get product name or number from user
  Product_Name = input('Enter item name or number: ').strip().lower()
#Try to get the quantity from the user
  try:
      #Converts the users input to an integer
    Quantity = int(input(f' Enter quantity for {Product_Name}: '))
  #If the user enters something that is not a number
  except ValueError:
    print('Invalid quantity.')#Show error message
    return #Exit the function
  #Checks if the product exist and if there is enough stock
  available,index, Product_Name, message = stock_availability(Product_Name, Quantity)
  #Display stock message ('In stock' or 'Out of stock')
  print(message)
  #If the item is available in sufficent quantity
  if available:
      #Reduce the stock in the Dataframe
      df.at[index, 'Quantity'] -= Quantity
      #Add item to the cart or update quantity if already in the cart
      Cart[Product_Name] = Cart.get(Product_Name, 0)+ Quantity
      #Confirms item added to the cart
      print(f'{Quantity} x {Product_Name} to Cart.')
# Function to view items in cart       
def view_cart():
  print('* My Cart *')
  if not Cart: # Check if cart is empty
    print('My cart is empty') #Informs the user
    return #Exits the function
  
  print ('***My Cart***')
  for Product_Name, Quantity in Cart.items():# Loop through cart items
    #Loops through the DataFrame to find matching product details
    for index, row in df.iterrows():
        #Matches product name
      if row['Product_Name'].strip().lower() == Product_Name.strip().lower():
       #Gets the price of the product
        price = row ['Price']
        #Calculate total cost for the item
        Line_Total = price * Quantity
        #Display item details in the cart
        print(f'{Product_Name} x {Quantity} = ${Line_Total:.2f}')
        break #Stops searching once the product is found
#Function to remove item from cart     
def remove_item():
  print('* My Cart *')
  #Check if the cart is empty
  if not Cart:
    print('My cart is empty') #Informs the user
    return #Exits function
  #Ask the user to enter product name or name
  Product_Input = input('Enter item number or item name to remove:').strip()
  #Finds the product in the inventory
  index,Product_Name = Find_Product(Product_Input)
    #If the product was not found
  if Product_Name is None:
    print ('Product not found')
    return
  #Check if the product is in the cart
  if Product_Name not in Cart:
    print(f'{Product_Name} is not in the cart.')
    return
  #Ask the user how many items they want to remove
  try:
    quantity = int(input(f'Enter quantity to remove from {Product_Name}:'))
 #Handle invalid input (non-numeric)
  except ValueError: 
    print('Invalid Entry')
    return
 #Ensure quantity is greater than 0   
  if quantity <= 0:
    print('Quantity must be greater than 0.')
    return
#Check if the user is trying to remove more than they have 
  if quantity > Cart[Product_Name]:
    print(f'You have {Cart[Product_Name]} x {Product_Name} in the cart')
    return
#Reduce quantity in the cart
  Cart[Product_Name] -= quantity
  #Return removed item back to the inventory
  df.at[index, 'Quantity'] += quantity
  #If quantity becomes '0' remove item entirely from the cart
  if Cart [Product_Name] == 0:
    del Cart[Product_Name]
    #Saves and update inventory
  Store_Inventory()
  #Confirms removed item(s)
  print(f'{quantity} x {Product_Name} removed from cart and returned to inventory.')

# Function to calculate total cost
def Calculate_Total():
  subtotal = 0 # Initialize subtotal

# Loop through cart items
  for Product_Name, Quantity in Cart.items():
    for index, row in df.iterrows(): #Loops through the DataFrame
        # Match product name
      if row ['Product_Name'].strip().lower() == Product_Name.strip().lower():
        subtotal += row ['Price']*Quantity  # Add item total to subtotal
        break #Stop searching once the product is found
    
  tax = subtotal * 0.10 # Calculate 10% tax
  total = subtotal + tax # Add tax to subtotal
  
  discount = 0 # Initialize discount
  if total >= 5000: # Apply discount if total is above threshold
    discount = total *0.05 #Calculate discount
    total -= discount #Subtract discount from total
    #Display discount applied
    print(f'5% discount: -${discount: .2f}')
    #Return all calculated valves
  return subtotal,tax,discount,total

def Print_receipt(Cart, subtotal, tax, discount, total, Amount_Paid, Change):
    print("\nReceipt:")
    print("Best Buy Retail Store")
    print("--------------------")
    #Loop through each item in the cart 
    for Product_Name, Quantity in Cart.items():
        #Loops through the DataFrame to find product 
      for index, row in df.iterrows():
          #Matches product name
        if row['Product_Name'].strip().lower() == Product_Name.strip().lower():
          #Gets price of the product
          Price = row ['Price']
          #Calculate total cost for the item
          line_total = Price * Quantity
          #Print item detail on receipt
          #.2f Formats number to 2 decimal place
          print(f"{Product_Name} x {Quantity} -${line_total: .2f}")
          break #Stop searching once product is found
    #Prints summary of cost  
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Tax (10%): ${tax:.2f}")
    print(f'Discount: -${discount:.2f}')
    print(f"Total: ${total:.2f}")
    #Print payment details
    print(f"Amount Paid: ${Amount_Paid:.2f}")
    print(f"Change: ${Change:.2f}")
    #Final message
    print("Thank You!")

# Function to handle checkout    
def Checkout():
  if not Cart: # Prevent checkout if cart is empty
    print('Cart is empty')
    return
#Call function to calculate totals
  subtotal, tax, discount, total = Calculate_Total()
  #Displayed calculated values
  print(f"Subtotal: ${subtotal:.2f}")
  print(f"Tax (10%): ${tax:.2f}")
  print(f'Discount: -${discount:.2f}')
  print(f"Total: ${total:.2f}")
  #Ask user to enter the amount paid
  try:
    Amount_Paid = float(input('Enter amount paid: $'))
 #Handles invalid amount
  except ValueError: 
    print('Invalid payment amount')
    return
#Checks if the user entered enough
  if Amount_Paid < total:
    print('Insufficient Funds') #Not enough money
    return
#Calculate the change to be given back
  Change = Amount_Paid - total
  #Display Change
  print(f'Change due: ${Change:.2f}')
  #Calls function to print the receipt
  Print_receipt(Cart, subtotal, tax, discount, total, Amount_Paid, Change)
  
  #Clear all items from the cart after check-out
  Cart.clear()
  #Save/update the inventory(Write Changes to the csv file )
  Store_Inventory()
  #Display message to the user that the system is ready for the next Customer
  print('Next Customer')
#Function to display exit message
def Goodbye():
  print('Thank you. Have a good day')
#Calls function to display the menu again
show_menu()
  
#Infinite loop to keep the pos system running
while True:
    #Display menu option to the user
  print('===== POS Menu ======')
  print('1. Menu | 2. Add to cart| 3. View cart| 4. Remove From Cart | 5. Checkout| 6. Exit')
  #Ask user to select on option
  selection = input ('Select Option:')
  if selection == '1': show_menu() #Show product menu
  elif selection == '2':add_item() # Add item to the cart
  elif selection == '3':view_cart() #View items in the cart
  elif selection == '4':remove_item() #Removes item from the cart
  elif selection == '5':Checkout() #Proceeds to checkout
  elif selection == '6':Goodbye() #Exit program
 #if the user enters anything else  
else:
    print('Invalid Option. Please try again')