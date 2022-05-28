from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import CreateView, TemplateView
from django.views import View

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .word2vec import Word2Vec
# from ..hackSite import urls

from .forms import UserCreateForm, LoginForm, PartnerForm, MeetingForm
from .models import Topic, Meeting, Partner

#from ... Word2Vec.word2vec import Word2Vec

# Create your views here.


class Index(TemplateView):
    template_name = 'index.html'


index = Index.as_view()

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


class Account_login(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            partners = Partner.objects.filter(user_id=user.id)
            # redirect('/', {'user_id': user.id, 'partners': partners})
            for partner in partners:
                print(partner.pk, partner.name)
            # print("あああああああああああああああああああああああああああああああああああああああああああああああああああああ")
            login(request, user)
            print("あああああああああああああああああああああああああああああああああああああああああああああああああああああ")
            return render(request, 'index.html', {'user_id': user.id, 'partners': partners})
        return render(request, 'login.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form, })


account_login = Account_login.as_view()

# 営業先の一覧を表示


# def select_partner(request, user_id):
#     # partners = Partner.objects.filter(user_id = user_id)
#     partners = Partner.objects.filter(pk=user_id)
#     return render(request, 'select_partner.html', {'user_id': user_id, 'partners': partners})

# 営業先を追加


def add_partner(request):
    user_id = request.GET['userid']
    if request.method == "POST":  # POSTrequestなら
        # print("test")
        form = PartnerForm(request.POST)  # formの内容
        if form.is_valid():  # 記入内容が正常なら
            # Pattnerを登録
            partner = form.save(commit=False)
            partner.user_id = user_id
            partner.save()
            # return redirect('select_partner', user_id = partner.user_id)
            return redirect('select_partner', user_id=partner.pk)
    else:
        form.PartnerForm()
    return render(request, 'add_partner.html', {'form': form})

# 指定された営業先の話題デッキを表示するview 引数にuser_idとpartner_idが必要


def topic_deck(request, user_id, partner_id):
    # user_id = request.GET['user_id']
    # partner_id = request.GET['partnerid']
    # partners = Partner.objects.filter(user_id = user_id)
    # meetings = Meeting.objects.filter(partner_id = partner_id) # 指定営業先に該当するMeetingのデータを抽出
    meetings = Meeting.objects.filter(
        name=partner_id)  # 指定営業先に該当するMeetingのデータを抽出

    topics = []

    for meeting in meetings:  # Meetingのデータごとに
        # topics += Topic.objects.filter(meeting_id = meetings.id).topic # 該当するTopicを抽出し，話題のリストを作る
        meetings = Meeting.objects.filter(
            pk=partner_id)  # 指定営業先に該当するMeetingのデータを抽出

    proposed_topics = topics  # mlしたくないからそのまま出すように

    # proposed_topics = word2vec.topics(topics) # 抽出したtopicを機械学習にかけて，提案された話題リスト

    return render(request, 'topic_deck.html', {'proposed_topics': proposed_topics})

# ミーティングで出た話題が入力されたものをデータベースに登録するview partner_idが必要


def post_topic(request):
    if request.method == "POST":  # POSTrequestなら
        partner_id = request.GET['partnerid']
        form = MeetingForm(request.POST)  # formの内容

        if form.is_valid():  # 記入内容が正常なら
            # meetingを登録
            meeting = form.save(commit=False)
            meeting.partner_id = partner_id
            meeting.day = timezone.now()
            meeting.save()

            # Topicを登録
            topic1 = meeting.topic1
            # Topic.object.create(meeting_id = meeting.id, topic = topic1)
            Topic.object.create(pk=meeting.id, topic=topic1)

            topic2 = meeting.topic2
            if topic2 != None:
                # Topic.object.create(meeting_id = meeting.id,  topic = topic2)
                Topic.object.create(pk=meeting.id,  topic=topic2)

            topic3 = meeting.topic3
            if topic3 != None:
                # Topic.object.create(meeting_id = meeting.id,  topic = topic3)
                Topic.object.create(pk=meeting.id,  topic=topic3)

            # return redirect('topic_deck.html', patner_id = meeting.patrner_id)
            return redirect('topic_deck.html', patner_id=meeting.pk)
        else:
            form = MeetingForm()

        return render(request, 'topic_post.html', {'form': form})


# def add_partner()
