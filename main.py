import os
import hashlib

# Create tasks folder if not exists
if not os.path.exists("tasks"):
    os.makedirs("tasks")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for line in f:
                stored_user = line.strip().split(",")[0]
                if stored_user == username:
                    print("User already exists!")
                    return

    with open("users.txt", "a") as f:
        f.write(username + "," + hash_password(password) + "\n")

    print("Registration successful!")


def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if not os.path.exists("users.txt"):
        print("No users found. Register first.")
        return None

    with open("users.txt", "r") as f:
        for line in f:
            user, stored_password = line.strip().split(",")
            if user == username and stored_password == hash_password(password):
                print("Login successful!")
                return username

    print("Invalid credentials!")
    return None


def add_task(username):
    task = input("Enter task: ").strip()

    if task == "":
        print("Task cannot be empty!")
        return

    file = f"tasks/{username}.txt"

    task_id = 1
    if os.path.exists(file):
        with open(file, "r") as f:
            task_id = len(f.readlines()) + 1

    with open(file, "a") as f:
        f.write(f"{task_id},{task},Pending\n")

    print("Task added!")


def view_tasks(username):
    file = f"tasks/{username}.txt"

    if not os.path.exists(file):
        print("No tasks found.")
        return

    print("\nYour Tasks:")
    print("-" * 30)

    with open(file, "r") as f:
        for line in f:
            tid, task, status = line.strip().split(",")
            print(f"{tid}. {task} [{status}]")

    print("-" * 30)


def mark_complete(username):
    file = f"tasks/{username}.txt"

    if not os.path.exists(file):
        print("No tasks found.")
        return

    task_id = input("Enter task ID: ").strip()
    updated_tasks = []
    found = False

    with open(file, "r") as f:
        for line in f:
            tid, task, status = line.strip().split(",")
            if tid == task_id:
                status = "Completed"
                found = True
            updated_tasks.append(f"{tid},{task},{status}\n")

    with open(file, "w") as f:
        f.writelines(updated_tasks)

    if found:
        print("Task marked as completed!")
    else:
        print("Task ID not found!")


def delete_task(username):
    file = f"tasks/{username}.txt"

    if not os.path.exists(file):
        print("No tasks found.")
        return

    task_id = input("Enter task ID: ").strip()
    updated_tasks = []
    found = False

    with open(file, "r") as f:
        for line in f:
            tid, task, status = line.strip().split(",")
            if tid != task_id:
                updated_tasks.append(f"{tid},{task},{status}\n")
            else:
                found = True

    with open(file, "w") as f:
        f.writelines(updated_tasks)

    if found:
        print("Task deleted!")
    else:
        print("Task ID not found!")


def user_menu(username):
    while True:
        print(f"\nLogged in as: {username}")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Complete")
        print("4. Delete Task")
        print("5. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_task(username)
        elif choice == "2":
            view_tasks(username)
        elif choice == "3":
            mark_complete(username)
        elif choice == "4":
            delete_task(username)
        elif choice == "5":
            print("Logged out.")
            break
        else:
            print("Invalid choice!")


def main():
    while True:
        print("\n===== TASK MANAGER =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                user_menu(user)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()