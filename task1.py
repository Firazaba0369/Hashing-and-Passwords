from hashlib import sha256

def hamming_distance(str1, str2): # calculate hamming distance
    count = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            count += 1
    return count

def find_hamming_one_string(original_string):
    hex_string = sha256(original_string.encode()).hexdigest()  # 
    for i in range(len(hex_string)):
        new_string = list(hex_string)
        if new_string[i] == '0':
            new_string[i] = '1'
        else:
            new_string[i] == '0'
        new_string = ''.join(new_string)
    
        if hamming_distance(hex_string, new_string) == 1:
            

            return new_string

#task 1a
input1 = "randomgibberish" # arbitrary inputs
input2 = "jkl12jkledaS/.d"
input3 = "even more random gibby"
input4 = "hello"

encrypted1 = sha256(input1.encode()).hexdigest()
encrypted2 = sha256(input2.encode()).hexdigest()
encrypted3 = sha256(input3.encode()).hexdigest()
encrypted4 = sha256(input4.encode()).hexdigest()

print("This is input1 in hex", encrypted1)
print("This is input2 in hex", encrypted2)
print("This is input3 in hex", encrypted3)

#task 1b
print(encrypted4)
d = find_hamming_one_string("hello")
print(d)