def str_to_digits(num_str):
    """Convert a number string to a list of digits."""
    return [int(char) for char in num_str if char.isdigit()]

def digits_to_str(digits):
    """Convert a list of digits back to a string."""
    return ''.join(str(d) for d in digits)

def add(num1, num2):
    """Add two arbitrary-precision integers represented as digit lists."""
    result = []
    carry = 0
    num1, num2 = num1[::-1], num2[::-1]  # Reverse for easier addition
    max_len = max(len(num1), len(num2))
    
    for i in range(max_len):
        digit1 = num1[i] if i < len(num1) else 0
        digit2 = num2[i] if i < len(num2) else 0
        total = digit1 + digit2 + carry
        result.append(total % 10)  # Keep the last digit
        carry = total // 10       # Carry the overflow
    
    if carry:
        result.append(carry)
    
    return result[::-1]  # Reverse back to normal order

def subtract(num1, num2):
    """Subtract num2 from num1 (num1 >= num2)."""
    result = []
    borrow = 0
    num1, num2 = num1[::-1], num2[::-1]
    
    for i in range(len(num1)):
        digit1 = num1[i]
        digit2 = num2[i] if i < len(num2) else 0
        total = digit1 - digit2 - borrow
        
        if total < 0:
            total += 10
            borrow = 1
        else:
            borrow = 0
        
        result.append(total)
    
    # Remove leading zeros
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    
    return result[::-1]

def multiply(num1, num2):
    """Multiply two arbitrary-precision integers represented as digit lists."""
    result = [0] * (len(num1) + len(num2))  # Result can be at most this long

    num1, num2 = num1[::-1], num2[::-1]  # Reverse for easier computation

    for i in range(len(num1)):
        carry = 0
        for j in range(len(num2)):
            total = result[i + j] + num1[i] * num2[j] + carry
            result[i + j] = total % 10
            carry = total // 10
        if carry:
            result[i + len(num2)] += carry

    # Remove leading zeros
    while len(result) > 1 and result[-1] == 0:
        result.pop()

    return result[::-1]  # Reverse back to normal order

def strip_leading_zeros(digits):
    """Remove leading zeros from a list of digits."""
    while len(digits) > 1 and digits[0] == 0:
        digits.pop(0)
    return digits

def compare(num1, num2):
    """Compare two digit lists. Returns -1, 0, or 1."""
    if len(num1) != len(num2):
        return -1 if len(num1) < len(num2) else 1
    for d1, d2 in zip(num1, num2):
        if d1 != d2:
            return -1 if d1 < d2 else 1
    return 0

def divide(num1, num2):
    """Divide num1 by num2. Returns (quotient, remainder)."""
    if num2 == [0]:
        raise ValueError("Division by zero is not allowed.")

    quotient = []
    remainder = []

    for digit in num1:
        remainder.append(digit)
        remainder = strip_leading_zeros(remainder)
        count = 0

        while compare(remainder, num2) >= 0:  # remainder >= num2
            remainder = subtract(remainder, num2)
            count += 1

        quotient.append(count)

    quotient = strip_leading_zeros(quotient)
    remainder = strip_leading_zeros(remainder)

    return quotient, remainder

def modulo(num1, num2):
    """Compute num1 % num2."""
    _, remainder = divide(num1, num2)
    return remainder

def power(base, exponent):
    """Compute base^exponent."""
    result = [1]  # Start with 1
    for _ in range(int(digits_to_str(exponent))):  # Convert exponent to integer
        result = multiply(result, base)
    return result
def factorial(num):
    """Compute the factorial of a number represented as a digit list."""
    if compare(num, [0]) == 0:  # 0! = 1
        return [1]
    
    result = [1]
    current = [1]

    while compare(current, num) <= 0:  # current <= num
        result = multiply(result, current)
        current = add(current, [1])  # Increment current by 1

    return result

def log10(num):
    """Compute the integer part of log10 for an arbitrary-precision number."""
    if compare(num, [0]) <= 0:
        raise ValueError("Logarithm is undefined for non-positive numbers.")

    return [len(num) - 1]

def to_base(num, base):
    """Convert a base-10 number (digit list) to another base."""
    if compare(num, [0]) == 0:
        return [0]

    result = []
    while compare(num, [0]) > 0:
        _, remainder = divide(num, [base])
        result.append(remainder[0])
        num = divide(num, [base])[0]  # Update num as the quotient

    return result[::-1]  # Reverse the result

def from_base(digits, base):
    """Convert a number in another base back to base-10."""
    result = [0]
    for digit in digits:
        result = multiply(result, [base])
        result = add(result, [digit])

    return result


def repl():
    print("Arbitrary Precision Integer Calculator")
    print("Supported operations: +, -, *, /, %, ^, !, log10, base")
    print("Type 'exit' to quit.")

    while True:
        expr = input("> ")
        if expr.lower() == "exit":
            break
        try:
            if "!" in expr:  # Factorial
                num = str_to_digits(expr.replace("!", "").strip())
                result = factorial(num)
            elif "log10" in expr:  # Logarithm
                num = str_to_digits(expr.replace("log10", "").strip())
                result = log10(num)
            elif "base" in expr:  # Base conversion
                parts = expr.split()
                num = str_to_digits(parts[1])
                base = int(parts[2])
                result = to_base(num, base)
                print("Result in base", base, ":", digits_to_str(result))
                continue
            else:  # Regular operations
                num1, op, num2 = expr.split()
                num1 = str_to_digits(num1)
                num2 = str_to_digits(num2)

                if op == "+":
                    result = add(num1, num2)
                elif op == "-":
                    result = subtract(num1, num2)
                elif op == "*":
                    result = multiply(num1, num2)
                elif op == "/":
                    result, _ = divide(num1, num2)
                elif op == "%":
                    result = modulo(num1, num2)
                elif op == "^":
                    result = power(num1, num2)
                else:
                    print("Unsupported operation.")
                    continue

            print(digits_to_str(result))
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    repl()
