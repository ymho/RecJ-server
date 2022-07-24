import csv
import numpy as np
import collections


def abs2D(x, y):
    return (x ** 2 + y ** 2) ** 0.5


def analyze(data) -> list:
    # タスク4の処理を行う関数
    frame = ''
    timestamp = []
    ay, az, lat, lon = [], [], [], []
    for i, row in enumerate(data):
        # print(i, row)
        t = row['timestamp']
        if (t != frame):
            frame = t
            timestamp.append(row['timestamp'])
            ay.append(float(row['ay']))
            az.append(float(row['az']))
            lat.append(row['lat'])
            lon.append(row['lon'])

    num = len(timestamp)
    aveacc = np.ndarray(num - 10)
    ay = np.array(ay)
    az = np.array(az)
    for i in range(num - 10):
        y = ay[i:i + 10].mean()
        z = az[i:i + 10].mean()
        aveacc[i] = abs2D(y, z)

    mean = aveacc.mean()
    std = np.std(aveacc)
    dev = [(i - mean) / std for i in aveacc]

    # print(aveacc)
    # print("dev")
    # print(dev)

    # 判断に使うフレーム数
    obsFrame = 10
    # 危険フレームと判断する加速度の閾値
    dangerAcc = 2
    # 危険フレームがいくつ観測されれば危険運転と判断するか
    dangerFrame = 5

    danger = []
    devs = np.array(dev)
    i = 0
    while i < num - 10:
        # 直近obsFrame(0.5秒くらい)でdangerFrame以上加速度がdangerAccより大きければ危険と判断
        if np.count_nonzero(devs[i - obsFrame:i] > dangerAcc) >= dangerFrame:
            # 危険運転を記録
            t = int(i + 10 - obsFrame / 2)
            danger.append({'timestamp': timestamp[t], 'type': 3, 'lat': lat[t], 'lon': lon[t]})
            # 同じイベントを複数回検知しないようリセット(＆時間を進める?)
            # que.clear()
            i += 30
        i += 1

    return danger
