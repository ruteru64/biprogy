from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import CreateView, TemplateView
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

from .word2vec import Word2Vec

from .forms import UserCreateForm, LoginForm, PartnerForm, MeetingForm
from .models import Topic, Meeting, Partner
from main import word2vec

# Create your views here.


def index(request):
    try:
        id = request.session['user_id']
        partners = Partner.objects.filter(user_id=id)
        user = User.objects.get(id=id)
        return render(request, 'index.html', {'isLogin': 1, 'partners': partners, 'user': user})
    except:
        return render(request, 'index.html', {'isLogin': 0})
        # index = Index.as_view()

        # アカウント作成


class Create_account(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            # フォームから'username'を読み取る
            name = form.cleaned_data.get('username')
            # フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            user = authenticate(username=name, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'create.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return render(request, 'create.html', {'form': form, })


create_account = Create_account.as_view()

# ログイン機能

ml = None


class Account_login(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            partners = Partner.objects.filter(user_id=user.id)
            login(request, user)
            request.session['user_id'] = user.id
            return redirect('/')
            ml = Word2Vec()
        return render(request, 'login.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form, })


account_login = Account_login.as_view()

# 営業先を追加


def add_partner(request, user_id):
    if request.method == "POST":  # POSTrequestなら
        # print("test")
        form = PartnerForm(request.POST)  # formの内容
        if form.is_valid():  # 記入内容が正常なら
            # Pattnerを登録
            partner = form.save(commit=False)
            partner.user_id = user_id
            partner.save()
            return redirect('/')
    else:
        form = PartnerForm()
    return render(request, 'add_partner.html', {'form': form})

# 指定された営業先の話題デッキを表示するview 引数にuser_idとpartner_idが必要


# def topic_deck(request, user_id, partner_id):
#     meeting = Meeting.objects.filter(
#         partner_id=partner_id).order_by('-day').first()  # 指定営業先に該当するMeetingのデータを抽出

#     if meeting:

#         topics = []

#         topics.append(meeting.topic1)

#         if meeting.topic2:
#             topics.append(meeting.topic2)

#         if meeting.topic3:
#             topics.append(meeting.topic3)

#         proposed_topics = topics  # mlしたくないからそのまま出すように

#         # proposed_topics = word2vec.topics(topics) # 抽出したtopicを機械学習にかけて，提案された話題リスト

#         # user = User.objects.get(id=user_id)

#         # form = LoginForm(user_id, user.password)

#         return render(request, 'topic_deck.html', {'proposed_topics': proposed_topics, "user_id": user_id, "partner_id": partner_id, "form": form})
#     else:
#         return render(request, 'topic_deck.html', {"user_id": user_id, "partner_id": partner_id})
#         # ミーティングで出た話題が入力されたものをデータベースに登録するview partner_idが必要


# def topic_deck_api(request, user_id, partner_id):
#     meeting = Meeting.objects.filter(
#         partner_id=partner_id).order_by('-day').first()  # 指定営業先に該当するMeetingのデータを抽出

#     if meeting:

#         topics = []

#         topics.append(meeting.topic1)

#         if meeting.topic2:
#             topics.append(meeting.topic2)

#         if meeting.topic3:
#             topics.append(meeting.topic3)

#         proposed_topics = {
#             "meta": {
#                 "user_id": user_id,
#                 "partner_id": partner_id
#             },
#             "data": {
#                 "topics": topics
#             }
#         }

#         # proposed_topics = word2vec.topics(topics) # 抽出したtopicを機械学習にかけて，提案された話題リスト

#         return JsonResponse(proposed_topics)
#     else:
#         return JsonResponse({
#             "meta": {
#                 "user_id": user_id,
#                 "partner_id": partner_id
#             }
#         })


def post_topic(request, user_id, partner_id):

    if request.method == "POST":  # POSTrequestなら
        form = MeetingForm(request.POST)  # formの内容

        if form.is_valid():  # 記入内容が正常なら
            # meetingを登録
            meeting = form.save(commit=False)
            meeting.partner_id = partner_id
            meeting.day = timezone.now()
            meeting.save()

            # print(meeting.id)

            # Topicを登録
            topic1 = meeting.topic1
            Topic.objects.create(
                meeting_id=meeting.id, partner_id=partner_id, topic=topic1)

            topic2 = meeting.topic2
            if topic2:
                Topic.objects.create(
                    meeting_id=meeting.id, partner_id=partner_id, topic=topic2)

            topic3 = meeting.topic3
            if topic3:
                Topic.objects.create(
                    meeting_id=meeting.id, partner_id=partner_id, topic=topic3)

            return redirect('test', user_id=user_id, partner_id=partner_id)
    else:
        form = MeetingForm()

    return render(request, 'post_topic.html', {'form': form})


def post_topic_api(request, user_id, partner_id):

    if request.method == "POST":  # POSTrequestなら
        form = MeetingForm(request.POST)  # formの内容

        if form.is_valid():  # 記入内容が正常なら
            # meetingを登録
            meeting = form.save(commit=False)
            meeting.partner_id = partner_id
            meeting.day = timezone.now()
            meeting.save()

            # print(meeting.id)

            # Topicを登録
            topic1 = meeting.topic1
            Topic.objects.create(
                meeting_id=meeting.id, partner_id=partner_id, topic=topic1)

            topic2 = meeting.topic2
            if topic2:
                Topic.objects.create(
                    meeting_id=meeting.id, partner_id=partner_id, topic=topic2)

            topic3 = meeting.topic3
            if topic3:
                Topic.objects.create(
                    meeting_id=meeting.id, partner_id=partner_id, topic=topic3)

            return redirect('topic_deck_api', user_id=user_id, partner_id=partner_id)
    else:
        form = MeetingForm()

    return False


def test(request, user_id, partner_id):
    # print(user_id, partner_id)
    meeting = Meeting.objects.filter(
        partner_id=partner_id).order_by('-day').first()  # 指定営業先に該当するMeetingのデータを抽

    if meeting:

        topics = []

        topics.append(meeting.topic1)

        if meeting.topic2:
            topics.append(meeting.topic2)

        if meeting.topic3:
            topics.append(meeting.topic3)

        proposed_topics = ml.topics(topics)  # mlしたくないからそのまま出すように

        proposed_topics = {
            "data": {
                "topics": topics
            }
        }
        return render(request, 'index2.html', {'user_id': user_id, 'partner_id': partner_id, 'proposed_topics': json.dumps(proposed_topics)})
    else:
        return render(request, 'index2.html', {"user_id": user_id, "partner_id": partner_id})
        # ミーティングで出た話題が入力されたものをデータベースに登録するview partner_idが必要
