import sys
import json
import time

def open_file():
    try:
         with open("list_task_CLI.json", "r") as file:
            muat_task = json.load(file)
            if not muat_task:
                return []
    except FileNotFoundError:
        file = open("list_task_CLI.json", "x")
        return []
    except json.JSONDecodeError as e:
        print(f"this error: {e}")
    return muat_task

muat_task = open_file()

def add_task(muat_task):
        new_id = 1
        while any(task["id"] == new_id for task in muat_task):
            new_id += 1

        muat_task.append({
        "id" : new_id,
        "description" : sys.argv[2],
        "status" : "todo",
        "created_at" : time.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at" : ""
    })
        muat_task.sort(key=lambda task: task["id"])
        return muat_task

def delete_task(muat_task, task_id):
    kosong = []
    for task in muat_task:
        if task != task_id:
            kosong.append(task)
    muat_task = kosong
    return muat_task

def clear_task():
    return []

def update_task(muat_task):
        task_id = int(sys.argv[2])
        new_description = sys.argv[3]
        for task in muat_task:
            if task["id"] == task_id:
                task["description"] = new_description
                task["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                break
        return muat_task

def mark_task_in_progress(muat_task, task_id):
        for task in muat_task:
            if task["id"] == task_id:
                task["status"] = "in_progress"
                task["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                break
        return muat_task

def mark_task_in_done(muat_task, task_id):
    for task in muat_task:
        if task["id"] == task_id:
            task["status"] = "done"
            task["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            break
    return muat_task

def list_task(muat_task):
        for task in muat_task:
            print(f"ID: {task['id']}, \nDescription: {task['description']}, \nStatus: {task['status']}, \nCreated At: {task['created_at']}, \nUpdated At: {task['updated_at']}\n")

def list_task_by_status(muat_task, status):
    for task in muat_task:
        if task["status"] == status:
            print(f"ID: {task['id']}, \nDescription: {task['description']}, \nStatus: {task['status']}, \nCreated At: {task['created_at']}, \nUpdated At: {task['updated_at']}\n")

def save_tasks_to_file(muat_task):
    with open("list_task_CLI.json", "w") as file:
        json.dump(muat_task, file, indent=4)

if len(sys.argv) < 2:
    print("Please provide a command.")
    sys.exit(1)
else:
    command = sys.argv[1]
    cmd_list = ["add", "list", "delete", "update", "mark-in-progress", "mark-in-done", "help", "clear"]
    if command not in cmd_list:
        print(f"Unknown command: {command}")
        sys.exit(1)
    elif command == "help":
        print("Available commands:")
        print("add <description> - Add a new task")
        print("list - List all tasks")
        print("delete <id> - Delete a task by ID")
        print("update <id> <new_description> - Update a task's description by ID")
        print("mark-in-progress <id> - Mark a task as in progress by ID")
        print("mark-in-done <id> - Mark a task as done by ID")
    else:
        try:
            if command == "add":
                muat_task = add_task(muat_task)
            elif command == "list":
                if len(sys.argv) == 2:
                    list_task(muat_task)
                else:
                    list_task_by_status(muat_task, sys.argv[2])
            elif command == "delete":
                muat_task = delete_task(muat_task, int(sys.argv[2]))
            elif command == "clear":
                muat_task = clear_task()
            elif command == "update":
                muat_task = update_task(muat_task)
            elif command == "mark-in-progress":
                muat_task = mark_task_in_progress(muat_task, int(sys.argv[2]))
            elif command == "mark-in-done":
                muat_task = mark_task_in_done(muat_task, int(sys.argv[2]))
        except IndexError:
            print("Missing arguments for the command.")
        except Exception as e:
            print(f"this error: {e}")
            sys.exit(1)
        save_tasks_to_file(muat_task)