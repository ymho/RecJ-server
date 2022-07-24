from unicodedata import name
from flask import Flask, g, request, render_template, jsonify, send_file
from analyzer import analyze_task1
from analyzer import analyze_task2
from analyzer import analyze_task3
from analyzer import analyze_task4

import csv
import folium
from folium.plugins import HeatMap


def generate_html(alz1, alz2, alz3, alz4, uuid) -> bool:
    # TODO HTMLの生成から保存まで
    # 地図生成
    f = folium.Figure(width=1000, height=500)
    # 初期表示の中心の座標を指定して地図を作成する。
    center_lat = 35.02642729499398
    center_lon = 135.78080831152516
    m = folium.Map([center_lat, center_lon], zoom_start=15).add_to(f)

    folium.raster_layers.TileLayer(
        tiles="https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png",
        attr="地理院タイル",
        fmt="image/png",
        tms=False,
        overlay=True,
        control=True,
        opacity=0.7,
    ).add_to(m)

    HeatMap(
        [
            [float(x['lat']), float(x['lon']), float(x["speed"])]
            for x in alz1
        ],
        radius=8,
        blur=7,
        gradient={"0.3": "white", "0.7": "green", "1.0": "darkgreen"},
    ).add_to(m)

    HeatMap(
        [
            [float(x['lat']), float(x['lon'])]
            for x in alz2
        ],
        radius=8,
        blur=7,
        gradient={"0.3": "white", "0.7": "blue", "1.0": "darkblue"},
    ).add_to(m)

    HeatMap(
        [
            [float(x['lat']), float(x['lon'])]
            for x in alz3
        ],
        radius=8,
        blur=7,
        gradient={"0.3": "white", "0.7": "red", "1.0": "pink"},
    ).add_to(m)

    HeatMap(
        [
            [float(x['lat']), float(x['lon'])]
            for x in alz4
        ],
        radius=8,
        blur=7,
        gradient={"0.3": "white", "0.7": "orange", "1.0": "darkred"},
    ).add_to(m)

    with open("/app/templates/" + uuid + "_map.html", "wb") as f:
        m.save(f, close_file=False)

    bad_drive_hantei_count = 0
    if len(alz1) != 0:
        bad_drive_hantei_count += 1
    if len(alz2) != 0:
        bad_drive_hantei_count += 1
    if len(alz3) != 0:
        bad_drive_hantei_count += 1
    if len(alz4) != 0:
        bad_drive_hantei_count += 1

    bad_drive_hantei = "A"
    if bad_drive_hantei_count == 1:
        bad_drive_hantei = "B"
    elif bad_drive_hantei_count == 2:
        bad_drive_hantei = "C"
    elif bad_drive_hantei_count == 3:
        bad_drive_hantei = "D"
    elif bad_drive_hantei_count == 4:
        bad_drive_hantei = "E"

    html = render_template('sample.html', url_for="/map/"+uuid, uuid=uuid, score=bad_drive_hantei, hitogomi=len(alz1), tomare=len(alz2),
                           sidewalk=len(alz3), kyu=len(alz4))

    if html is None:
        return False
    else:
        with open("/app/templates/" + uuid + ".html", mode='w', encoding="utf-8") as f:
            f.write(str(html))
        return True


app = Flask(__name__)


@app.route('/<uuid>/', methods=["GET", "POST"])
def scoring(uuid):
    if request.method == "POST":
        with open("/app/csv/"+uuid+".csv", mode='w') as f:
            csv_file = request.get_data().decode('utf-8')
            if csv_file is None:
                return jsonify({'message': 'csvの読み取りに失敗しました'}), 400
            f.write(csv_file)
        with open("/app/csv/"+uuid+".csv", mode='r') as g:
            alz1 = analyze_task1.analyze(csv.DictReader(g))
        with open("/app/csv/" + uuid + ".csv", mode='r') as g:
            alz2 = analyze_task2.analyze(csv.DictReader(g))
        with open("/app/csv/" + uuid + ".csv", mode='r') as g:
            alz3 = analyze_task3.analyze(csv.DictReader(g))
        with open("/app/csv/" + uuid + ".csv", mode='r') as g:
            alz4 = analyze_task4.analyze(csv.DictReader(g))

        if generate_html(alz1, alz2, alz3, alz4, uuid):
            return jsonify({'message': 'HTMLを出力しました'}), 200
        else:
            return jsonify({'message': 'HTMLを出力に失敗しました'}), 500

    elif request.method == "GET":
        return render_template(uuid+".html")

    else:
        return jsonify({'message': '許可されていない操作です'}), 400


@app.route('/map/<uuid>/', methods=["GET"])
def heatmap(uuid):
    return render_template(uuid + "_map.html")


@app.route('/sample/', methods=["GET"])
def sample():
    return jsonify({'message': 'サンプルです'}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
