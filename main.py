import sleek
import sys

if len(sys.argv) != 2:
    print("Usage: sleek *.slk")
    sys.exit(1)

file_name = sys.argv[1]

if not file_name.endswith('.slk'):
    print(f"Need a *.slk file, not *.{file_name.split('.')[-1]}")
    sys.exit(1)

try:
    result = sleek.run_file(file_name)
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
