import datetime
import plistlib
import subprocess

script = f'tell application "MoneyMoney" to export categories'
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
for category in plist:
    print(f'{category["uuid"]}, {category["name"]}')
 