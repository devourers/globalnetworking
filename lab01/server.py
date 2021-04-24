import socket
import select
import hamming_code_88 as HC

def printStat(stat_err):
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
    print(f'Common statistic: \nTotal hamming words count : {total_word} \nWithout errors: {noError}/{total_word} \nOne error: {oneError}/{total_word} \nTwo erros: {twoError}/{total_word}')
    with open('./server_result.txt', 'w') as wf:
        wf.write(f'Common statistic: \nTotal word count : {total_word} \nWithout errors: {noError}/{total_word} \nOne error: {oneError}/{total_word} \nTwo erros: {twoError}/{total_word}')

def process(response):
    words = [response[i*96:i*96+96].decode('cp1251') for i in range(int(len(response)/96))]
    stat_err = []
    str_res, stat_err = HC.getSeqOfBitsAndDecode(words, stat_err)
    printStat(stat_err)
    with open('./server_result.txt', 'a') as wf:
        wf.write('\nRESULT TEXT:\n')
        wf.write(str_res)
    print(str_res)
    statistic_str = ''
    sep = ';'
    for i in stat_err:
        statistic_str = statistic_str + str(i) + sep
    
    bins = HC.encode_str_to_bin_seq(statistic_str)
    words, temp = HC.create_words_hamming(bins, 0) 
    message = ''
    for word in words:
        message = message + word
    message = message.encode('cp1251')
    return message


def main():
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(1)
    count = 0
    while True: 
        conn, addr = sock.accept()
        count += 1
        print('connected:', addr)
        response = b''
        while True:
            conn.settimeout(2.0) 
            try:
                data = conn.recv(1024)
            except:
                break 
            response = response + data
                
        req = process(response)   

        conn.send(req)

        conn.close()
        if count == 5: 
            break 

    return 0

if __name__ == "__main__":
    main()