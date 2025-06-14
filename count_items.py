import re

def count_items(text):
    total = 0
    # Updated pattern to catch numbers followed by "items" or "item" with or without colons
    pattern = r'[:\s](\d+)\s+items?'
    
    # Find all numbers followed by "item" or "items"
    matches = re.findall(pattern, text)
    
    # Convert to integers and sum
    numbers = [int(n) for n in matches]
    total = sum(numbers)
    
    # Print all entries for verification
    print("\nAll entries found:")
    lines = text.split('\n')
    current_name = ""
    for line in lines:
        if line.strip().startswith('@'):
            current_name = line.strip()
        elif 'item' in line:
            count = re.search(r'(\d+)\s+items?', line)
            if count:
                print(f"{current_name}: {count.group(1)} items")
    
    # Print counts in descending order
    print("\nCounts found (sorted):")
    for n in sorted(numbers, reverse=True):
        print(f"{n}", end=" ")
    
    print(f"\n\nTotal number of items: {total}")
    print(f"Number of entries with counts: {len(numbers)}")
    
    # Print missing or problematic entries
    print("\nEntries that might need attention:")
    for line in lines:
        if 'item' in line and not re.search(pattern, line):
            print(f"Possible missing count: {line.strip()}")

# Your pasted text here
text = """@Alexandre Bonny
 3 items
@Alvin Ho
: 8 items
@Amol Tulaskar
: 2 items
@Amrut Nandedkar
: 2 items
@Anchal Khatwani
: 1 item
@Anuj Kumar
:2 items
@Asger Winther Jørgensen
 2 items
@Aviv Moyal
: 2 items
@Boris Rabinovich
: 1 item
@Brian Sherman
: 2 items
@Chandrasekhar Gopal
: 1 item
@Chris Willetts
: 3 items
@Michael B. Lee
 
@Sonia Singh
: 1 item
@Emma Utstrand
: 1 item
@Greg Keech
 Lazarev: 2 items
@Gunjan Choudhary
: 4 items
@Guy Segev
: 1 item
@Håkon Dissen
: 1 item
@Itzhak Yacobi
 2 items
@Jack Li
: 2 items
@John Elston
: 3 items
@Jun Khit Tang
: 1 item
@Kenny Ong
: 1 item
@Kevin Stueber
: 2 items
@Lakshmi Narayana Nindra Krishna
: 1 item
@Wenqi Liang
 Shao: 1 item
@Lijuan Zhu
: 1 item
@Logan Xiao
: 2 items
@Mark King
: 2 items
@Michal Hradil
 1 item
@Mike Snelling
 1 item
@Daniel Wardziński
 14 items
@Nicola Nardino
: 1 item
@Osman Can Ornek
: 1 item
@Osman Can Ornek
 Shashi Sahu: 1 item
@Prabhat Kumar
: 1 item
@Praveen Subramanian
: 2 items
@Rahul Parekh
: 1 item
@Raj Milan Samal
: 4 items
@Sapna Bhargava
: 5 items
@Sarah Gibson
: 1 item
@Saurabh Misra
 Aggarwal: 1 item
@Kiran Sebastian
 Casallas: 4 items
@Seema Jaisinghani
: 1 item
@Sekhar Jajimoggala
: 2 items
@Shankar Kumar
 2 items
@Sriram Dayanand
: 1 item
@Stanley Diji
: 1 item
@Suhasis Saha
: 1 item
@Sunmit Girme
: 2 items
@Tomasz Kudlinski
 Wojdyla: 1 item
@Tony Zhang
: 1 item
@Trevor Sweeney
: 2 items
@Uday Didigam
: 4 items
@Uma Veerappan
: 1 item
@Vera Rumyantseva
: 6 items
@Yohai Zvuloon
: 2 items"""

count_items(text) 