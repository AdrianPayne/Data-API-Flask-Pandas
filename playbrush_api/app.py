import io
from flask import Flask, render_template, request

from brush_stats import week_stats

app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def week_stats_view():
    if request.method == "GET":
        return render_template('main.html')

    elif request.method == "POST":

        rawdata_csv = request.files["rawdata"]
        groups_csv = request.files["groupsdata"]

        rawdata_csv = io.StringIO(rawdata_csv.stream.read().decode("UTF8"), newline=None)
        groups_csv = io.StringIO(groups_csv.stream.read().decode("UTF8"), newline=None)

        try:
            user_stats, group_stats = week_stats(rawdata_csv, groups_csv)
            error_message = None
        except:
            user_stats= None
            group_stats = None
            error_message='ERROR WITH CSV FILES. Upload them again'

        return render_template('main.html', user_stats=user_stats, group_stats=group_stats, error_message=error_message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
