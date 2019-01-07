from data.grader import grader

def display_menu():
    print("Enter the the number of the command.\nCTRL-C to exit.\n")
    print("1. " + "Grade an Assignments.")
    print("2. " + "Enter a new assignment.")

def get_menu_option():
    valid = False 
    while not valid:
        try:
            val = int(input())
            valid = True
            return val
        except ValueError:
            print("Must be an integer.")
    
def main():
    display_menu()
    option = get_menu_option()
    while option < 3:
        grader.grade() if option == 1 else grader.enter_new_assignment()
        print("\n")
        display_menu()
        option = get_menu_option()

main()
