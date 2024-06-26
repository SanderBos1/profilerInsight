from flask import Blueprint, render_template


htmlPagesBP = Blueprint(
    "htmlPagesBP",
    __name__,
)

@htmlPagesBP.route('/home', methods=['GET'])
def home():

    return render_template('home.html')

@htmlPagesBP.route('/profiler', methods=['GET'])
def profiler():

    return render_template('profilerPage.html')

@htmlPagesBP.route('/connections', methods=['GET'])
def connections():

    return render_template('connectionPage.html')

@htmlPagesBP.route('/settings', methods=['GET'])
def settings():

    return render_template('settingsPage.html')