from django import forms
from django.forms import widgets
from user import models
import re


class Register(forms.Form):
    username = forms.CharField(max_length=16,
                               min_length=6,
                               label="登陆账号",
                               widget=widgets.TextInput(attrs={"class": "form-control"}),
                               error_messages={
                                   "max_length": "账号最大长度为16位",
                                   "min_length": "账号最小长度为6位",
                                   "required": "账号不能为空",
                               })

    jx3_name = forms.CharField(max_length=8,
                               min_length=2,
                               label="昵称",
                               widget=widgets.TextInput(attrs={"class": "form-control"}),
                               error_messages={
                                   "max_length": "昵称最大长度为6位",
                                   "min_length": "昵称最小长度为2位",
                                   "required": "昵称不能为空",
                               })

    # 验证账号存在合法性的局部钩子
    def clean_username(self):
        username = self.cleaned_data.get("username")
        print(123, username)

        user = models.UserInfo.objects.filter(username=username).first()
        if user:
            self.add_error("username", "此账号已被注册")
        return username

    # 验证昵称存在合法性的局部钩子
    def clean_jx3_name(self):
        jx3_name = self.cleaned_data.get("jx3_name")
        user = models.UserInfo.objects.filter(jx3_name=jx3_name)
        if user:
            self.add_error("jx3_name", "此昵称已被使用")
        return jx3_name

    password = forms.CharField(max_length=16,
                               min_length=6,
                               label="登陆密码",
                               widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                               error_messages={
                                   "max_length": "密码最大长度为16位",
                                   "min_length": "密码最小长度为6位",
                                   "required": "密码不能为空",
                               })

    re_password = forms.CharField(max_length=16,
                                  min_length=6,
                                  label="确认密码",
                                  widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                                  error_messages={
                                      "max_length": "密码最大长度为16位",
                                      "min_length": "密码最小长度为6位",
                                      "required": "密码不能为空",
                                  })

    # 校验两次密码是否一致的全局钩子
    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if password != re_password:
            self.add_error("re_password", "两次密码不一致")
        return self.cleaned_data


class RegisterPhone(forms.Form):
    phone = forms.CharField(max_length=16,
                            min_length=6,
                            label="手机号",
                            widget=widgets.TextInput(attrs={"class": "form-control"}),
                            error_messages={
                                "max_length": "手机号必须为11位",
                                "min_length": "手机号必须为11位",
                                "required": "手机号不能为空",
                            })

    jx3_name = forms.CharField(max_length=8,
                               min_length=2,
                               label="昵称",
                               widget=widgets.TextInput(attrs={"class": "form-control"}),
                               error_messages={
                                   "max_length": "昵称最大长度为6位",
                                   "min_length": "昵称最小长度为2位",
                                   "required": "昵称不能为空",
                               })

    # 验证手机号存在合法性的局部钩子
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        print('账号钩子：', phone)
        user = models.UserInfo.objects.filter(phone=phone)
        if user:
            self.add_error("phone", "此手机号已经注册过了")
            # return phone
        if not re.match(r'^1[3-9]\d{9}$', phone):
            self.add_error("phone", "手机号有误")
        return phone



    # 验证昵称存在合法性的局部钩子
    def clean_jx3_name(self):
        jx3_name = self.cleaned_data.get("jx3_name")
        user = models.UserInfo.objects.filter(jx3_name=jx3_name)
        if user:
            self.add_error("jx3_name", "此昵称已被使用")
        return jx3_name

    # 校验两次密码是否一致的全局钩子
    def clean(self):
        password = self.cleaned_data.get("username")
        re_password = self.cleaned_data.get("re_password")
        if password != re_password:
            self.add_error("re_password", "两次密码不一致")
        return self.cleaned_data

