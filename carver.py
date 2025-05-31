import sys
import re

if len(sys.argv) != 2:
    print("Usage: python carver.py <filename>")
    exit(1)

filename = sys.argv[1]

try:
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    first_0x = content.find('0x')
    if first_0x == -1:
        print("No shellcode found")
    else:
        content = content[first_0x:]
    
    last_0x = content.rfind('0x')
    if last_0x == -1:
        print("No '0x' found, keeping all content")
    else:
        content = content[:last_0x + 4]
    
    content = content.replace('0x', '')
    content = content.replace(',', '')
    
    hex_only = re.sub(r'[^0-9A-Fa-f]', '', content)
    hex_encode = hex_only.encode()


    base_name = filename.rsplit('.', 1)[0]
    output_filename = f"{base_name}.bin"

    with open(output_filename, 'wb') as f:
        f.write(hex_encode)

        print(f"Shellcode saved to: {output_filename}")
        print(f"Total bytes written: {len(hex_encode)}")
    
except FileNotFoundError:
    print(f"Error: File '{filename}' not found")
except Exception as e:
    print(f"Error: {e}")
