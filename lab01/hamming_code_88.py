import random

def encode_str_to_bin_seq(data):
    str = data.encode('cp1251')
    bin_seq = ''
    for letter_code in str:
        bin_letter = f'{letter_code:08b}'
        bin_seq += bin_letter
    
    return bin_seq

def create_words_hamming(bins_seq,flag=0): 
    len_of_word = 88
    q = False
    hamming_words = []          
    hamming_words_error = []
    stat_err = []
    for i in range(int(len(bins_seq) / len_of_word) + 1):
        word_88 = bins_seq[i*len_of_word:i*len_of_word+len_of_word]
        
        
        if len(word_88) == 0:
            break 
        while len(word_88) < len_of_word:
            word_88 = word_88 + '0'
 
        hamming_word = create_code_hamming(word_88)
        hamming_words.append(hamming_word)
        if not flag == 0:
            if flag == 1: 
                
                isError = random.choice([True, False])
                if (isError):
                    pos_error = random.randint(1,51) - 1 
                    error = 1 if int(hamming_word[pos_error]) == 0 else 0 
                    hamming_word = hamming_word[:pos_error] + f'{error}' + hamming_word[pos_error+1:]
                    stat_err.append(pos_error) 
                else:
                    stat_err.append(-1) 
                hamming_words_error.append(hamming_word)
            elif flag == 2: 
                isError = random.choice([True, False])
                if (isError):
                    pos_error = random.randint(1,51) - 1 
                    error = 1 if int(hamming_word[pos_error]) == 0 else 0 
                    hamming_word = hamming_word[:pos_error] + f'{error}' + hamming_word[pos_error+1:]

                    pos_error_2 = random.randint(1,51) - 1 
                    while pos_error_2 == pos_error:
                        pos_error_2 = random.randint(1,51) - 1 
                    error = 1 if int(hamming_word[pos_error_2]) == 0 else 0
                    hamming_word = hamming_word[:pos_error_2] + f'{error}' + hamming_word[pos_error_2+1:] 

                    stat_err.append(-2) 
                else:
                    stat_err.append(-1)
                hamming_words_error.append(hamming_word)
            elif flag == 3: 
                amount_of_errors = random.choice([0,1,2])
                if amount_of_errors == 0:
                    stat_err.append(-1) 
                elif amount_of_errors == 1:
                    pos_error = random.randint(1,51) - 1 
                    error = 1 if int(hamming_word[pos_error]) == 0 else 0 
                    hamming_word = hamming_word[:pos_error] + f'{error}' + hamming_word[pos_error+1:]
                    stat_err.append(pos_error) 
                elif amount_of_errors == 2:
                    pos_error = random.randint(1,51) - 1 
                    error = 1 if int(hamming_word[pos_error]) == 0 else 0 
                    hamming_word = hamming_word[:pos_error] + f'{error}' + hamming_word[pos_error+1:]
                    pos_error_2 = random.randint(1,51) - 1 
                    while pos_error_2 == pos_error:
                        pos_error_2 = random.randint(1,51) - 1 
                    error = 1 if int(hamming_word[pos_error_2]) == 0 else 0
                    hamming_word = hamming_word[:pos_error_2] + f'{error}' + hamming_word[pos_error_2+1:] 
                    stat_err.append(-2) 
                
                hamming_words_error.append(hamming_word)
        else:
            
            hamming_words_error.append(hamming_word)
            stat_err.append(-1)
    return hamming_words_error, stat_err

def create_code_hamming(word):
    
    code_hamming = '0'
    left = 0
    
    for i in range(1,7):
        right = left + 2**i -1
        print(len(word[left:right]))
        code_hamming = code_hamming + '0' + word[left:right]
        left = right
    
    for i in range(7):
        r = 2**i
        xor = 0
        for k in range(r-1, len(code_hamming), 2*r): 
            
            for j in range(0, r):  
                

                xor = xor ^ int(code_hamming[k+j])
                if (k+j >= len(code_hamming)-1):
                    break
        
        code_hamming = code_hamming[:r-1] + f'{xor}' + code_hamming[r-1+1:]       
    
    support_xor = 0
    for bit in code_hamming:
        support_xor = support_xor ^ int(bit)
    code_hamming = code_hamming + f'{support_xor}'
    
    return code_hamming

