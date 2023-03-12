from flask import render_template, Blueprint
from Patient.app.views.index import login_required


page_blueprint = Blueprint('page', __name__)


@page_blueprint.route('/page')
@login_required
def page():
    return render_template("page.html")
