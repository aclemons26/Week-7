
import json
import re
from typing import List, Dict, Any, Optional

def get_valid_employee_id() -> str:
    """Required: numeric, 1-7 digits."""
    while True:
        emp_id = input("Enter Employee ID (1-7 digits): ").strip()
        if emp_id.isdigit() and 1 <= len(emp_id) <= 7:
            return emp_id
        print("Invalid ID. Must be a number with 7 or fewer digits.")

def get_valid_name() -> str:
    """Required: primarily letters, spaces, apostrophe, and hyphen allowed."""
    while True:
        name = input("Enter Employee Name: ").strip()
        if name and re.fullmatch(r"[A-Za-z\s'-]+", name):
            return name
        print("Invalid name. Use only letters, spaces, apostrophes ('), and hyphens (-).")

def get_valid_email() -> str:
    """Required: primarily alphanumeric. Forbidden: !\"#$%^&*()=+,< >/?;:[]{}\\"""
    forbidden = set('!"#$%^&*()=+,< >/?;:[]{}\\')
    while True:
        email = input("Enter Employee Email: ").strip()
        if email and not any(c in forbidden for c in email) and re.fullmatch(r"[A-Za-z0-9@._-]+", email):
            return email
        print("Invalid email. Cannot contain: ! \" # $ % ^ & * ( ) = + , < > / ? ; : [ ] { } \\")

def get_valid_address() -> Optional[str]:
    """Optional. If provided, primarily alphanumeric. Forbidden: !\"'@ $%^&*_= +<>?;:[]{}\\"""
    forbidden = set("!\"'@$%^&*_= +<>?;:[]{}\\")
    while True:
        address = input("Enter Employee Address (press Enter to skip): ").strip()
        if not address:
            return None
        if not any(c in forbidden for c in address) and re.fullmatch(r"[A-Za-z0-9\s.,#-]+", address):
            return address
        print("Invalid address. Cannot contain: ! \" ' @ $ % ^ & * _ = + < > ? ; : [ ] { } \\")

def get_valid_salary() -> float:
    """Required: float between 18 and 27."""
    while True:
        try:
            salary = float(input("Enter Employee Salary (between 18 and 27): "))
            if 18 <= salary <= 27:
                return salary
            print("Salary must be between 18 and 27.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def gather_employee_data() -> List[Dict[str, Any]]:
    """Collect employees until the user chooses to stop. Returns list of dicts."""
    employees: List[Dict[str, Any]] = []
    print("=== Employee Data Entry ===")
    print("Enter 'no' or 'done' when finished adding employees.\n")

    while True:
        cont = input("Add another employee? (yes/no): ").strip().lower()
        if cont in ("no", "n", "done", "exit", "quit"):
            break

        employee = {
            "id": get_valid_employee_id(),
            "name": get_valid_name(),
            "email": get_valid_email(),
            "address": get_valid_address(),
            "salary": get_valid_salary()
        }
        employees.append(employee)
        print(f"Added employee: {employee['name']}\n")

    return employees

# --- Comprehension functions ---

def get_names(employees: List[Dict[str, Any]]) -> List[str]:
    """List comprehension: extract all employee names."""
    return [emp["name"] for emp in employees]

def get_high_earners(employees: List[Dict[str, Any]], threshold: float = 22.0) -> List[Dict[str, Any]]:
    """List comprehension: employees earning above the threshold."""
    return [emp for emp in employees if emp["salary"] > threshold]

def get_email_domain_map(employees: List[Dict[str, Any]]) -> Dict[str, str]:
    """Dictionary comprehension: map employee name -> email domain."""
    return {
        emp["name"]: emp["email"].split("@")[-1] if "@" in emp["email"] else "unknown"
        for emp in employees
    }

def get_employees_with_address(employees: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """List comprehension: only employees who provided an address."""
    return [emp for emp in employees if emp.get("address")]

def write_employees_to_json(employees: List[Dict[str, Any]], filename: str = "employees.json") -> None:
    """Write the list of employee dictionaries to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(employees, f, indent=4)
        print(f"\nWrote {len(employees)} employee record(s) to '{filename}'.")
    except OSError as e:
        print(f"Error writing JSON file: {e}")

def display_results(employees: List[Dict[str, Any]]) -> None:
    """Show results produced by the comprehension functions."""
    if not employees:
        print("No employees entered.")
        return

    print("\n=== Results (via comprehensions) ===")
    print("All names:", get_names(employees))
    print("High earners (> 22):", [e["name"] for e in get_high_earners(employees)])
    print("Email domains:", get_email_domain_map(employees))
    with_addr = get_employees_with_address(employees)
    print(f"Employees with address ({len(with_addr)}):", [e["name"] for e in with_addr])

def main() -> None:
    employees = gather_employee_data()
    display_results(employees)
    if employees:
        write_employees_to_json(employees)
    print("\nDone.")

if __name__ == "__main__":
    main()
