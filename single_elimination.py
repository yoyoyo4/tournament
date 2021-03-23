# single_elimination

import random
import bisect

# ソート済みのリストlの中から値vに最も近い(2つ以下の)値のリストを返す
def closest_values(l,v):
    output = [float("inf")]
    x = bisect.bisect_left(l,v)
    for i in [x-1, x, x+1]:
        try:
            if abs(output[0]-v) > abs(l[i]-v):
                output = [l[i]]
            elif abs(output[0]-v) == abs(l[i]-v):
                output.append(l[i])
                break
        except IndexError:
            continue
    return output

N = 100

for exponent in range(9, 10):
    n = 2**exponent # プレイヤー数
    MSE = [0]*n

    original_proper = [1] # その大会形式で取得できる順位
    x = 0
    while len(original_proper) < n:
        original_proper.extend([2**x+1]*(2**x))
        x += 1
    original_proper = sorted(list(set(original_proper)))

    for _ in range(N):
        players = random.sample(range(1,n+1), k=n) # 各プレイヤーの実力順位
        abs_error = [0]*n

        while len(players) >= 2:
            tmp = []
            rank = 2**(len(players).bit_length()-2) + 1 # この時点で敗退したプレイヤーの順位
            for i in range(0,len(players),2):
                tmp.append(min(players[i], players[i+1]))
                if players[i] > players[i+1]:
                    cv = closest_values(original_proper, players[i])
                    abs_error[players[i]-1] += min(abs(cv[x]-rank) for x in range(len(cv)))
                else:
                    cv = closest_values(original_proper, players[i+1])
                    abs_error[players[i+1]-1] += min(abs(cv[x]-rank) for x in range(len(cv)))
            players = tmp.copy()
        
        for i in range(n):
            MSE[i] += abs_error[i]/(N*(i+1))

    # print(n, sum(MSE), 100*sum(MSE)/n)
    for m in MSE:
        print(m)