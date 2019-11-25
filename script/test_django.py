import os


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jx3_api.settings.dev')
    import django
    django.setup()
    # 以下写django的测试代码
    from django.conf import settings
    print(os.path.join(settings.BASE_DIR, 'alipay_private_2048.txt'))
    # print(settings.BASE_DIR)
    # from django.shortcuts import reverse
    # print(reverse('home'))
    # from django.core.cache import cache
    # code = cache.get("code")
    # print(666, code)
    # from article import models as article_models
    # article_list = article_models.Article.objects.all().order_by('look_num')
    # print(article_list)

    # path = os.path.join(settings.BASE_DIR, 'media', 'article_img')
    # print(os.path.exists(path))



if __name__ == '__main__':
    main()
