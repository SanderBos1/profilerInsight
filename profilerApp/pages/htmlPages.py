from flask import Blueprint, render_template
from ..userConnections import connectionForm
from ..userTables import tableForm

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
    form = connectionForm()
    return render_template('connectionPage.html', form=form)

@htmlPagesBP.route('/tables', methods=['GET'])
def tables():
    form = tableForm()
    return render_template('tables.html', form=form)


@htmlPagesBP.route('/settings', methods=['GET'])
def settings():

    return render_template('settingsPage.html')