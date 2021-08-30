character = input("Enter any lowercase alaphabet")
if character >= "a" and character <= "z":
    ord_value = ord(character)
    difference = ord_value - 32
    chr_value = chr(difference)
    print (chr_value)
else:
    print ("Invalid Character")