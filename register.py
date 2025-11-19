import csv
import json
import random
from datetime import datetime

USER_FILE = 'users.csv'
SCORE_FILE = 'scores.csv'

class Registration:
    def __init__(self):
        self.logged_in = False
        self.current_user = {}
        self.role = 'user'  # can be 'admin'

    def register(self):
        user_name = input("Enter username: ")
        if self.user_exists(user_name):
            print("Username already exists.")
            return

        role = input("Enter role (user/admin): ").strip().lower()
        pswd = input("Enter your password : ")
        cnf_pswd = input("Re-enter your password : ")

        if pswd != cnf_pswd:
            print("Password Mismatch")
            return

        if role == "user":
            f_name = input("Enter First name : ")
            m_name = input("Enter Middle name : ")
            l_name = input("Enter Last name : ")
            father_name = input("Enter your father's name : ")
            age = input("Enter your age : ")
            gender = input("Select your gender M/F : ")
            mobile_no = input("Enter contact number : ")
            f_contact = input("Enter Father's contact no. : ")
            address = input("Enter your permanent address : ")
            nation = input("Enter nationality : ")
            pincode = input("Enter your pincode : ")
            city = input("Enter your city : ")
            state = input("Enter your state : ")
            email = input("Enter your email : ")
            branch = input("Enter branch : ")
            year = input("Enter year : ")
        else:  # Admin minimal info
            f_name = m_name = l_name = father_name = age = gender = mobile_no = f_contact = address = \
                nation = pincode = city = state = email = branch = year = ""

        with open(USER_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([user_name, pswd, f_name, m_name, l_name, father_name, age, gender,
                             mobile_no, f_contact, address, nation, pincode, city, state,
                             email, branch, year, role])
        print("Registration Successful")

    def user_exists(self, u_name):
        try:
            with open(USER_FILE, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == u_name:
                        return True
        except FileNotFoundError:
            return False
        return False

    def login(self):
        u_name = input("Enter username : ")
        pwd = input("Enter your password : ")
        try:
            with open(USER_FILE, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == u_name and row[1] == pwd:
                        print("Login Successful..")
                        self.logged_in = True
                        self.current_user = {
                            "user_name": row[0], "pswd": row[1], "f_name": row[2], "m_name": row[3], "l_name": row[4],
                            "father_name": row[5], "age": row[6], "gender": row[7], "mobile_no": row[8], 
                            "f_contact": row[9], "address": row[10], "nation": row[11], "pincode": row[12],
                            "city": row[13], "state": row[14], "email": row[15], "branch": row[16], "year": row[17],
                            "role": row[18]
                        }
                        self.role = row[18]
                        return
            print("Incorrect username or password")
        except FileNotFoundError:
            print("No users registered yet.")

    def show_profile(self):
        if self.logged_in:
            for k, v in self.current_user.items():
                print(f"{k.title()} :\t{v}")
        else:
            print("Please login first to view profile")

    def update_profile(self):
        if not self.logged_in:
            print("Please login first to update profile")
            return
        if self.role != "user":
            print("Admins cannot update profile details.")
            return
        self.current_user["email"] = input("Enter new email : ")
        self.current_user["branch"] = input("Enter new branch : ")
        self.current_user["year"] = input("Enter new year : ")
        self.current_user["mobile_no"] = input("Enter new contact number : ")
        self.current_user["f_name"] = input("Enter new name (first): ")
        self.update_user_csv()
        print("Profile updated successfully")

    def update_user_csv(self):
        users = []
        with open(USER_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == self.current_user["user_name"]:
                    row[15] = self.current_user["email"]
                    row[16] = self.current_user["branch"]
                    row[17] = self.current_user["year"]
                    row[2] = self.current_user["f_name"]
                    row[8] = self.current_user["mobile_no"]
                users.append(row)
        with open(USER_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(users)

    def logout(self):
        if self.logged_in:
            self.logged_in = False
            self.current_user = {}
            print("Logged Out Successfully")
        else:
            print("You are not logged in")

    def sessionterminate(self):
        print("Thank You !!!")
        exit()

    def is_admin(self):
        return self.role == 'admin'

def load_questions(category):
    file_map = {
        "DSA": "dsa_questions.json",
        "DBMS": "dbms_questions.json",
        "PYTHON": "python_questions.json"
    }
    file_name = file_map.get(category.upper())
    if not file_name:
        print("Invalid category.")
        return []
    try:
        with open(file_name, 'r') as f:
            questions = json.load(f)
            random.shuffle(questions)
            return questions[:min(len(questions), 10)]
    except FileNotFoundError:
        print(f"File {file_name} not found. Please check if file exists.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_name}. Check file format.")
    return []

def attempt_quiz(user, category):
    questions = load_questions(category)
    if not questions:
        return
    score = 0
    for idx, q in enumerate(questions):
        print(f"\nQ{idx+1}: {q['question']}")
        for opt in q['options']:
            print(f"- {opt}")
        ans = input("Enter your answer: ").strip()
        if ans.lower() == q['answer'].lower():
            score += 1
    print(f"\nYou scored {score} out of {len(questions)}")
    with open(SCORE_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user["user_name"], category, score, len(questions), datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def main():
    reg = Registration()
    print("Welcome To Shree Shyam Commerce Point Quiz App")

    while True:
        if not reg.logged_in:
            reply = input('''
Choose option:
    1. Registration
    2. Login
    3. Exit

Choose the option (1/2/3): ''').strip()
            if reply == '1':
                reg.register()
            elif reply == '2':
                reg.login()
            elif reply == '3':
                reg.sessionterminate()
            else:
                print("Please enter correct input!!")
        else:
            while reg.logged_in:
                reply = input('''
Logged in! Choose option:
    1. Show Profile
    2. Update Profile
    3. Attempt Quiz
    4. Logout
    5. Exit

Choose the option (1/2/3/4/5): ''').strip()
                if reply == '1':
                    reg.show_profile()
                elif reply == '2':
                    reg.update_profile()
                elif reply == '3':
                    print("Select category: DSA, DBMS, PYTHON")
                    cat = input("Enter category: ").strip()
                    attempt_quiz(reg.current_user, cat)
                elif reply == '4':
                    reg.logout()
                elif reply == '5':
                    reg.sessionterminate()
                else:
                    print("Please enter correct input!!")

if __name__ == "__main__":
    main()
