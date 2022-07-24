import csv
import datetime
import dateutil.parser


def analyze(log_csv) -> list:
    output_list = []
    row_detected = []
    # stopsign_detected = False
    for i, row in enumerate(log_csv):
        # init
        if i == 0:
            last_stopped_time = dateutil.parser.parse(row['timestamp'])
            last_detected_time = dateutil.parser.parse(row['timestamp'])
            stopsign_detected = False
            print(last_stopped_time)
        current_time = dateutil.parser.parse(row['timestamp'])
        # stopsign detect
        if row['detect'] == 'tomare':  # and (current_time - last_stopped_time > datetime.timedelta(seconds=5)or stopsign_detected):
            if current_time - last_detected_time < datetime.timedelta(seconds=1) and float(
                    row['sidewalk_bdbox_width']) > 0.07:  #
                last_detected_time = dateutil.parser.parse(row['timestamp'])
                if not (stopsign_detected):
                    stopsign_detected = True
                    enter_time = dateutil.parser.parse(row['timestamp'])
                    last_detected_time = dateutil.parser.parse(row['timestamp'])
                    row_detected = [str(row['timestamp']), int(2), float(row['lat']), float(row['lon'])]
                    print('detected', current_time, 'size:', row['sidewalk_bdbox_width'])
            last_detected_time = current_time

        if stopsign_detected:
            # stopped
            if float(row['speed']) < 0.7:
                print('stopped', current_time, row['speed'])
                last_stopped_time = dateutil.parser.parse(row['timestamp'])
                stopsign_detected = False
            # offence!
            elif current_time - enter_time > datetime.timedelta(seconds=15):
                print('offence!')
                output_list.append({'timestamp': row_detected[0], 'type': row_detected[1], 'lat': row_detected[2],
                                    'lon': row_detected[3]})
                stopsign_detected = False
    if stopsign_detected:
        output_list.append({'timestamp': row_detected[0], 'type': row_detected[1], 'lat': row_detected[2], 'lon': row_detected[3]})
    return output_list
