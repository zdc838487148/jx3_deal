from jx3_api.settings.dev import ACCESSKEYID, ACCESSSECRET
from jx3_api.settings.constant import SMS_EXPIRE_TIME
import random
from django.core.cache import cache


# 发送验证码
def sendmsg(phone):
    # 导入所需模块，再次之前我们都已经pip install好了的
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.request import CommonRequest

    # 这三个参数即 AccessKey ID， AccessKey Secret， 地区的id，关于地区id怎么获得我会贴在文章最下方
    client = AcsClient(ACCESSKEYID, ACCESSSECRET, "cn-shanghai")

    # 下面就是一些规定的配置，复制即可
    request = CommonRequest()
    request.set_accept_format("json")
    request.set_domain("dysmsapi.aliyuncs.com")
    request.set_method("POST")
    request.set_protocol_type("https")  # https | http
    request.set_version("2017-05-25")
    request.set_action_name("SendSms")

    # 配置地区id  地区id即为 cn_%s % (所在的地区名，应该是可以细分到市级的，如cn_hangzhou)
    request.add_query_param("RegionId", "cn-shanghai")
    # 配置要发送的手机号码
    request.add_query_param("PhoneNumbers", str(phone))
    # 配置你所设置的信息模板code,文章下方我会贴出来在哪边可以设置信息模板
    request.add_query_param("TemplateCode", "SMS_171117099")
    # 这个TemplateParam参数是给信息模板中的变量传值的，正常使用应该是后端获取验证码然后塞到这个参数中的

    code = ''
    for i in range(6):
        code += str(random.randint(0, 9))
    print("生成的code", code)
    request.add_query_param("TemplateParam", {"code": code})
    # cache.set(phone, code, SMS_EXPIRE_TIME)

    # 这是配置签名的
    request.add_query_param("SignName", "输诚一")

    # response = client.do_action(request)  # 调用发送短信方法
    # print(str(response, encoding='utf-8'))
    # if response:
    cache.set(phone, code)


