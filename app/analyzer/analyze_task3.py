import csv
import datetime
import dateutil.parser

def analyze(data) -> dict:
    # 歩道禁止区域の緯度経度
    lat1 = 35.025184
    lat2 = 35.025359
    lon1 = 135.772380
    lon2 = 135.781947
    result = []
    first_detect_flag = False
    judge_range_flag = False

    for i, row in enumerate(data):
        lat = row['lat']
        lon = row['lon']

        current_time = dateutil.parser.parse(row['timestamp'])

        if first_detect_flag == False:
            last_detect_time = current_time

        if judge_range_flag == False:
            first_time = current_time
            judge_range_flag = True

        if lat1 < float(lat) < lat2 and lon1 < float(lon) < lon2:

            if row['detect'] == 'sidewalk' and float(row['confidence']) > 0.998:  # 座標で絞る　アプリで実験して確認
                if float(row['sidewalk_bdbox_min']) > 0.30 and (
                        float(row['sidewalk_bdbox_min']) + float(row['sidewalk_bdbox_width'])) < 0.70:
                    last_detect_time = current_time
                    first_detect_flag = True
                    judge_range_flag = False
                    # print('detected')
            else:
                if current_time - last_detect_time >= datetime.timedelta(
                        seconds=5) or current_time - first_time >= datetime.timedelta(seconds=5):
                    # print('genten')  # 違反件数をカウントしていく
                    result.append({'timestamp': row['timestamp'], 'lat': lat, 'lon': lon})
                    first_detect_flag = False
                    judge_range_flag = False

        else:
            first_detect_flag = False
            judge_range_flag = False

    # print(result)

    return result


# if __name__ == "__main__":
#     with open("/content/drive/My Drive/10_PIA/20220723_record/sample1.csv") as f:
#         data = csv.DictReader(f)
#         analyze(data)
