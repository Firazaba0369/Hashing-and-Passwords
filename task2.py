import bcrypt
import nltk
import time
import numpy
import multiprocessing
from nltk.corpus import words
from nltk.data import find

def main():
    #download corpus if needed
    try:
        #Check if the corpus is already downloaded
        find('corpora/words.zip') 
    except LookupError:
        #Download only if not found
        nltk.download('words')  

    #get words between 6-10 char long
    valid_words = []
    for word in words.words():
        if 6<=len(word) <= 10:
            valid_words.append(word.lower())

    #make into set for faster lookup
    valid_words_set = set(valid_words)

    #get user_data
    user_data = parse_file("shadow.txt")

    #crack user password
    parallel_crack(user_data, valid_words)

#check a chunk of words against a given bcrypt hash
def check_password_chunk(chunk, hash_val):
    for word in chunk:
        if bcrypt.checkpw(word.encode(), hash_val.encode()):
            return word  # Return the cracked password if found
    return None

#crack passwords in parallel
def parallel_crack(user_data, valid_words, num_workers=multiprocessing.cpu_count()):
    cracked_passwords = {}
    for user, hash_val in user_data:
        print("Attempting to crack password for: " + user)
        #start logging time
        start_time = time.time()
        #seperate words into chunks
        word_chunks = []
        for chunk in numpy.array_split(list(valid_words), num_workers):
            word_chunks.append(chunk)
        
        #use multiprocessing to check passwords in parallel
        with multiprocessing.Pool(num_workers) as pool:
            results = pool.starmap(check_password_chunk, [(chunk, hash_val) for chunk in word_chunks]) 
        
        #check for password
        password = next((res for res in results if res is not None), None)

        #store password and print
        if password:
            time_taken = time.time() - start_time
            cracked_passwords[user] = (password, time_taken)
            print("Cracked " + user + "'s password: " + password + " in " + format(time_taken, ".2f") + " seconds")

    return cracked_passwords

# def crack_passwords(user_data, valid_words):
#     cracked_passwords = {}
#     for user, hash_val in user_data:
#         print("Attempting to crack password for: " + user)
#         #start logging time
#         start_time = time.time()
#         for word in valid_words:
#             #start checking passwords with words in nltk corpus
#             word_bytes = word.encode('utf-8')
#             if bcrypt.checkpw(word_bytes, hash_val.encode('utf-8')):
#                 #log time taken to crack password and print to terminal
#                 time_taken = time.time() - start_time
#                 cracked_passwords[user] = (word, time_taken)
#                 print("Cracked " + user + "'s password: " + word + " in " + format(time_taken, ".2f") + " seconds")
#                 #Stop checking once password is found
#                 break  
#     return cracked_passwords

#get the user and hash value
def parse_file(filename):
    user_data = []
    with open(filename, 'r') as file:
        for line in file:
            #get rid of whitespace
            data = line.strip()
            #get user and hash value and store together
            for i in range(len(data)):
                if data[i] == '$':
                    user = data[0:i-1]
                    hash_val = data[i:]
                    user_data.append((user, hash_val))
                    #print("User: " + str(user) + " Hash_val: " + str(hash_val))
                    break
    return user_data


if __name__ == "__main__":
    main()  