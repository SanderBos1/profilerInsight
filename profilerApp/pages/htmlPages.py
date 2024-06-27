from flask import Blueprint, render_template
from ..userConnections import connectionForm
from ..userTables import tableForm
from ..userConnections import dbConncetions
from ..userTables import userTable


htmlPagesBP = Blueprint(
    "htmlPagesBP",
    __name__,
)

@htmlPagesBP.route('/home', methods=['GET'])
def home():

    return render_template('home.html')

@htmlPagesBP.route('/profiler', methods=['GET'])
def profiler():
    tableList = userTable.query.with_entities(userTable.uniqueTableName).all()
    tableList = [str(connection_id[0]) for connection_id in tableList]
    return render_template('profilerPage.html', tables=tableList)

@htmlPagesBP.route('/connections', methods=['GET'])
def connections():
    form = connectionForm()
    return render_template('connectionPage.html', form=form)

@htmlPagesBP.route('/tables', methods=['GET'])
def tables():
    form = tableForm()
    connectionList = dbConncetions.query.with_entities(dbConncetions.connectionId).all()
    connectionList = [str(connection_id[0]) for connection_id in connectionList]
    form.connectionId.choices = connectionList
    return render_template('tables.html', form=form)


@htmlPagesBP.route('/settings', methods=['GET'])
def settings():

    return render_template('settingsPage.html')