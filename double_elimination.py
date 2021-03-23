# double_elimination

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

    original_proper = [1,2,3] # その大会形式で取得できる順位
    x = 1
    dummy = True
    while len(original_proper) < n:
        if dummy:
            original_proper.extend([2**x + 2**(x-1) + 1]*(2**(x-1)))
            x += 1
        else:
            original_proper.extend([2**x + 1]*(2**(x-1)))
        dummy = not dummy
    original_proper = sorted(list(set(original_proper)))

    for _ in range(N):
        players_wt = random.sample(range(1,n+1), k=n) # 勝者側トーナメントのプレイヤーの実力順位
        players_lt = [] # 敗者側トーナメントのプレイヤーの実力順位
        abs_error = [0]*n

        while len(players_wt) + len(players_lt) > 2:
            if len(players_wt) >= 2: # 1位2位は確定しているのでGFはシミュする必要なし
                tmp_wt = []
                tmp_lt = []
                for i in range(0,len(players_wt),2):
                    tmp_wt.append(min(players_wt[i], players_wt[i+1]))
                    tmp_lt.append(max(players_wt[i], players_wt[i+1]))
                players_wt = tmp_wt.copy()
                random.shuffle(tmp_lt) # 敗者側トーナメントへの参戦箇所をシャッフル
                if players_lt: # 敗者側トーナメントに残っているプレイヤーと新たに負けたプレイヤーを合わせる
                    x = min(len(players_lt), len(tmp_lt))
                    tmp = [None]*(x*2)
                    tmp[::2] = players_lt[:x].copy()
                    tmp[1::2] = tmp_lt[:x].copy()
                    tmp.extend(players_lt[x:])
                    tmp.extend(tmp_lt[x:])
                    players_lt = tmp.copy()
                else:
                    players_lt = tmp_lt.copy()

            if len(players_lt) >= 2:
                tmp_lt = []
                rank = len(players_wt) + len(players_lt)//2 + 1 # この時点で敗退したプレイヤーの順位
                for i in range(0,len(players_lt),2):
                    try:
                        tmp_lt.append(min(players_lt[i], players_lt[i+1]))
                        if players_lt[i] > players_lt[i+1]:
                            cv = closest_values(original_proper, players_lt[i])
                            abs_error[players_lt[i]-1] += min(abs(cv[x]-rank) for x in range(len(cv)))
                        else:
                            cv = closest_values(original_proper, players_lt[i+1])
                            abs_error[players_lt[i+1]-1] += min(abs(cv[x]-rank) for x in range(len(cv)))
                    except IndexError: # 敗者側トーナメントに奇数人いる場合
                        tmp_lt.append(players_lt[i])
                players_lt = tmp_lt.copy()
        
        for i in range(n):
            MSE[i] += abs_error[i]/(N*(i+1))

    print(n, sum(MSE), 100*sum(MSE)/n)
    for x in MSE:
        print(x)