def decode_code_hamming(code_hamming):
    left = 0
    support_bits = []
    
    for i in range(7):
        r = 2**i
        xor = 0
        for k in range(r-1, len(code_hamming)-1, 2*r): 
            for j in range(0, r):   
                xor = xor ^ int(code_hamming[k+j])
                if (k+j >= len(code_hamming)-1-1):
                    break
        support_bits.append(int(xor))
    
    C = 0 
    for idx, bit in enumerate(support_bits):
        if bit > 0:
            C += 2**idx
    
    P = 0
    support_xor = 0
    isDoubleError = False
    oneError = -1 

    
    for bit in code_hamming:
        P = P ^ int(bit)
    
    if C == 0 and P == 0:
        
        temp = '0'
        
    if C != 0 and P == 1:
        
        
        pos_error = C - 1 
        correct = 1 if int(code_hamming[pos_error]) == 0 else 0
        code_hamming = code_hamming[:pos_error] + f'{correct}' + code_hamming[pos_error+1:] 
        oneError = pos_error
        
    if C != 0 and P == 0:
        
        isDoubleError = True

        
    if C == 0 and P == 1:
        
        pos_error = 96 - 1
        oneError = pos_error
        
        
    
    
    if not (isDoubleError):
        code_hamming = code_hamming[:len(code_hamming)-1] 
        for i in reversed(range(7)):
            r = 2**i
            code_hamming = code_hamming[:r - 1] + code_hamming[r:]
        bit_seq = code_hamming
        return bit_seq, oneError
    else:
        return [], -2 

    

def getSeqOfBitsAndDecode(words, statistic):
    result_str = ''
    isPrevError = False
    halfLetter = ''
    fullLetter = ''
    
    
    for idx, word in enumerate(words):
        
        result, pos = decode_code_hamming(word) 
        statistic.append(pos)        

        
        if idx == len(words) - 1:
            if len(result) > 0:
                if (idx % 2) == 0: 
                    for i in range(11):
                        symbol = result[i*8:i*8+8]
                        if int(symbol) == 0:
                           
                            
                            last_letters = result[:i*8]
                            result_str = result_str + decode_bin_seq_to_str(last_letters)
                            break
                        if i == 10:
                            last_letters = result[:i*8+8]
                            result_str = result_str + decode_bin_seq_to_str(last_letters)
                            break
                    break
            else:
                result_str = result_str + '???????????'
                break
                

        if len(result) > 0:
        
            eleven_letters = result[:88]
            result_str = result_str + decode_bin_seq_to_str(eleven_letters)
        else:  
            isPrevError = True
            result_str = result_str + '?????????????'
    
    return result_str, statistic

def decode_bin_seq_to_str(bins_seq):
    if (len(bins_seq) % 8 != 0):
        print('Error. Not equal amount of bits')
    
    list_of_bins = [bins_seq[i*8:i*8+8] for i in range(int(len(bins_seq) / 8))]
    hex_str = b''

    for bin_letter in list_of_bins:
        letter_code = int(bin_letter, 2)    
        hex_code = hex(letter_code)[2:] 
        if letter_code <= 15:
            hex_code =  '0' + hex_code 
        hex_str += bytes.fromhex(hex_code) 
    str = hex_str.decode('cp1251', 'replace')
    return str

def process(str):
    
    bins = encode_str_to_bin_seq(str)
    
    words, err = create_words_hamming(bins, 2)
    
    
    
    stat_err = []
    str_res, stat_err = getSeqOfBitsAndDecode(words, stat_err)
    
    

    oneError = 0
    twoError = 0
    noError = 0
    for idx, err in enumerate(stat_err):
        if err >= 0:
            oneError +=1
            
        elif err == -1:
            noError +=1
            
        elif err == -2:
            twoError +=1
            
    
    total_word = oneError+noError+twoError
    
    print(str_res)
    print(f'Total match : {str == str_res}')
    

def main():
    str = 'ДумаюR2456rwafaw235235124afs' 
    process(str)
    return 0

if __name__ == "__main__":
    main()