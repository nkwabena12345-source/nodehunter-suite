import hashlib

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 1
    return score

def register():
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    
    # check strength
    score = check_strength(password)
    if score < 3:
        print(f"❌ Password too weak! Score {score}/4")
        return
    
    # HASH IT
    hashed = hash_pass(password)
    
    with open("users_secure.txt", "a") as f:
        f.write(f"{username}:{hashed}\n")
    print(f"✅ Account created! {username} - Strength: {score}/4")
    print(f"Hashed: {hashed[:15]}... (hidden)")

def login():
    username = input("Username: ")
    password = input("Password: ")
    hashed_input = hash_pass(password)
    
    try:
        with open("users_secure.txt", "r") as f:
            for line in f:
                u, h = line.strip().split(":")
                if u == username and h == hashed_input:
                    print(f"\n✅ Welcome back {username}! Login successful!")
                    return
        print("❌ Wrong username or password!")
    except FileNotFoundError:
        print("No users yet!")

while True:
    print("\n--- SECURE CYBER-LAB ---")
    print("1. Register\n2. Login\n3. Exit")
    choice = input("Choose 1/2/3: ")
    if choice == "1": register()
    elif choice == "2": login()
    elif choice == "3":
        print("Bye NodeHunter!")
        break
