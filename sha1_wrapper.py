import hashlib
import random
import string
import logging
import matplotlib.pyplot as plt

def sha1_wrapper(str, num_bit):
    msg = hashlib.sha1()
    msg.update(str.encode())
    digest = int(msg.hexdigest(), 16)
    shift = msg.digest_size * 8 - num_bit
    shift = max(0, shift)
    return hex(digest >> shift)


def get_random_str(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length)) 


def collision_attack(num_bit):
    hash_dict = {}
    str = get_random_str(10)
    digest = sha1_wrapper(str, num_bit)
    while digest not in hash_dict:
        hash_dict[digest] = str
        str = get_random_str(10)
        digest = sha1_wrapper(str, num_bit)
    return digest, str, hash_dict[digest], len(hash_dict)


def preimage_attack(num_bit):
    str = get_random_str(10)
    digest = sha1_wrapper(str, num_bit)
    str2 = get_random_str(10)
    digest2 = sha1_wrapper(str2, num_bit)
    attempt = 1
    while digest != digest2:
        str2 = get_random_str(10)
        digest2 = sha1_wrapper(str2, num_bit)
        attempt += 1
    return digest, str, str2, attempt
    


def log_collision_attack(num_bit):
    logging.info(f'Collision Attack for bit size {num_bit}')
    total_attempt = 0
    num_sample = 50
    for i in range(num_sample):
        digest, str1, str2, num_attempt = collision_attack(num_bit)
        total_attempt += num_attempt
        logging.info(f'digest:{digest}, str1:{str1}, str2:{str2}, num_attempt:{num_attempt}')
    average_attempt = total_attempt / num_sample
    logging.info(f'Average Attempt:{average_attempt}')
    logging.info(f'Expected Attempt: {pow(2, num_bit/2)} (2^(n/2))')
    return average_attempt


def log_preimage_attack(num_bit):
    logging.info(f'Preimage Attack for bit size {num_bit}')
    total_attempt = 0
    num_sample = 50
    for i in range(num_sample):
        digest, str1, str2, num_attempt = preimage_attack(num_bit)
        total_attempt += num_attempt
        logging.info(f'digest:{digest}, str1:{str1}, str2:{str2}, num_attempt:{num_attempt}')
    average_attempt = total_attempt / num_sample
    logging.info(f'Average Attempt:{average_attempt}')
    logging.info(f'Expected Attempt: {pow(2, num_bit)} (2^n)')
    return average_attempt


def log_attacks():
    logging.basicConfig(filename='collision.log', level=logging.INFO)
    plt.figure()
    plt.title('Collision Attacks')
    plt.xlabel('number of bits')
    plt.ylabel('number of attempts')
    x = [8, 10, 16, 20, 24]
    y = [pow(2, n/2) for n in x]
    plt.plot(x, y, label='expected')
    y = []
    for num in x:
        y.append(log_collision_attack(num))
    plt.plot(x, y, label='actual')
    plt.legend()
    plt.savefig('collision.png')

    plt.figure()
    plt.title('Preimage Attacks')
    plt.xlabel('number of bits')
    plt.ylabel('number of attempts')
    x = [8, 10, 16]
    y = [pow(2, n) for n in x]
    plt.plot(x, y, label='expected')
    y = []
    for num in x:
        y.append(log_preimage_attack(num))
    plt.plot(x, y, label='actual')
    plt.legend()
    plt.savefig('preimage.png')
    
 
log_attacks()