from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Skater, Trick
from .forms import BehaviorForm
from django.contrib.auth.views import LoginView


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def skater_index(request):
    skaters = Skater.objects.filter(user=request.user)
    return render(request, 'skaters/index.html', {'skaters': skaters})

# views.py
@login_required
def skater_detail(request, skater_id):
    skater = Skater.objects.get(id=skater_id)
    tricks_skater_doesnt_have = Trick.objects.exclude(id__in = skater.tricks.all().values_list('id'))
    behavior_form = BehaviorForm()
    return render(request, 'skaters/detail.html', {
        # include the cat and feeding_form in the context
        'skater': skater, 
        'behavior_form': behavior_form,
        'tricks': tricks_skater_doesnt_have
    })

@login_required
def add_behavior(request, skater_id):
    # create a ModelForm instance using the data in request.POST
    form = BehaviorForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the cat_id assigned
        new_behavior = form.save(commit=False)
        new_behavior.skater_id = skater_id
        new_behavior.save()
    return redirect('skater-detail', skater_id=skater_id)

@login_required
def associate_trick(request, skater_id, trick_id):
    # Note that you can pass a toy's id instead of the whole object
    Skater.objects.get(id=skater_id).tricks.add(trick_id)
    return redirect('skater-detail', skater_id=skater_id)

@login_required
def remove_trick(request, skater_id, trick_id):
    skater = Skater.objects.get(id=skater_id)
    trick = Trick.objects.get(id=trick_id)
    skater.tricks.remove(trick)
    return redirect('skater-detail', skater_id=skater.id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('skater-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )


class Home(LoginView):
    template_name = 'home.html'



class SkaterCreate(LoginRequiredMixin, CreateView):
    model = Skater
    fields = ['name', 'breed', 'description', 'age']
    success_url = '/skaters'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SkaterUpdate(LoginRequiredMixin, UpdateView):
    model = Skater
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']

class SkaterDelete(LoginRequiredMixin, DeleteView):
    model = Skater
    success_url = '/skaters/'


class TrickCreate(LoginRequiredMixin, CreateView):
    model = Trick
    fields = ['name', 'breed', 'description', 'age']
    success_url = '/skater'

class TrickList(LoginRequiredMixin, ListView):
    model = Trick

class TrickDetail(LoginRequiredMixin, DetailView):
    model = Trick

class TrickUpdate(LoginRequiredMixin, UpdateView):
    model = Trick
    fields = ['name', 'type']

class TrickDelete(LoginRequiredMixin, DeleteView):
    model = Trick
    success_url = '/tricks/'
