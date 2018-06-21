
from flask import Blueprint, render_template, jsonify

from APP.models import Area, Facility
from utils import status_code

house_blueprint = Blueprint('house', __name__)


@house_blueprint.route('/myhouse/')
def my_house():
    return render_template('myhouse.html')


@house_blueprint.route('/newhouse/')
def new_house():
    """发布房源"""
    return  render_template('newhouse.html')


@house_blueprint.route('area_facility/')
def area_facility():
    """获取区位信息"""
    areas = Area.query.all()
    facilitys = Facility.query.all()
    areas_list = [area.to_dict() for area in areas]
    facilitys_list = [facility.to_dict() for facility in facilitys]
    return jsonify(code=status_code.OK, areas=areas_list,
                   facility=facilitys_list)