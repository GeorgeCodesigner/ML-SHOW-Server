from django.db import models
from mongoengine import *
# Create your models here.
class User(Document):
    meta = {
        # 数据库中显示的document名字
        'collection': 'user'
    }
    _id = SequenceField(required=True, primary_key=True)
    name = StringField()
    age = IntField()
    sex = StringField()

    # 可以定义查询集
    @queryset_manager
    def show_newest(doc_cls, queryset):
        # 通过poem_id降序显示
        return queryset.order_by('-_id')