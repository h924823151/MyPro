# main : 处理所有的业务

# 将自己加入到Blueprint中
from flask import Blueprint

main = Blueprint('main',__name__)

from . import views