"""Validate bank transactions stored one per line in a text file.

Input format: Type,Amount (for example: Deposit,5000 or Withdraw,2000)
"""

import math
import sys


OPENING_BALANCE = 10000
MAX_TRANSACTION_AMOUNT = 100000
VALID_TYPES = {"deposit", "withdraw"}
VALID_OUTPUT_FILE = "valid_transactions.txt"


def validate_transaction(transaction_type, amount_text, balance):
    """Return (is_valid, reason, updated_balance, amount).

    A valid deposit or withdrawal is the only kind of transaction that changes
    the balance. The returned amount is None if it could not be parsed.
    """
    transaction_type = transaction_type.strip()
    normalized_type = transaction_type.lower()

    if normalized_type not in VALID_TYPES:
        return False, "unknown type {!r}".format(transaction_type), balance, None

    try:
        amount = float(amount_text.strip())
    except (ValueError, AttributeError):
        return (
            False,
            "amount {!r} is not a number".format(amount_text.strip()),
            balance,
            None,
        )

    if not math.isfinite(amount):
        return False, "amount must be a finite number", balance, amount

    if amount <= 0:
        return False, "amount must be positive", balance, amount

    if amount > MAX_TRANSACTION_AMOUNT:
        return (
            False,
            "exceeds limit of {}".format(MAX_TRANSACTION_AMOUNT),
            balance,
            amount,
        )

    if normalized_type == "withdraw":
        if amount > balance:
            return False, "insufficient balance", balance, amount
        return True, "", balance - amount, amount

    return True, "", balance + amount, amount


def format_money(amount):
    """Display whole-number amounts without a decimal part."""
    if amount.is_integer():
        return str(int(amount))
    return "{:.2f}".format(amount)


def process_transactions(input_filename):
    """Read, validate, report, and save the valid transactions."""
    balance = float(OPENING_BALANCE)
    valid_count = 0
    invalid_count = 0
    valid_lines = []

    try:
        with open(input_filename, "r", encoding="utf-8") as transaction_file:
            lines = transaction_file.readlines()
    except FileNotFoundError:
        print("Error: file {!r} was not found.".format(input_filename))
        print("Create the file or provide its path when running this program.")
        return
    except OSError as error:
        print("Error: could not read {!r}: {}".format(input_filename, error))
        return

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()

        if not line:
            invalid_count += 1
            print("Line {}: Invalid – line is empty.".format(line_number))
            continue

        fields = line.split(",")
        if len(fields) != 2:
            invalid_count += 1
            print(
                "Line {}: Invalid – expected Type,Amount.".format(line_number)
            )
            continue

        transaction_type, amount_text = fields
        is_valid, reason, new_balance, amount = validate_transaction(
            transaction_type, amount_text, balance
        )

        if is_valid:
            balance = new_balance
            valid_count += 1
            valid_lines.append("{},{}\n".format(transaction_type.strip(), amount_text.strip()))
            print(
                "Line {}: Valid  |  Balance: {}".format(
                    line_number, format_money(balance)
                )
            )
        else:
            invalid_count += 1
            print("Line {}: Invalid – {}.".format(line_number, reason))

    try:
        with open(VALID_OUTPUT_FILE, "w", encoding="utf-8") as valid_file:
            valid_file.writelines(valid_lines)
    except OSError as error:
        print("Error: could not save valid transactions: {}".format(error))
        return

    print("\nValid: {}  |  Invalid: {}  |  Final balance: {}".format(
        valid_count, invalid_count, format_money(balance)
    ))
    print("Valid transactions saved to {!r}.".format(VALID_OUTPUT_FILE))


def main():
    """Use the filename supplied on the command line, or transactions.txt."""
    input_filename = sys.argv[1] if len(sys.argv) > 1 else "transactions.txt"
    process_transactions(input_filename)


if __name__ == "__main__":
    main()
