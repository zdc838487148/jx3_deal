from .pay import AliPay
import os

def ali_init():
    # o_你自己的应用ID
    app_id = "2016100100640484"
    # 支付宝收到用户的支付，会向商户发两个请求，一个get请求，一个post请求
    # o_你自己公网服务器处理支付宝回调的POST请求，验证订单
    notify_url = "http://127.0.0.1:7899/player/aliback/"
    # # o_你自己公网服务器处理支付宝回调的GET请求，将订单结果展现给用户
    return_url = "http://127.0.0.1:7899/player/aliback/"
    # o_你自己的私钥
    alipay_private_key_path = r'/python/code/jx3_api/jx3_api/libs/keys/alipay_private_2048.txt'
    # o_你自己的公钥
    alipay_public_key_path = r'/python/code/jx3_api/jx3_api/libs/keys/alipay_public_2048.txt'

    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=alipay_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    return alipay