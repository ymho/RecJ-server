from flask import Flask, g, request, render_template, jsonify

from analyzer import analyze_task1
from analyzer import analyze_task2
from analyzer import analyze_task3
from analyzer import analyze_task4


def generate_html(alz1, alz2, alz3, alz4) -> None:
    # TODO HTMLの生成から保存まで
    return


app = Flask(__name__)


@app.route('/<uuid>/', methods=['GET', 'POST'])
def scoring(uuid):
    if request.method == "POST":
        # csv形式のテキストを取得する
        raw_csv = request.get_data()
        log_csv = raw_csv  # TODO raw_csvはテキストなのでpythonで扱いやすい形に変えておく

        # raw_csvを解析して結果を保存
        alz1 = analyze_task1.analyze(log_csv)
        alz2 = analyze_task2.analyze(log_csv)
        alz3 = analyze_task3.analyze(log_csv)
        alz4 = analyze_task4.analyze(log_csv)

        # HTMLを生成してresults内に保存して終了
        generate_html(alz1, alz2, alz3, alz4)

    elif request.method == "GET":
        # HTMLを返す
        return render_template('results/'+uuid+'html')

    else:
        return jsonify({'message': '許可されていない操作です'}), 500


@app.route('/sample/', methods=['GET'])
def sample():
    return render_template('results/sample.html')


if __name__ == "__main__":
    app.run()
