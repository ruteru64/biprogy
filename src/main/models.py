from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.TextField("名前", max_length = 150, blank = True)
    email = models.EmailField("Eメールアドレス", blank = True)
    is_active = models.BooleanField(
        "ユーザーステータス",
        default=True,
    )
    password = models.CharField("パスワード", max_length = 15)

    def __str__(self):
        return self.name

class Partner(models.Model):
    user_id =  models.IntegerField() # int ユーザのid
    name = models.TextField() # TextField 営業先の名前？
    belongs = models.TextField() # TextField 営業先会社名

    def __str__(self):  # partnerのnameのテキストを返す
        return self.name


# ミーティングのモデル
class Meeting(models.Model):
    day = models.DateTimeField(default=timezone.now) # date型 登録日(ミーティングが行われたとき？)
    partner_id = models.IntegerField() # model,partnerのidによる
    topic1 = models.TextField() # TextField 入力された話題1つめ
    topic2 = models.TextField(null=True, blank=True) # TextField 空，nullであることを許容
    topic3 = models.TextField(null=True, blank=True) # TextField 空，nullであることを許容

    def __str__(self):  # Meetingのdayのテキストを返す
        return self.day

# 話題のモデル
class Topic(models.Model):
    meeting_id = models.IntegerField() # int型 ミーティングのid
    topic = models.TextField() # TextField 話題

    def __str__(self):  # topicのtopicのテキストを返す
        return self.topic