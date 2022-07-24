def analyze(data) -> dict:
    # タスク1の処理を行う関数
    comparison_time = ''
    result = []
    detect_hitogomi_count = 0
    frame_count = 0
    comparison_speed = 0.0
    lat = 0.0
    lon = 0.0
    for i, row in enumerate(data):
        if i == 0:
            comparison_time = row['timestamp'].split('.')[0]
            comparison_speed = row['speed']
            lat = row['lat']
            lon = row['lon']

        if comparison_time == row['timestamp'].split('.')[0]:
            frame_count += 1
        else:
            detect_person_num = float(detect_hitogomi_count) / float(frame_count)

            if detect_person_num >= 0.4 and float(comparison_speed) >= 3.0:
                result.append(
                    {
                        "timestamp": comparison_time,
                        "lat": lat,
                        "lon": lon,
                        "speed": comparison_speed
                    }
                )
            comparison_time = row['timestamp'].split('.')[0]
            comparison_speed = row['speed']
            lat = row['lat']
            lon = row['lon']
            detect_hitogomi_count = 0
            frame_count = 1

        if row['detect'] == 'hitogomi' and float(row['confidence']) >= 0.8:
            detect_hitogomi_count += 1

    print(result)

    return result