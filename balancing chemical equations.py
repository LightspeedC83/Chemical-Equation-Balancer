"""
The following is a program that balances an inputted chemical equation by utilizing a function that counts the number of "atoms" in a string by identifying their elemental symbol through the use of differentiation between capital and lowercase letters. Then it determines the number associated with that atomic symbol by following the rules and special cases associated. The program utilizes this function, in combination with an algorithm that generates all possible combinations of coefficients (within a maximum value for each coefficient), to balance the equation. It does this by generating the next coefficient combination, and counting the atoms on both sides of the equation and then determining if the coefficients balance the equation, and if not, proceeding to the next coefficient combination and so on.
"""

import math #importing the math module, which is used by the brute force algorithm to try all the possible coefficient combinations

####################################
# Defining functions for later use #
####################################
#note that procedures in Python are called functions, all references to functions in the comments reference procedures

#function that takes the raw equation string and turns it into data that the program can work with
def process_equation(raw_equation, separation_symbol):
  """
  this gets the string for each coefficient and compound associated fron the equation
  ---this function is not used multiple times, in the program. 
  The reason this is a funciton is to help with segmenting of code and abstraction.
  """

  reactant_side = raw_equation.split(separation_symbol)[0]
  product_side = raw_equation.split(separation_symbol)[1]

  if '+' in reactant_side:  #getting a list of all the reactants if there are multiple
    reactants = reactant_side.split('+')

    #removing any white space on each side
    strip_index = 0
    for item in reactants: 
      reactants[strip_index] = reactants[strip_index].strip()
      strip_index += 1

  else: #if there is only one reactant it strips that and adds it to a list 
    reactants = [reactant_side.strip()]

  if '+' in product_side:  #getting a list of all the products if there are multiple
    products = product_side.split('+')

    #removing any white space on each side
    strip_index = 0
    for item in products: 
      products[strip_index] = products[strip_index].strip()
      strip_index += 1  
  else:
    products = [product_side.strip()]
  
  return(reactants, products)


