import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.shortcuts import render, redirect
from .models import Tweet
from .forms import TweetForm


ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    print(request.user or None)
    return render (request, "pages/home.html", context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    # print("ajax:", request.is_ajax())
    form = TweetForm(request.POST or None)
    # print('post data is', request.POST)
    next_url = request.POST.get("next") or None
    # print("next_url", next_url)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)  # 201 == created items
        """
            By doing this we are adding new tweet
            and then redireting to same page
        """
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    return render(request, 'components/form.html', context={'form': form})


def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    qs = Tweet.objects.all()
    # it was kind of code where you can take a list
    # and for loop python dictionary inside it so I
    # am commenting out putting in for future refrences
    """
    tweets_list = [{
        "id": x.id,
        "content": x.content,
        "likes": random.randint(0 , 122),
        } for x in qs]
        """
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    data = {
        "id": tweet_id,
    }
    status = 200
    blank = "me"
    print(blank)
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404

    return JsonResponse(data, status=status)
    # json.dumps content_type='application/json'
