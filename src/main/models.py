from django.db import models
from django.utils import timezone

# class User(models.Model):
#     username = models.TextField("username", max_length = 150, blank = True)
#     #email = models.EmailField("email", blank = True)
#     password1 = models.CharField("password1", max_length = 15)
#     password2 = models.CharField("password2", max_length = 15)

#     def __str__(self):
#         return self.name


class Partner(models.Model):
    user_id = models.IntegerField()  # int ユーザのid
    name = models.CharField(max_length=200)  # TextField 営業先の名前？
    belongs = models.CharField(max_length=200)  # TextField 営業先会社名

    def __str__(self):  # partnerのnameのテキストを返す
        return self.name


# ミーティングのモデル
class Meeting(models.Model):
    # date型 登録日(ミーティングが行われたとき？)
    day = models.DateTimeField(default=timezone.now)
    partner_id = models.IntegerField()  # model,partnerのidによる
    topic1 = models.CharField(max_length=200)  # TextField 入力された話題1つめ
    # TextField 空，nullであることを許容
    topic2 = models.CharField(max_length=200, null=True, blank=True)
    # TextField 空，nullであることを許容
    topic3 = models.CharField(max_length=200, null=True, blank=True)

    # def __str__(self):  # Meetingのdayのテキストを返す
    #     return self.partner_id

# 話題のモデル


class Topic(models.Model):
    meeting_id = models.IntegerField()  # int型 ミーティングのid
    partner_id = models.IntegerField()  # model,partnerのidによる
    topic = models.CharField(max_length=200)  # TextField 話題

    def __str__(self):  # topicのtopicのテキストを返す
        return self.topic
