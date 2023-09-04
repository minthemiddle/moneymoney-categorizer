import datetime
import plistlib
import subprocess

# Export transactions from MoneyMoney.
from_date = datetime.date.today() + datetime.timedelta(days=-3000)
script = f'tell application "MoneyMoney" to export transactions from date "{from_date.strftime("%Y-%m-%d")}" as "plist"'
command = ['osascript', '-e', script]
with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pipe:
    result = pipe.communicate()
    if result[1]:
        print(f'Could not export transactions from MoneyMoney. {result[1].decode().strip()}')
        exit(1)

# Parse XML property list.
try:
    plist = plistlib.loads(result[0])
except plistlib.InvalidFileException as exception:
    print(f'Could not parse XML property list. {repr(exception)}')
    exit(1)

# Print transaction details if any exist.
for transaction in plist['transactions']:
    if transaction['booked']:
        details = []
        if 'amount' in transaction:
            details.append(f"Amount: {transaction['amount']}")
        if 'name' in transaction:
            details.append(f"{transaction['name']}")
        if 'bookingText' in transaction:
            details.append(f"{transaction['bookingText']}")
        if details:
            print(', '.join(details))
