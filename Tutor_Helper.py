from datetime import datetime as dt
import time
import csv
from operator import itemgetter


def main_menu():
    '''Used to display the main menu'''

    # Title and name
    print(f"{'Welcome To':^25}\n{'Tutor Helper!':^25}\n-------------------------\n")
    # User options
    print(
        "[1] Add or Remove a Student\n"
        "[2] View Student List\n"
        "[3] Create/Cancel a Lesson\n"
        "[4] View Your Calendar\n"
        "[5] View Monthly Revenue\n"
        "\n[6] Exit\n"
    )
    # Let's user choose option
    return input('What would you like to do? ')


def small_list():
    '''A function for a more concise student list that is used in some other functions (repeated code)'''
    
    # Opens the file and prints every line that contains a students (so everything but the first line)
    with open('tutoring_students.csv') as f:
        reader = enumerate(csv.reader(f))
        for i, row in reader:
            if i > 0 and len(row) > 0:
                print(row[0])
            time.sleep(0.2)


def add_remove_student():
    '''
    Gives the user the ability to add/remove students from their account.
    When adding a student, user must input the student's full name, subject 
    being taught, grade level, and hourly rate of payment.
    '''

    # Lets user choose to add or remove a student
    ans = input("Would you like to Add(1) or Remove(2) a student [1 or 2]: ")
    
    # Add student
    if ans == "1":
        # A list of subjects that are in the system (for sorting an other uses)
        valid_subjects = ('advanced functions','functions','calculus','physics','chemistry','biology','english','french')
        # Name input
        name = input("\nPlease enter the student's name: ")
        print("\nValid Subjects:")
        # Prints the valid subjects so the user may see what they are
        for subject in valid_subjects:
            print(subject.title())
            time.sleep(0.2)  # Adds a small delay between each print statement (more user friendly)
        # Subject input
        subject = input("\nWhat subject will you be teaching?: ").title()
        if subject.lower() not in valid_subjects:  # Warns the user they enetered a subject that is not in valid_subjects (won't be sorted by subject)
            input("WARNING: That subject is not in the list\n(Note: Lessons with this subject will be sorted in 'other')\npress enter to continue")
        # Grade level and rate inputs
        grade = input("\nSubject's grade level: ")
        rate = input("Hourly rate?: ")
        # Stores information in the tutoring_student.csv file with proper formatting
        with open('tutoring_students.csv', 'a') as f:  # Using 'with; to open a file closes it automatically after it's done using it
            f.write(f"\n{name}, {subject}, {grade}, {rate}")
        print("\nStudent Succesfully Added!")
        
        # Runs the function again if the user wants to add another student (a good use of recursion I think)
        another_student = input("\nWould you like to add or remove another student? [y/n]: ")
        if another_student == "y":
            return add_remove_student()


    # remove student
    elif ans == "2":
        # Prints a list of students from the tutoring_students file using the small_list() function
        print('\nHere is a list of your students:')
        small_list()
        # Gathers all the students in a list except for the one being deleted
        remove = input("\nWhich student would you like to remove?: ")
        students = list()
        with open('tutoring_students.csv') as readfile:  # Reads the file and appends the desired rows to 'students'
            reader = csv.reader(readfile)
            for row in reader:
                if len(row) == 0:
                    continue
                if row[0] != remove:
                    students.append(row)
        # This overwrites the file using the list of students
        with open('tutoring_students.csv', 'w', newline='') as writefile:
            writer = csv.writer(writefile)
            writer.writerows(students)
        print("\nStudent Removed")
        
        # Runs the function again if the user wants to add another student (a good use of recursion I think)
        another_student = input("\nWould you like to add or remove another student? [y/n]: ")
        if another_student == "y":
            return add_remove_student()

    # The input is 'returned' so it can be used to go back to main menu or 
    # exit the run() function
    return input("\nPress enter to go back to main menu, or 'exit' to close the program ")


