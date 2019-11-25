import xadmin
from . import models


# 注册
xadmin.site.register(models.Blog)
xadmin.site.register(models.Article)
xadmin.site.register(models.Tag)
xadmin.site.register(models.Category)
xadmin.site.register(models.Tag2Article)
xadmin.site.register(models.UpOrDown)
xadmin.site.register(models.Comment)