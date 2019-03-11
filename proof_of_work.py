from random import randint
from hashlib import sha256

previous_hash = "b9b9ee9ffc95fa4956b63b6043a99d0a8f04e0e52e687fc1958d3c6dff885f01"


# loopカウント
cnt = 1

# nonce値
nonce = str(randint(0, 1000000))

# 前ブロックのハッシュ値とnonce値の結合した文字列
header = sha256(f'{previous_hash}{nonce}'.encode()).hexdigest()
while header[:4] != "0000":
    text = 'loop:{}, header:{}, header[:4]:{}, nonce:{}\n'
    print(text.format(cnt, header, header[:4], nonce))

    nonce = str(randint(0, 1000000))
    header = sha256(f'{previous_hash}{nonce}'.encode()).hexdigest()
    cnt += 1

text = 'loop:{}, header:{}, header[:4]:{}, nonce:{}'
print(text.format(cnt, header, header[:4], nonce))