#function that counts the number of atoms on each side of the equation and returns the count in dictionary form 
def count_atoms(compound_list):
  atom_count = {} #dictionary that keeps a count of the total amount of atoms present, this will be the output of the function
  skipped_indexes = [] #a list of indexes for the counting function to not count beacause these indexes are inside of parentheses and will be counted when the function recursively calls itself. This way they are not counted twice

  for entry in compound_list: 
    compound_coefficient = entry[0] #getting the coefficient from the list of reactants and prducts
    compound_formula = entry[1] #getting the compound name
        

    #this part of the function isolates the different elements in the compound. 
    """
    There are alot of rules and exceptions for counting the number of times an element's atoms appears in a formula. These rules are easy and intuitive for a human, but not so for computers.
    Because of this, the part of the function (below) that performs this task requires a lot of nesting and if statements to cover all of the different possible conditions.
    """    
    current_index = 0
    for character in compound_formula:

      if character.isalpha() and character.isupper() and not(current_index in skipped_indexes):
        #looks ahead in the formula to find the element symbol and the number associated with it
        next_character = ''
        try:
          next_character = compound_formula[current_index +1]

        except IndexError: #if there nothing ahead of the current_index in the compound, it will add the atom at the current index's number of occurences (determined by the coefficient) to the atom_count dictionary
          #case for when there is only one character
          if character in atom_count.keys():
            atom_count[character] = atom_count[character] + (compound_coefficient * 1)
          else:
            atom_count[character] = compound_coefficient * 1 #we know that it should be a one because there is no number behind it and that means that one is present, I am choosing to include the *1 operation for clarity in the program although it is not strictly necessary

        if next_character != '': #if there is in fact another character after the current index, what's inside here will run
           
          if next_character.isalpha() and next_character.islower(): #case for if there is a two character symbol
            element_symbol = character + next_character
            
            #does the same operation as before to determine if there is a character after the current element 
            try:
              next_x2_character = compound_formula[current_index +2]
              #case for if there is a two character symbol and an associated number
              if next_x2_character in '123456789': #the reason I don't use the isdigit() method is because there can't be a 0 in the first digit of the number
                #determining if there are any numbers after it to get the full associated number
                num_check_index = current_index + 3
                while True:
                  try: 
                    num_check = compound_formula[num_check_index]
                    if num_check.isdigit():
                      num_check_index += 1
                    else:
                      associated_number = int(compound_formula[current_index +2 : num_check_index])
                      break
                  except IndexError:
                    associated_number = int(compound_formula[current_index +2 : num_check_index])
                    break
                #adding the correct number of atoms to the atom_count dictionary
                if element_symbol in atom_count.keys():
                  atom_count[element_symbol] = atom_count[element_symbol] + (compound_coefficient * associated_number)
                else:
                  atom_count[element_symbol] = compound_coefficient * associated_number

              #case for when there is a two character symbol and no number associated, but another element follows it
              elif ( next_x2_character.isalpha() and next_x2_character.isupper() ) or next_x2_character == '(' :
                if element_symbol in atom_count.keys():
                  atom_count[element_symbol] = atom_count[element_symbol] + (compound_coefficient * 1)
                else:
                  atom_count[element_symbol] = compound_coefficient * 1


            except IndexError:
              #case where there is a two character symbol and no associated number and it is at the end of the compound, so there is no next character
              if element_symbol in atom_count.keys():
                atom_count[element_symbol] = atom_count[element_symbol] + (compound_coefficient * 1)
              else:
                atom_count[element_symbol] = compound_coefficient * 1

          if next_character in '123456789': #the case for when there is a one character symbol and a number after it
            #checking to see if there are any numbers after it
            num_check_index = current_index + 2
            while True:
              try: 
                num_check = compound_formula[num_check_index]
                if num_check.isdigit():
                  num_check_index += 1
                else:
                  associated_number = int(compound_formula[current_index +1 : num_check_index])
                  break
              except IndexError:
                associated_number = int(compound_formula[current_index +1 : num_check_index])
                break
            #adding the associated number to the count for that atom
            if character in atom_count.keys():
              atom_count[character] = atom_count[character] + (compound_coefficient * associated_number)
            else:
              atom_count[character] = compound_coefficient * associated_number

          if ( next_character.isalpha() and next_character.isupper() ) or next_character == '(' : #case for when there is a lone character smooshed inbetween some other characters with no associated numbers, and for when there is no associated number and a parenthesis afterwards
            if character in atom_count.keys():
              atom_count[character] = atom_count[character] + (compound_coefficient *1)
            else:
              atom_count[character] = compound_coefficient * 1
                 


      elif character == '(': #case for if there is a parenthesis present, there are different rules needed to apply when parts of a compound are in parentheses, that require the elements inside of the parentheses to be counted separately

        #finds what's inside the parentheses and the number behind it
        parentheses_index = current_index
        
        for x in range(len(compound_formula) - parentheses_index): #finding what's inside the parentheses
          continue_character = compound_formula[parentheses_index]
          if continue_character == ')':
            end_parenthesis_index = parentheses_index
            break

          parentheses_index += 1

        #finding the number associated with the parentheses_compound (which should appear directly after the end parenthesis)
        last_checked_index = end_parenthesis_index 
        while True:
          try: #finds the last occuring number in a row starting from the end parenthesis
            character_check = compound_formula[last_checked_index +1]
            if not character_check.isdigit():
              if last_checked_index == end_parenthesis_index:
                associated_number = 1
              else:
                associated_number = compound_formula[end_parenthesis_index +1 : last_checked_index +1]
              break

          except IndexError: #if it tries to take the next character and there is no next character, then this will run
            if last_checked_index == end_parenthesis_index:
              associated_number = 1
            else: 
              associated_number = compound_formula[end_parenthesis_index +1 : last_checked_index +1]
            break

          last_checked_index += 1
        
        #using the asociated number as a coefficient and calling this same function to count the atoms in the formula inside the parentheses and then adding that to the atom count dictionary
        associated_number = int(associated_number)
        recursion_compound = [associated_number, compound_formula[current_index +1 : end_parenthesis_index]]

        parenthetical_atoms = count_atoms([recursion_compound])
        
        for atom in parenthetical_atoms.keys(): #updating the count values for the parenthetical values using the compound's coefficient
          parenthetical_atoms[atom] = (parenthetical_atoms[atom] * compound_coefficient)
        
        #adding the count of the parenthetical compound to the atom count
        for atom in parenthetical_atoms.keys():
          if atom in atom_count.keys():
            atom_count[atom] = (atom_count[atom] + parenthetical_atoms[atom])
          else:
            atom_count[atom] = parenthetical_atoms[atom]

        #adding the indexes where the parenthetical compound occurs to the 'skipped_indexes' list so that when the program continues it will not count them as they have already been counted    
        for x in range(current_index, end_parenthesis_index +1):
          skipped_indexes.append(x)

        
      current_index +=1 
  
  return atom_count #returning the completed atom_count dictionary  
      

