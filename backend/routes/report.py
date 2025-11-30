from flask import Blueprint
report_bp = Blueprint("report", __name__)

@report_bp.route('/gen_report/<int:p_id>')
def csv_init(p_id):
    from celeryApp import export_csv
    export_csv(p_id)
    return {'message':"Export Initiated, please wait for mail!"}