from django.shortcuts import render, redirect
from . import models
from django.urls import reverse, reverse_lazy
from tweetapp.forms import AddTweetForm, AddTweetModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth import views as auth_views




def listtweet(request):
    all_tweets = models.Tweet.objects.all()
    tweet_dict = {"tweets":all_tweets}
    return render(request,'tweetapp/listtweet.html', context=tweet_dict)

@login_required(login_url="/login")
def addtweet(request):
    if request.POST:
        message = request.POST["message"]
        models.Tweet.objects.create(username=request.user, message=message)
        return redirect(reverse('tweetapp:listtweet'))
    return render(request,'tweetapp/addtweet.html')

def addtweetbyform(request):
     if request.method == "POST":  # Daha doğru bir kontrol
         form = AddTweetForm(request.POST)
         if form.is_valid():
             nickname = form.cleaned_data["nickname_input"]
             message = form.cleaned_data["message_input"]
             models.Tweet.objects.create(nickname=nickname, message=message)
             return redirect(reverse('tweetapp:listtweet'))
         else:
             print("error in form")
             print(form.errors)
             return render(request, "tweetapp/addtweetbyform.html", context={"form": form, "errors": form.errors})

     else:
         form = AddTweetForm()
         return render(request, "tweetapp/addtweetbyform.html", context={"form": form})
    
    

def addtweetbymodelform(request):
    if request.POST:
            form = AddTweetModelForm(request.POST)
            if form.is_valid():
                nickname = form.cleaned_data["nickname"]
                message = form.cleaned_data["message"]
                models.Tweet.objects.create(nickname=nickname, message=message)
                return redirect(reverse('tweetapp:listtweet'))
            else:
                print("error in form")
                print(form.errors)
                return render(request, "tweetapp/addtweetbymodelform.html", context={"form":form})
                    
    else:
        form = AddTweetModelForm
        return render(request, "tweetapp/addtweetbymodelform.html", context={"form":form})


@login_required
def deletetweet(request, id):
    tweet = models.Tweet.objects.get(pk=id)
    if request.user == tweet.username:
        models.Tweet.objects.filter(id=id).delete()
        return redirect('tweetapp:listtweet')


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")  # Başarıyla kaydedildikten sonra login sayfasına yönlendirme

    def form_valid(self, form):
        # Formun geçerli olduğunu kontrol ediyoruz
        response = super().form_valid(form)
        
        # Kullanıcı kaydını kontrol et
        print(f"New user created: {form.instance.username}")  # Debugging: Kullanıcı adı yazdırılır
        return response
    
