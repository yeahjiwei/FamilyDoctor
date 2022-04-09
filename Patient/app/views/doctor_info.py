from flask import request, render_template, redirect, url_for, flash, session, Blueprint, Response


doctor_info_blueprint = Blueprint('doctor_info', __name__)