#function that, when given the current equation state, it will format it and output a string
def format_equation(reactant_state, product_state):
  """
  This funciton formats the representation of the equation into one string so that it can be outputted.
  --The reason for putting this code in a function, even though it's only used once, is to help with 
  segmenting of code and abstraction in the program. Additionally, it may be useful to have this function 
  in future versions of the program, where it may be neccessary to preform this task at multiple points in the program.
  """
  
  output = ""
  output_index = 0
  for reactant in reactant_state: 
    reactant_coefficient = reactant[0] #finding the coefficient
    if reactant_coefficient == 1:
      reactant_coefficient = ''
    else:
     reactant_coefficient = str(reactant_coefficient) 

    if output_index == 0: #putting it together
      output += reactant_coefficient + reactant[1]
    else:
      output += " + " + reactant_coefficient + reactant[1]
    output_index += 1

  output += ' --> '
  output_index = 0
  for product in product_state: #doing the same for the product's side of the equation
    product_coefficient = product[0] #finding the coefficient
    if product_coefficient == 1:
      product_coefficient = ''
    else: 
      product_coefficient = str(product_coefficient)

    if output_index == 0: #putting it together with the output
      output +=  product_coefficient + product[1]
    else:
      output += ' + ' + product_coefficient + product[1]
    output_index += 1

  return output #returning the formatted equation.



