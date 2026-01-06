from queue_manager import QueueManager
from auth import login

def receptionist_menu(qm):
    while True:
        print("\n--- Reception Menu ---")
        print("1. Register Patient")
        print("2. Call Next Patient")
        print("3. View Queue")
        print("0. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Patient Name: ")
            nid = input("National ID: ")
            service = input("Service Type: ")
            p = qm.register_patient(name, nid, service)
            print(f"Registered: {p.token} - {p.name}")

        elif choice == "2":
            p = qm.call_next()
            if p:
                print(f"Calling: {p.token} - {p.name}")
            else:
                print("No waiting patients.")

        elif choice == "3":
            print("\nCurrent Queue:")
            for p in qm.get_queue():
                print(f"{p.token} | {p.name} | {p.service_type} | {p.status}")

        elif choice == "0":
            break

        else:
            print("Invalid choice.")

def admin_menu(qm):
    while True:
        print("\n--- Admin Menu ---")
        print("1. View Report")
        print("2. View Queue")
        print("0. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            print("\n--- Report ---")
            print(f"Patients Served: {qm.served_count()}")
            for p in qm.get_queue():
                print(f"{p.token} | {p.name} | {p.status}")

        elif choice == "2":
            for p in qm.get_queue():
                print(f"{p.token} | {p.name} | {p.service_type} | {p.status}")

        elif choice == "0":
            break

        else:
            print("Invalid choice.")

def main():
    qm = QueueManager()

    while True:
        role = login()
        if role == "RECEPTIONIST":
            receptionist_menu(qm)
        elif role == "ADMIN":
            admin_menu(qm)
        else:
            print("Try again.")

if __name__ == "__main__":
    main()

