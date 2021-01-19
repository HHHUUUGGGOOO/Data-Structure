#########################################################################################
#                                       import                                          #                        
#########################################################################################


#########################################################################################
#                                        file                                           #                        
#########################################################################################


#########################################################################################
#                                      parameter                                        #                        
#########################################################################################
ascii_password, find_hash, output_line = [], [], []
hash_map = {}

#########################################################################################
#                                      function                                         #                        
#########################################################################################
# hash value function
def hash_function(left, right):
    h_value = (243*left + right) % 85767489
    return h_value


# dictionary function
def Dictionary_File(pass_word):
    global ascii_password, find_hash, output_line
    # String to ASCII, initialization
    for line in pass_word:
        temp = ""
        if (line != '\n'):
            for i in range(len(line)):
                if (line[i] != '\n'):
                    temp += str(ord(line[i]))
            ascii_password.append(temp)
    # Salt hash value (e.g. str.zfill(3))
    word = []
    output_seq = ""
    count = 0
    for line in pass_word:
        word.append(line)
    for i in range(len(ascii_password)):
        for j in range(1000):
            salt = str(j).zfill(3)
            combine = salt + ascii_password[i]
            temp = word[i].replace('\n', '') + ' ' + salt + ' ' + str(hash_function(int(combine[0:8]), int(combine[8:15]))) + '\n'
            output_seq = temp
            output_line.append(output_seq)
            output_seq = ""
            find_hash.append(str(hash_function(int(combine[0:8]), int(combine[8:15]))))
            hash_map[str(hash_function(int(combine[0:8]), int(combine[8:15])))] = salt
        # Check whether it's running
        count += 1
        # print(count)
    # Output file
    with open("Dictionary.txt", 'w') as result_file:
        result_file.writelines(output_line)


# result_pa2.txt
def Result_PA2(hash_value):
    global ascii_password, find_hash
    count = 1
    result = []
    for val in hash_value:
        # Column 1
        val = val.replace('\n', '')
        temp = val + ' '
        try:
            # print("val: ", val)
            # print("where: ", find_hash.index(val))
            index = find_hash.index(val)
            asci_all = output_line[index]
            asci = asci_all.split(' ', 2)[0].replace('\n', '')
            salt = asci_all.split(' ', 2)[2].replace('\n', '')
            # print("asci: ", asci)
            # print("salt: ", salt)
            # Column 2
            temp += asci
            temp += ' '
            # Column 3
            temp += hash_map[salt]
            temp += ' '
            # Column 4
            temp += str(index+1)
        except:
            # hash value not in the dictionary file
            # Column 2
            temp += "******"
            temp += ' '
            # Column 3
            temp += "***"
            temp += ' '
            # Column 4
            temp += "100000"
        temp += '\n'
        result.append(temp)
        temp = "" 
        # print(count)
        count += 1 
    # Output file
    with open("results_pa2.txt", 'w') as result_file:
        result_file.writelines(result)


# main function
def main():
    # Open password.txt
    file_name = input("Please enter the name of the password file: ")
    password_file = file_name
    f_pass = open(password_file)
    lines_pass = f_pass.readlines()
    # Create a dictionary file
    Dictionary_File(lines_pass)
    # Open list_pa2.txt
    mark = 0 # if enter a file name, mark == 1
    user_hash = input("Please enter a \"hash value\" or the \"txt file name\": ")
    if ("txt" in user_hash):
        list_file = open(user_hash)
        lines_list = list_file.readlines()
        Result_PA2(lines_list)
    else:
        Result_PA2([user_hash])
    # f_pass.close()
    if (mark == 1):
        mark = 0
        list_file.close()

#########################################################################################
#                                        main                                           #                        
#########################################################################################
if __name__ == '__main__':
	main()