########################
# Start of the Program #
########################
while True:
  print("-"*60 +"\n\tThis is a program that balances chemical equations.\n" + "-"*60)

  #getting and checking the euquation
  while True: #loop for input check for the equation input --this will run until a valid input is provided
    raw_equation = input("\nEnter your unbalanced equation with reactants on the left and products on the right: \n").strip() #getting user input for the equation

    #making sure the user input is in the correct format
    if not("-->" in raw_equation): #making sure the yeild arrow is included
      print("Invalid Input. You must include the 'yeild arrow', symbolized by '-->', separating your reactants and products\n")
      continue


    if raw_equation.split("-->")[0] == '' or raw_equation.split("-->")[1] == '': #making sure that the equation has both reactants and products
      print("You must have elements or compounds on both sides of the equation.\n")
      continue
    else: 
      reactants, products = process_equation(raw_equation, '-->') #calling the funciton to process the raw equation to get workable data

    #finding the coefficients for the reactants and products and preparing them to pass through the count_atoms function
    #this also formats the equation so the coefficients can be easily and actively manipulated later in the program
    reactants_state = [] #creating a list of reactants to pass through the count_atoms function to perform an intital atom count
    for compound in reactants: #getting the coefficient and string value for each reactant
      index = 0
      for character in compound:
        if compound[index].isdigit():
          index += 1
        else:
          coefficient_value = compound[0:index]
          if not(coefficient_value.isdigit()): #if there is no coefficient, this sets it to one
            coefficient_value = 1
          else:
            coefficient_value = int(coefficient_value)

          reactants_state.append([coefficient_value, compound[index:]]) #appending the coefficient value and the string for the compound 
          break

    products_state = [] #creating a list of product to pass through the count_atoms function to perform an intital atom count
    for compound in products: #getting the coefficient and string value for each product
      index = 0
      for character in compound:
        if compound[index].isdigit():
          index += 1
        else:
          coefficient_value = compound[0:index]
          if not(coefficient_value.isdigit()): #if there is no coefficient, this sets it to one
            coefficient_value = 1
          else:
            coefficient_value = int(coefficient_value)   
                 
          products_state.append([coefficient_value, compound[index:]]) #appending the coefficient value and the string for the compound 
          break

    reactant_count, product_count = count_atoms(reactants_state), count_atoms(products_state) #calling the count_atoms function to count the number atoms on each side of the yeild arrow, by passing the formatted lists through

    #making sure that no atoms are 'created' or 'destroyed' in the equation (ie. there are the same atomic symbols on both sides)
    conservation_of_mass = True
    for atom in reactant_count.keys(): #making sure no atoms are in the reactant_count that are not in the product_count
      if atom not in product_count.keys():
        conservation_of_mass = False
        break

    for atom in product_count.keys(): #making sure no atoms are in the product_count that are not in the reactant_count
      if atom not in reactant_count.keys():
        conservation_of_mass = False
        break

    if conservation_of_mass == False:
      
      print("Invalid Input. You must enter an equation with the same elements on each side, you may not create or destroy matter, Alchemy is not real.\n")
      continue
    
    break #will stop the loop if all of the input checks do not run

  print(f"\nCounting up the atoms...\nReactants: \n{str(reactant_count)} \nProducts:\n{str(product_count)}\n")


  #checking to see if the equation entered is already balanced
  is_balanced = True
  for atom in reactant_count: 
    if reactant_count[atom] != product_count[atom]:
      is_balanced = False
      break
  if is_balanced:#if any of the atoms aren't the same on both sides, then what's in here will run
    print(f"Your equation is already balanced: \n{raw_equation}\n")
    continue


  #if the equation is not already balanced, what's under this will run

  #formatting the states of both the products and reactants to all have coefficients as one, so as to get a base from which to brute force
  for reactant in reactants_state:
    if reactant[0] != 1:
      reactant[0] = 1
  for product in products_state:
    if product[0] != 1:
      product[0] = 1

  #actually balancing the equation

  num_coefficients = len(reactants_state + products_state) #determining the number of coefficients that need to be tried in total

  while True: #this loop facilitates the repitition of this section of the program, which is triggered if no balanced equation is found
    while True: #getting a ceilling value from the user (ie. getting a maximum value to try for each digit in the coefficient combination)
      ceiling = input("Enter a maximum value for the coefficients (consider that higher values will take more time to process): ")
      try:
        ceiling = int(ceiling)
        break
      except ValueError:
        print("Input invalid. You must enter a number.")

    max_possible = [] #this is for the user's benefit and has no real use in the actual balancing of the equation
    for x in range(num_coefficients):  #getting and formatting the data for the Max_possible list of coefficients
      max_possible.append(ceiling)
    print(f"\nTrying all the possible coefficient combinations below {max_possible}...\n")

    active_combination = [] #setting the current state of possible coefficients to the base state (meaning all coefficients are one)
    for x in range(num_coefficients):  
      active_combination.append(1)

    combinations_tried = 1
    number_of_combinations = ceiling**num_coefficients #finding out how many different combinations are possible

    equation_found = False
    for x in range(1, number_of_combinations +1): #for each possible combination the algorithm will do the following
      #applying the current coefficicient state to the current equation state 
      #(once applied to the equation state, the program checks to see if it balances the equation and if not, the next coefficient state will be generated)
      index = 0 
      for compound in reactants_state: #applying the coefficient state to the equation state for the list representing reactants
        reactants_state[index][0] = active_combination[index]
        index += 1
      product_index = 0
      for compound in products_state:  #doing it for the products
        products_state[product_index][0] = active_combination[index]
        index += 1
        product_index += 1

      #checking to see if the current coefficient state balances the equation
      reactants_count = count_atoms(reactants_state) #calling the count_atoms() function and checking to see if the equation is balanced
      products_count = count_atoms(products_state)
      is_balanced = True
      for atom in reactants_count.keys():
        if reactants_count[atom] != products_count[atom]:
          is_balanced = False
          break

      if is_balanced: #if the equation is balanced, this formats and outputs it
        output_equation = format_equation(reactants_state, products_state)
        print(f'The balanced equation, found after {combinations_tried} possible combinations tried, is: \n{output_equation}\n')
        print(f'The final atom count for the balanced equation is: \n\treactants: {reactants_count} \n\tproducts: {products_count}\n')
        equation_found = True
        break

      else: #if the equation is not balanced by the current coefficinet state, then this section of code will generate the next combination using the current number in list of possible combinations
        combinations_tried += 1
          #################################################################################################################################################################
        ### the algorithm below that generates combinations based off of an input of a maximum value and number of places was created in collaboration with Chris McGrath ###
          #################################################################################################################################################################

        #the algorithm essentially works by counting up in a number system where the base is the maximum value for each digit, with the exception that a digit who's value would have been 0 becomes the maximum value
        
        power = number_of_combinations #first defining power as the number of possible combinations
        active_combination = [] #clearing the active combination list, which will hold the combination generated

        for i in range(num_coefficients): #this goes through each digit in the combination (ie. repeating the below num_coefficients amount of times)
          power = power/ceiling  #for each of the digits, the power is modified by dividing it by the maximum value for each digit (because the digit is found by dividing by the power, the farther right digits will tend to be larger)

          #getting the output digit by taking the ceiling of the quotient of current place in the number of combinations and the updated power,  then getting the modulos of that and the maximum value
          #(the updated power is the place value for the current digit in the number system with base "maxumum_value")
          output = math.ceil(x/power) % ceiling  

          if output == 0:#because 0 can't be one of the digits, if any of the values that it tries to append is 0, it will be changed to be the maximum place value
            output = ceiling

          active_combination.append(output)  #appending the digit produced to the active combination list

    if equation_found == False: #if a balanced equation is not found, this prompts the user to enter a higher ceiling value and repeats the above section of the program that balances the equation.
      print(f'All combinations of coefficients up to {str(max_possible)} were tried (totalling {str(combinations_tried)} combinations attempted) and none balanced the equation.\nTry repeating the program with a higher ceiling value.\n')

      retry_ceiling = input('Would you like to try a higher ceiling value? (yes/no): ').strip().lower() 
      if retry_ceiling in ['yes','y','yea']: #if the user wants to retry the equation that they have entered with a new ceiling value, this repeats the loop
        continue
      else: #if the user does not want to try again with a higher ceiling value, this breaks the loop
        break

    else: #if a balanced equation is found, this breaks the loop
      break
  
  #repeating the program
  repeat = input("Would you like to repeat the program from the beginning?(yes/no): \n").strip().lower()
  if repeat not in ["yes", "y", 'yea', 'repeat']:
    break
  
