USERS = {
    "admin": ("adminpass", "ADMIN"),
    "reception": ("receppass", "RECEPTIONIST")
}


def login():
    print("\n=== AQMS LOGIN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username in USERS and USERS[username][0] == password:
        print(f"Login successful ({USERS[username][1]})\n")
        return USERS[username][1]
    else:
        print("Invalid credentials.\n")
        return None
