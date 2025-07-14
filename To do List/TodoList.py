task_list = []

def print_intro():
    print("\nWelcome to the To-Do List Maker")
    print("This tool helps you stay organized by creating and managing your tasks in one place.")
    print("Add items to your to-do list, mark them as completed, edit them when priorities change, or delete them once they're no longer needed.\n")

def print_task():
    print("Your tasks:")
    if not task_list:
        print("  No tasks yet.")
        return
    for idx, task in enumerate(task_list, 1):
        status = '✔' if task['completed'] else ' '
        print(f"  {idx}. [{status}] {task['task']}")

print_intro()  
while True:
    print("\nWhat do you want to do?")
    print("1. Enter a task")
    print("2. Complete a task")
    print("3. View tasks")
    print("4. Delete a task")
    print("5. Edit a task")
    print("6. Quit\n")

    user_input = input("Enter what you want to do (1-6): ").strip()

    if user_input == "1":
        print()
        task = input("Enter your task: ").strip()
        if task:
            task_list.append({'task': task, 'completed': False})
            print("Your task is entered.")
        else:
            print("Task cannot be empty.")

    elif user_input == "2":
        print()
        print_task()
        print()
        try:
            idx = int(input("Enter the index of the completed task: "))
            if 1 <= idx <= len(task_list):
                task_list[idx-1]['completed'] = True
                print(f"'{task_list[idx-1]['task']}' marked as completed.")
            else:
                print("Invalid index.")
        except ValueError:
            print("Please enter a valid number.")

    elif user_input == "3":
        print()
        print_task()
        print()

    elif user_input == "4":
        print()
        print_task()
        print()
        try:
            idx = int(input("Enter index of the task to delete: "))
            if 1 <= idx <= len(task_list):
                removed = task_list.pop(idx-1)
                print(f"'{removed['task']}' has been deleted.")
            else:
                print("Invalid index.")
        except ValueError:
            print("Please enter a valid number.")

    elif user_input == "5":
        print()
        print_task()
        print()
        try:
            idx = int(input("Enter the index of the task to edit: "))
            if 1 <= idx <= len(task_list):
                new_task = input(f"Enter the new task for '{task_list[idx-1]['task']}': ").strip()
                if new_task:
                    old_task = task_list[idx-1]['task']
                    task_list[idx-1]['task'] = new_task
                    print(f"'{old_task}' changed to '{new_task}'.")
                else:
                    print("Task cannot be empty.")
            else:
                print("Invalid index.")
        except ValueError:
            print("Please enter a valid number.")

    elif user_input == "6":
        print("\nExiting.")
        break

    else:
        print("Please enter a number from 1 to 6.")