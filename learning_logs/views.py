from django.shortcuts import render,redirect,get_object_or_404
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import  login_required
from django.http import Http404

# Create your views here.
def index(request) :
    return render(request, "learning_logs/index.html")

@login_required
def topics(request):
    """ show all the topics """
    topic_shown = []
    for  topic in Topic.objects.all() :
        if topic.choice == "public" or topic.choice == "" :
            topic_shown.append(topic)
    topics=Topic.objects.filter(owner=request.user).order_by("date_added")
    for topic in topics :
        if topic.choice == "private" :
            topic_shown.append(topic)
    context = {"topics":topic_shown}
    return render(request,"learning_logs/topics.html" , context)

@login_required
def topic(request ,topic_id ) :
    """ show all the topics releted """
    topic = get_object_or_404(Topic,id=topic_id)
    entries=topic.entry_set.order_by("-date_added")
   # check_topic_ownership(request,topic)
    
    context ={"topic":topic ,"entries":entries}
    return render(request , "learning_logs/topic.html" , context)

@login_required
def new_topic(request) :
    if request.method != "POST" :
        form= TopicForm()
    else :
        form=TopicForm(data=request.POST)
        if form.is_valid() :
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            return redirect("learning_logs:topics")
            
    context ={"form":form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def edit_entry(request,entry_id):
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    check_topic_ownership(request,topic)
    
    if request.method != "POST":
        form = EntryForm(instance=entry)
    else :
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid() :
            form.save()
            return redirect('learning_logs:topic',topic_id =topic.id)
    context ={"form":form ,'topic':topic ,"entry":entry}
    return render(request,'learning_logs/edit_entry.html',context)



@login_required
def new_entry(request,topic_id) :
    topic=Topic.objects.get(id =topic_id)
    check_topic_ownership(request,topic)
    
    if request.method != "POST":
        form = EntryForm()
    else :
        form=EntryForm(data=request.POST)
        if form.is_valid() :
            new_entry=form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic',topic_id=topic.id)
    context ={"form":form ,"topic":topic}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_topic(request,topic_id) :
    topic=Topic.objects.get(id =topic_id)
    check_topic_ownership(request,topic)
    
    if request.method != "POST":
        form = TopicForm(instance=topic)
    else :
        form = TopicForm(data=request.POST,instance=topic)
        if form.is_valid() :
            form.save()
            return redirect("learning_logs:topics")
    context ={"form":form,"topic":topic}
    return render(request,'learning_logs/edit_topic.html',context)

def check_topic_ownership(request,topic):
    if topic.owner != request.user :
        raise Http404