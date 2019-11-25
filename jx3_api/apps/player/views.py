from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import JsonResponse
from user.models import UserInfo
from . import models
from django.db import transaction
from article import models as article_models
from django.core.cache import cache



class SetPlayerInfo(View):
    def get(self, request):
        return render(request, 'playerinfo.html', locals())

    def post(self, request):
        data = request.POST
        print(data)
        is_keep_play = int(data.get("is_keep_play"))
        player_obj = models.PlayerInfo.objects.filter(user=request.user).first()
        if not is_keep_play:
            if player_obj:
                player_obj.update(is_keep_play=0)
            return redirect(reverse('setplayerinfo'))
        else:
            age = data.get('age')
            sex = data.get('sex')
            voice_obj = request.FILES.get("voice")
            price = data.get('price')
            work_time = data.get("work_time")
            is_skill = int(data.get("is_skill"))
            is_humor = int(data.get("is_humor"))
            accouter_num = data.get("accouter_num")
            body = data.get("body")
            addr = data.get('addr')
            contact_way = data.get("contact_way")

            if not player_obj:
                player_obj = models.PlayerInfo(is_keep_play=1,
                                               age=age,
                                               sex=sex,
                                               price=price,
                                               work_time=work_time,
                                               is_skill=is_skill,
                                               is_humor=is_humor,
                                               accouter_num=accouter_num,
                                               body=body,
                                               addr=addr,
                                               contact_way=contact_way,
                                               user=request.user)
                player_obj.save()
            else:
                player = models.PlayerInfo.objects.filter(user=request.user)
                print('wjw')
                player.update(is_keep_play=1,
                              age=age,
                              sex=sex,
                              price=price,
                              work_time=work_time,
                              is_skill=is_skill,
                              is_humor=is_humor,
                              accouter_num=accouter_num,
                              body=body,
                              addr=addr,
                              contact_way=contact_way)

            if voice_obj:
                print('保存录音')
                player_obj = models.PlayerInfo.objects.filter(user=request.user).first()
                player_obj.voice = voice_obj
                player_obj.save()

            return redirect(reverse('setplayerinfo'))


class PlayerView(View):
    def get(self, request):
        print('run playview')
        player_list = models.PlayerInfo.objects.filter(is_keep_play=1)
        return render(request, 'player_view.html', locals())



class PlayerDetail(View):
    def get(self, request, player_id):
        player_obj = models.PlayerInfo.objects.filter(pk=player_id).first()
        comment_list = models.PlayerComment.objects.filter(player_id=player_id)

        return render(request, 'player_detail.html', locals())


class PlayerComment(View):
    def post(self, request):
        back_dic = {'code': 1, 'msg': ''}
        # 获取前端发送过来的数据
        player_id = request.POST.get("player_id")
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        # 1.校验当前用户是否登录
        if request.user.is_authenticated:
            with transaction.atomic():
                # 在文章表中将普通的评论字段加1
                # models.Article.objects.filter(pk=article_id).update(comment_num=F('comment_num') + 1)
                # 在去评论表存储真正的数据
                models.PlayerComment.objects.create(user=request.user, player_id=player_id, content=content,
                                              parent_id=parent_id)
            back_dic['msg'] = '评论成功'
        else:
            back_dic['code'] = 0
            back_dic['msg'] = '请先登录'
        return JsonResponse(back_dic)




import time
from jx3_api.libs.alipay.payinit import ali_init
class AliPayAPIView(View):
    def post(self, request, *args, **kwargs):
        subject = request.POST.get('subject')
        money = request.POST.get('money')

        # 1）初始化alipay
        alipay = ali_init()

        # 2）生成订单号
        out_trade_no = "x2" + str(time.time())

        # 3）生成支付链接
        query_params = alipay.direct_pay(
            subject=subject,  # 商品名描述
            out_trade_no="x2"+out_trade_no,  # 商户订单号
            total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
        )
        pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

        # 4）将订单存入数据库 - 非完成订单
        cache.set(out_trade_no, False, 300)


        return JsonResponse({
            "out_trade_no": out_trade_no,
            "pay_url": pay_url
        })


class AliPayBackViewSet(View):
    def post(self, request, *args, **kwargs):
        # 初始化alipay
        alipay = ali_init()

        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        print(post_dict)

        sign = post_dict.pop('sign', None)
        # 通过调用alipay的verify方法去二次认证
        status = alipay.verify(post_dict, sign)

        if status:
            # 修改订单状态
            pass
        return JsonResponse('验证成功')

    def get(self, request, *args, **kwargs):
        # 初始化alipay
        alipay = ali_init()

        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('GET验证', status)
        if status:
            # 获取订单状态，显示给用户
            return JsonResponse('支付成功')