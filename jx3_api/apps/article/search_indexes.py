from haystack import indexes
from .models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    #类名必须为需要检索的Model_name+Index，这里需要检索Article，所以创建ArticleIndex
    text = indexes.CharField(document=True, use_template=True)#创建一个text字段
    #其它字段
    desc = indexes.CharField(model_attr='desc')
    content = indexes.CharField(model_attr='content')

    def get_model(self):#重载get_model方法，必须要有！
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()