def student_list():
    '''Let's the user view all of their students in a list'''

    print('Here is a list of your students:')
    print(f"{'Name':<21} {'Subject':<21} {'Grade':<7} {'Hourly Rate':<4}")
    # Prints a list of students from the tutoring_students.csv file and organizes them by column
    with open('tutoring_students.csv', 'r') as f:
        reader = enumerate(csv.reader(f))  # This assigns an index value to each row to facilitate iteration
        for i, row in reader:
            if i > 0 and len(row) > 0:
                print(f"{row[0]:<20} {row[1]:<21} {row[2]:<7} {row[3]:<4}/hr")
                time.sleep(0.2)
    
    # Exit input
    time.sleep(2)
    return input("\nPress enter to go back to main menu, or 'exit' to close the program ")


def lesson():
    '''
    Asks for the name of the student, and the date and length of the lesson 
    and adds it to a lessons file
    '''

    # Let's user decide whether to create or cancel
    ans = input("Would you like to create(1) or cancel(2) a lesson? [1 or 2]: ")

    # Create a lesson
    if ans == "1":
        # Shows user their student's names
        print("\nYour Students:")
        small_list()
        # Asks for the name
        name = input("\nStudent: ")
        # Extracts subject from list of students
        with open('tutoring_students.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 0:
                    continue
                if row[0] == name:
                    subject = row[1]  # the indexes connect to each column in the csv (1 is subject, 3 is hourly rate)
                    rate = row[3]
        # Asks for the date, start time, and length of the lesson
        date = dt.strptime(input("Enter the date for your lesson (mm/dd/yy): "), '%m/%d/%y').date()  # strptime() method changes a string to a datetime value
        start_time = dt.strptime(input('Start time (HH:MM AM/PM): '), '%I:%M %p').time()
        duration = float(input("How many hours?: "))
        # Adds the lesson to the lessons file
        with open('tutoring_lessons.csv', 'a') as f:
            f.write(f"\n{name},{subject}, {date}, {start_time:%I:%M %p}, {duration}, {duration*float(rate)}")
        # Asks user if they would like to add/remove another lesson and calls the lesson function again
        another_lesson = input("\nWould you like to add or remove another lesson? [y/n]: ")
        if another_lesson == "y":
            return lesson()  # If this returns, it will end the function so the exit input doesn't show up twice
        # Exit input
        return input("\nLesson Added!\nPress enter to go back to main menu, or 'exit' to close the program ")
    
    # Delete a lesson
    elif ans == "2":
        # Shows a list of current lessons by their index to allow user to choose cancellation by index number
        print(f"   {' Name':<22} {'Subject':<20} {'Date':<11} {'Time':<7} {'Duration':<10}")
        with open("tutoring_lessons.csv", "r") as f:
            reader = enumerate(csv.reader(f))
            for i, row in reader:
                if len(row) == 0:
                    continue
                if i > 0:
                    print(f"[{i}] {row[0]:<20} {row[1]:<20} {row[2]:<11} {row[3]:<7} {row[4]} hrs")
        # Reads tutoring_lessons.csv and appends the lessons you want to keep to 'updated_file'
        cancel = input("Which lesson do you want to cancel?: ")
        updated_file = []
        with open("tutoring_lessons.csv", "r") as readfile:
            reader = enumerate(csv.reader(readfile))
            for i, row in reader:
                if str(i) != cancel:  # Adds all rows except for the row at the index inputted by the user to updated_file
                    updated_file.append(row)
        # Uses updated file to overwrite the original file
        with open("tutoring_lessons.csv", "w", newline ='') as writefile:
            writer = csv.writer(writefile)
            writer.writerows(updated_file)  # writerows() treats every sublist in updated_file as a row when writing to file
         # Asks user if they would like to add/remove another lesson and calls the lesson function again
        another_lesson = input("\nWould you like to add or remove another lesson? [y/n]: ")
        if another_lesson == "y":
            return lesson()
        # Exit input
        return input("\nLesson Canceled\nPress enter to go back to main menu, or 'exit' to close the program ")

    # Exit input when the user doesn't choose add or cancel lesson (invalid input)
    return input("\nPress enter to go back to main menu, or 'exit' to close the program ")


def calendar():
    '''A calendar to show the user all of their upcoming lessons sorted by date'''

    lessons = []
    # Stores all upcoming lessons in 'lessons' (the ones we want to actually display)
    with open("tutoring_lessons.csv", "r") as readfile:
        reader = enumerate(csv.reader(readfile))
        for i, row in reader:
            if len(row) == 0:
                continue
            if i > 0:
                if dt.strptime(row[2], ' %Y-%m-%d').date() >= dt.now().date():  # Compares the date of the lesson to the current date on the user's computer
                    lessons.append(row)                                        # If it is later than the current date, it adds it to 'lessons'
    
    # Sorts lessons by date. itemgetter() sets the sorting key to be the 3rd item (index 2) of the inner lists that are being sorted. In this case, the dates.
    sorted_lessons = sorted(lessons, key=itemgetter(2))

    # Prints out the lessons sorted by date
    print("Your Calendar")
    print(f"{'Name':<21} {'Subject':<22} {'Date':<18} {'Time':<8} {'Duration':<6}")
    for row in sorted_lessons:
        print(f"{row[0]:<20} {row[1]:<23} {dt.strptime(row[2], ' %Y-%m-%d'):%a, %B %d} {row[3]:>9} {row[4]} hrs")
        time.sleep(0.2)
    
    #Exit input
    time.sleep(2)
    return input("\nTo Continue\nPress enter to go back to main menu, or 'exit' to close the program ")


def revenue():
    '''
    Allows the user to see their revenue from the lessons they have completed 
    or will complete throughout the current month (user is paid monthly)
    '''

    # Placeholder variable for revenue
    revenue = 0
    # Finds the lessons who's dates are during the current month on the user's computer 
    # and adds that lesson's "payment" value to revenue
    with open("tutoring_lessons.csv", "r") as f:
        reader = enumerate(csv.reader(f))
        current_month = f"{dt.now().date():%m}"  # f string is used to only extract the month value
        for i, row in reader:
            if len(row) == 0:
                continue
            if i > 0:
                month = f"{dt.strptime(row[2], ' %Y-%m-%d'):%m}"
                if month == current_month:    # If the month of the lesson is the same as current month
                    revenue += float(row[5])  # the payment value (index 5 of the row) gets added to revenue
    # Displays user's revenue
    print(f"Your revenue for this month is: ${revenue}")
    # Exit input
    return input("\nPress enter to go back to main menu, or 'exit' to close the program ")


def run():
    '''
    This is where the program is run and where the functions are called
    A while loop is used so that the program only stops when the user selects 
    exit in the main menu or types 'exit' when prompted
    '''
    while True:
        print("\n-------------------------")
        # Takes user's input from main menu
        option = main_menu()
        
        # A set of if statements that will run the corresponding function from user input
        if option == "1":
            print("\n-------------------------\n")
            out = add_remove_student()
            # This is used to let the user terminate the program
            if out.lower() == 'exit':
                break
        
        elif option == "2":
            print("\n-------------------------\n")
            out = student_list()
            if out.lower() == 'exit':
                break
        
        elif option == "3":
            print("\n-------------------------\n")
            out = lesson()
            if out.lower() == 'exit':
                break
        
        elif option == "4":
            print("\n-------------------------\n")
            out = calendar()
            if out.lower() == 'exit':
                break
        
        elif option == "5":
            print("\n-------------------------\n")
            out = revenue()
            if out.lower() == 'exit':
                break
        
        elif option == "6":
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    run()

# Create a 'refresh/speed up' option that goes through the 2 files and removes empty lines