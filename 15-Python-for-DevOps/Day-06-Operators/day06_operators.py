#!/usr/bin/env python3

print("--- Task 1: Arithmetic Operators ---")
a = 20
b = 6

print(f"Addition ({a} + {b}):", a + b)
print(f"Subtraction ({a} - {b}):", a - b)
print(f"Multiplication ({a} * {b}):", a * b)
print(f"Division ({a} / {b}):", a / b)
print(f"Floor Division ({a} // {b}):", a // b)
print(f"Modulus ({a} % {b}):", a % b)
print(f"Exponentiation ({a} ** {b}):", a ** b)


print("\n--- Task 2: Comparison Operators ---")
print(f"{a} < {b}:", a < b)
print(f"{a} > {b}:", a > b)
print(f"{a} <= {b}:", a <= b)
print(f"{a} >= {b}:", a >= b)
print(f"{a} == {b}:", a == b)
print(f"{a} != {b}:", a != b)


print("\n--- Task 3: Logical Operators ---")
x = True
y = False

print(f"{x} and {y}:", x and y)
print(f"{x} or {y}:", x or y)
print(f"not {x}:", not x)


print("\n--- Task 4: Assignment Operators ---")
total = 10
print("Initial total:", total)

total += 5  # 15
print("After += 5:", total)

total -= 3  # 12
print("After -= 3:", total)

total *= 2  # 24
print("After *= 2:", total)

total /= 4  # 6.0
print("After /= 4:", total)


print("\n--- Task 5: Bitwise Operators (Advanced) ---")
# 5 = 0101, 3 = 0011
num1 = 5
num2 = 3
print(f"{num1} & {num2}:", num1 & num2)  # AND -> 0001 (1)
print(f"{num1} | {num2}:", num1 | num2)  # OR  -> 0111 (7)
print(f"{num1} ^ {num2}:", num1 ^ num2)  # XOR -> 0110 (6)


print("\n--- Task 6: Identity and Membership Operators ---")
my_list = ["docker", "jenkins", "ansible", "terraform"]

print("Is 'jenkins' in the list?:", "jenkins" in my_list)
print("Is 'kubernetes' NOT in the list?:", "kubernetes" not in my_list)

# Identity Check
a_list = [1, 2, 3]
b_list = [1, 2, 3]
c_list = a_list

print("\nIdentity Check:")
print(f"a_list == b_list (Values Equal?):", a_list == b_list)
print(f"a_list is b_list (Same Memory Object?):", a_list is b_list)
print(f"a_list is c_list (Same Memory Object?):", a_list is c_list)


print("\n--- Task 7: DevOps Decision Engine Example ---")
disk_usage = 85
cpu_usage = 70
server_status = "active"

if disk_usage >= 80 or cpu_usage >= 90:
    if server_status == "active":
        print("[ALERT] Server is active but resources are critically high! Triggering Auto-Scaling...")
else:
    print("[OK] Server resources are normal.")
