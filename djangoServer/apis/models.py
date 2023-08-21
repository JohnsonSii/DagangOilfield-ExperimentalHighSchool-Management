from django.db import models

# Create your models here.

import uuid


class User(models.Model):
    # 唯一主键
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # 用户名密码
    username = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=50, null=True)

    # 用户权限 -> 0: 普通用户 1: 管理员
    role = models.IntegerField(null=True)

    # 个人信息
    name = models.CharField(max_length=10, null=True)
    qq = models.CharField(max_length=20, null=True)
    school = models.CharField(max_length=20, null=True)
    
    # 图片存储地址
    image_url = models.CharField(max_length=100, null=True)

    # 审核状态 -> 2 未审核 0: 待审核 1: 已审核
    passed = models.IntegerField(null=True)

    # 创建与更新日期
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
