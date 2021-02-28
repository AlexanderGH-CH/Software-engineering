"""
Created on Sun Dec 20 14:08:00 2020

@author: Alexander
"""

# Import the sys module
import sys
# Import os module
import os
# Import pandas as pd
import pandas as pd
# Import own module
import mulinreg


def get_properties(indicator):
    """Searches for properties based on the users input."""
    # If the customer selects option 1 then search with price.
    if indicator == 1:
        price = get_affordability()          # Get user data on affordability
        propertyinfo = get_propertyinfo()       # Get user data on property info
        # Get the listings that correspond to the user data
        properties = mulinreg.find_properties(propertyinfo[0],
                                              propertyinfo[1], propertyinfo[2],
                                              price)
        return properties
    # If the customer selects option 2 then search without price
    propertyinfo = get_propertyinfo()       # Get user data on property info
    # Get the listings that correspond to the user data
    properties = mulinreg.find_properties(propertyinfo[0],
                                          propertyinfo[1],
                                          propertyinfo[2], 0)
    return properties

def valid_input(help_info):
    """Validates input as being of type float."""
    while True:
        try:
            uinput = float(input(help_info))
            break
        except ValueError:       #raise error if uses wrong input non-float
            print('You have input a in-valid value')
    return uinput

def ask_user(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        sys.stdout.write("Please respond with 'yes' or 'no' "
                    "(or 'y' or 'n').\n")

def get_multiple(annual_income):
    """Returns the multiple based on the annual income."""
    if annual_income <= 100000:
        return 3.5
    elif annual_income > 100000 and annual_income <= 250000:
        return 4
    return 4.5

def get_financialinfo():
    """Gets the financial information from the user."""
    income = valid_input('Please enter your annual income: ')
    deposit = valid_input('Please enter the amount your would like to deposit: ')
    mlength = valid_input('Please enter your mortgage length: ')
    fininfo = [income, deposit, mlength]
    return fininfo


def get_affordability():
    """Calculation of the price based on the users financial information."""
    # Get the users financial info for subsequent calculation
    ufininfo = get_financialinfo()
    # Calculate the price of the property based on the users financial information
    price = ufininfo[0]*get_multiple(ufininfo[0])+ufininfo[1]
    return price

def get_propertyinfo():
    """Gets the property details from the users."""
    propertyinfo = []
    # Get the number of rooms in the property
    rooms = valid_input('Please enter the number of rooms: ')
    while rooms <= 0 or rooms > 10:
        print('Invalid input, please enter a number in range 1 - 10')
        rooms = valid_input('Please enter the number of rooms: ')
    propertyinfo.append(rooms)
    # Get the type of property
    typep = valid_input('Please enter the type: ')
    while typep <= 0 or typep > 3:
        print('Invalid input, please enter a number in range 1 - 3')
        typep = valid_input('Please enter the type: ')
    propertyinfo.append(typep)
    # Get the loction of the property
    location = valid_input('Please enter the location: ')
    while location <= 0 or location > 4:
        print('Invalid input, please enter a number in range 1 - 4')
        location = valid_input('Please enter the location: ')
    propertyinfo.append(location)
    return propertyinfo

def get_interest(amount_borrowed, price_property):
    """Calculates the interest based on the loan to value ratio."""
    # LTV = loan amount / price of property
    LTV = amount_borrowed/price_property
    if LTV >= 0.95:
        interest = 0.0499
    elif LTV < 0.95 and LTV >= 0.90:
        interest = 0.0449
    elif LTV < 0.9 and LTV >= 0.85:
        interest = 0.0399
    elif LTV < 0.85 and LTV >= 0.80:
        interest = 0.0349
    else:
        interest = 0.0299
    return interest

def calculate_credit(official_price, predicted_price):
    """Calculates the probability of mortgage acceptance as well as the monthly payments"""
    # Get the financial information and calculate the affordability
    while True:
        credit = []
        while True:
            fininfo = get_financialinfo()
            # Formulae ussed: Amount borrowed = loan amount = asking price - deposit
            amount_borrowed = official_price-fininfo[1]
            if fininfo[1] > amount_borrowed:
                print("No need for any further calulations you can buy"
                      "the house directly with the desposit")
                return False
            # Check if the amount borowed exceed the maximum amount
            if get_multiple(fininfo[0]) * fininfo[0] < amount_borrowed:
                print("The amount borrowed exceeds the maximum amount to be"
                      " borrowed based on your income")
                # User needs to re-enter the data if amount borrowed is exceeded
                reenteryn = ask_user('Would you like to re-enter the data?')
                if reenteryn == False:
                    return False
                else:
                    pass
            else:
                break          
        # Check if the loan would be larger than the predicted amount
        if amount_borrowed > predicted_price:
            # If amount borrowed to large inform the user
            print("We are sorry to inform you, but \nwith the provided details"
                  " your application would be unlikely to be successful")
            reenteryn = ask_user('Would you like to re-enter your financial details? ')
            if reenteryn == False:
                return False
            else:
                # Clear any data from the list for multiple usage
                credit.clear()   
        else:
            break
    # Appending is only possible if all checks are passed
    credit.append(int(fininfo[2]))
    #print(fininfo[2])
    credit.append(int(amount_borrowed))
    all_months = fininfo[2]*12
    #print(all_months)
    # Calculate the interest the user needs to pay per month
    interest = (get_interest(amount_borrowed, official_price))/12
    #print(r)
    # Calculate the monthly amount to be paid based on the formulae
    monthlyam = amount_borrowed*((interest*(1+interest)**all_months)/
                                 (((1+interest)**all_months)-1))
    credit.append(int(monthlyam))
    # Caclulate the total amount to be paid over the loan length
    totalam = monthlyam*all_months
    #print(t)
    credit.append(int(totalam))
    return credit
    
def save_results(propertyinfo, i):
    """Saves the search results from the user."""
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(r'C:\Users\Alexander\Desktop\Properties_SearchResults.xlsx', 
                            engine='xlsxwriter')
    if i != 0:
        k = pd.DataFrame([i], columns=['Mortgage_length', 'Mortgage_amount',
                                       'Monthly_Payment', 'Total_Payment'],
                         dtype=int)
        # Write each dataframe to a different worksheet.
        propertyinfo.to_excel(writer, sheet_name='Property information', index=False)
        k.to_excel(writer, sheet_name='Mortgage information', index=False)
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        print('Results saved in: ', os.getcwd())
    else:
        # Write the dataframe to the excel sheet
        propertyinfo.to_excel(writer, sheet_name='Property information', index=False)
        writer.save()
        print('Results saved in: ', os.getcwd())
        
# Start of the program
print('Hi there, thank you for using our app.')

# Large loop to guide the user through the program
while True:
    # Starting question to be answered
    x = int(input("Would you like to look for a property? [1] \n"
                  "or \nWould you like to look for affordable properties? [2]"
                 "\nYour choice: "))
    if x == 1:
        # Loop to get property characteristica
        while True:
            # Get the properties for the user
            propdata = get_properties(2)
            # If the returned dataframe is empty inform the user
            if propdata.empty:
                print("Sorry we could not find any properties that match"
                      " the given characteristics")
                startagain = ask_user('Would you like to start over again?')
                if startagain == False:
                    break
            # If the returned dataframe is not-empty then display the properties
            else:
                propdata.reset_index(drop=True, inplace=True)       #Reset index to start at 0
                print(propdata)
                # Get credit probability and monthly payment
                credityn = ask_user("Would you like to to see the credit approval probability \n"
                                    "and monthly payment for a specific property ? ")
                if credityn == True:
                    while True:
                        propid = valid_input('Please enter the List_ID: ')
                        if propid not in propdata.List_ID.values:          #check if provided List_ID in dataframe
                            print('Sorry we could not find any property with such an ID, please re-enter it')
                        break                          
                    proprow = (propdata[(propdata['List_ID'] == propid)])         # Get the corresponding row with the provided List_ID
                    print(proprow)
                    f = proprow.iloc[0]['Price']        # Assign the Price to a variable
                    j = proprow.iloc[0]['Predictions']      #Assign the Predictions to a variable
                    creditdetails = calculate_credit(f, j)       #Call the function to get the details on the credit
                    # If user quits in function calculate_credit
                    if creditdetails == False:
                        print('')
                    else:
                        # Print what the user has to pay in total, per month and the amount he borrowed.
                        print("For a {}-year mortgage ({}), you need to pay {} "
                              "per month, and {} in total.'"
                              .format(creditdetails[0], creditdetails[1],
                                      creditdetails[2], creditdetails[3]))
                    # Option for user to save the results
                    save = ask_user('Would you like to save the search results?')
                    if save == True:
                        # Save the results using a function
                        save_results(proprow, creditdetails)
                        break
                    break
                # Option for user to save the results
                if credityn == False:
                    save = ask_user('Would you like to save the search results?')
                    if save == True:
                        save_results(propdata, 0)
                        break
                    break
                   
    elif x == 2:
        # Loop to get property characteristica
        while True:
            # Get the property information
            propdata =get_properties(1)
            # If the returned dataframe is empty then inform the user
            if propdata.empty:
                print("Sorry we could not find any properties that match the"
                      " given characteristics")
                startagain = ask_user('Would you like to start over again?')
                if startagain == False: 
                    break
            else:
                # If the returned dataframe is not-empty then display the properties
                propdata.reset_index(drop=True, inplace=True)
                print(propdata)              
                # Option for user to save the results
                save = ask_user('Would you like to save the search results?')
                if save == True:
                    save_results(propdata, 0)
                break
    
    # Ask the user whether he wants to continue using the program or not
    startagain = ask_user('Would you like to start all over again?')
    if startagain == True: 
        pass
    else:
        break

# Final goodbye message
print('Thank you for using the application')


        