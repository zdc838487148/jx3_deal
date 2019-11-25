import xadmin
from xadmin import views
from . import models

class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "剑三园"  # 设置站点标题
    site_footer = "输诚一"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)

# 注册
# xadmin.site.register(models.UserInfo)
