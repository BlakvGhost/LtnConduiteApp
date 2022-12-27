from django.db.models import Sum,Avg,Q
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as connect,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Vote,Classe,AskNewPassword,Review



class Utils:
    def whoami(request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            else:
                return False

    def notifications():
        data = []
        password_reset_new = AskNewPassword.objects.filter(statue='New').order_by('-id')[0:3]
        reviews_upgrade = Review.objects.filter(statue='upgrade').order_by('-id')[0:3]
        reviews_new = Review.objects.filter(statue='New').order_by('-id')[0:3]
        total = len(password_reset_new)+len(reviews_new)+len(reviews_upgrade)
        for x,post in enumerate(password_reset_new):
            data.append([User.objects.get(id=post.user),post])
        return {'passN':data,'revwU':reviews_upgrade,'revwN':reviews_new,'total':total}

    def appreciation(value):
        if 0 <= value and value <= 7:
            return "Mediocre"
        if 8 <= value and value <= 11:
            return "Passable"
        if 12 <= value and value <= 13:
            return "Assez Bien"
        if 14 <= value and value <= 16:
            return "Bien"
        if 17 <= value and value <= 18:
            return "Très Bien"
        if 19 <= value and value <= 20:
            return "Excellent"

    def getAll():
        data,votes,classeI,classeII = [],Vote.objects.all(),[],[]
        for votex in votes:
            note = votes.filter(classe=votex.classe,note__isnull=False).aggregate(Sum('note'))['note__sum'] / votes.filter(classe=votex.classe,note__isnull=False).count()
            avis = Utils.appreciation(note)
            if not data.__contains__([votex.classe,note,avis]):
                data.append([votex.classe,note,avis])
        for x in votes.filter(niveau=1):
            if not classeI.__contains__(x.classe):
                classeI.append(x.classe)
        for x in votes.filter(niveau=2):
            if not classeII.__contains__(x.classe):
                classeII.append(x.classe)
        return {'data':data,'classeI':classeI,'classeII':classeII}

    def login(request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('controllers')
            else:
                return redirect('teachers')
        info = ''
        if request.method == 'POST':
            user = authenticate(request, username=request.POST['user_name'], password=request.POST['mdp'])
            if user is not None:
                connect(request,user)
                return redirect('login')
            else:
                info = "Mot de Passe Incorrect "
        context = {'users':User.objects.filter(is_staff=False),'info':info}
        return render(request,'login.html',context)

    def logoutUser(request):
        logout(request)
        return redirect('login')

class Surveillant:

    @login_required(login_url='login')
    def inscrire(request):
        if not Utils.whoami(request):
            return redirect('teachers')
        post,info = request.POST,''
        if request.method == 'POST':
            user = User.objects.create_user(post['id'],'',post['mdp'])
            user.first_name,user.last_name,user.is_staff = post['nom'],post['prenom'],False
            user.save()
            info = f"{post['nom']} {post['prenom']} Enregister avec sucess"
        notifs = Utils.notifications()
        context = {'passN':notifs['passN'],'revwU':notifs['revwU'],'revwN':notifs['revwN'],'Htotal':notifs['total'],'info':info}
        return render(request,'inscrire.html',context)

    @login_required(login_url='login')
    def controllers(request):
        if not Utils.whoami(request):
            return redirect('teachers')
        notifs = Utils.notifications()
        context = {'passN':notifs['passN'],'revwU':notifs['revwU'],'revwN':notifs['revwN'],'Htotal':notifs['total']}
        return render(request,'sSindex.html',context)

    @login_required(login_url='login')
    def voirVote(request):
        if not Utils.whoami(request):
            return redirect('teachers')
        values = Utils.getAll()
        notifs = Utils.notifications()
        context = {'niveau1':Vote.objects.filter(niveau=1),'niveau2':Vote.objects.filter(niveau=2),'moyennes':values['data'],'classeI':values['classeI'],'classeII':values['classeII'],'passN':notifs['passN'],'revwU':notifs['revwU'],'revwN':notifs['revwN'],'Htotal':notifs['total']}
        return render(request,'vote1.html',context)

    @login_required(login_url='login')
    def printable(request):
        if not Utils.whoami(request):
            return redirect('teachers')
        values = Utils.getAll()
        data,votes = [],Vote.objects.all()
        for votex in votes:
            totol = votes.filter(classe=votex.classe,note__isnull=False).count()
            if not data.__contains__([votex.classe,totol]):
                data.append([votex.classe,totol])
        notifs = Utils.notifications()
        context = {'moyennes':values['data'],'classeI':values['classeI'],'classeII':values['classeII'],'totals':data,'passN':notifs['passN'],'revwU':notifs['revwU'],'revwN':notifs['revwN'],'Htotal':notifs['total']}
        return render(request,'vote2.html',context)

    @login_required(login_url='login')
    def inscrireDeja(request):
        if not Utils.whoami(request):
            return redirect('teachers')
        post = request.POST
        if request.method == 'POST':
            user = User.objects.get(id=post['id_user'])
            user.username,user.first_name,user.last_name = post['id'],post['nom'],post['prenom']
            user.set_password(post['mdp'])
            user.save()
        notifs = Utils.notifications()
        context = {'teachers':User.objects.filter(is_staff=False),'passN':notifs['passN'],'revwU':notifs['revwU'],'revwN':notifs['revwN'],'Htotal':notifs['total']}
        return render(request,'voir.html',context)

    @login_required(login_url='login')
    def passwordReset(request):
        if not Utils.whoami(request):
            return redirect('teachers')
        notifs,data = Utils.notifications(),[]
        demandes = AskNewPassword.objects.filter(statue='New')
        for x,post in enumerate(demandes):
            data.append([User.objects.get(id=post.user),post])
        notifs = Utils.notifications()
        context = {'passN':notifs['passN'],'revwU':notifs['revwU'],'revwN':notifs['revwN'],'Htotal':notifs['total'],'demandes':data}
        return render(request,'password.html',context)

    @login_required(login_url='login')
    def validePasswordDetail(request,pk):
        if not Utils.whoami(request):
            return redirect('teachers')
        notifs = Utils.notifications()
        user = User.objects.get(id=pk)
        context = {'passN':notifs['passN'],'revwU':notifs['revwU'],'revwN':notifs['revwN'],'Htotal':notifs['total'],'userx':user}
        return render(request,'passwordDetail.html',context)

    @login_required(login_url='login')
    def suggestions(request):
        if not Utils.whoami(request):
            return redirect('teachers')
        notifs = Utils.notifications()
        suggs = Review.objects.all()
        context = {'passN':notifs['passN'],'revwU':notifs['revwU'],'revwN':notifs['revwN'],'Htotal':notifs['total'],'suggestions':suggs}
        return render(request,'suggestions.html',context)
class Enseignant:
    @login_required(login_url='login')
    def teachers(request):
        if Utils.whoami(request):
            return redirect('controllers')
        info,rated,rate = '','',''
        if not Review.objects.filter(user=request.user):
            rated = 'TrueRated'
        else:
            rate = Review.objects.get(user=request.user)
            rated = 'upgrade'
        if request.method == 'POST':
            classe = request.POST.getlist('classe')
            note = request.POST.getlist('note')
            for x, post in enumerate(classe):
                niveau = Classe.objects.get(classe=post).niveau
                instance = Vote(user=request.user,classe=post,note=note[x],message=request.POST['message'],ua=request.META['HTTP_USER_AGENT'],niveau=niveau)
                instance.save()
                info = "Vous avez bien voter,Merci !"
        return render(request,'teacher.html',{'info':info,'rated':rated,'rate':rate})
class Ajax(Utils):
    def __init__(Utils, arg):
        super(Utils, Utils).__init__()

    @login_required(login_url='login')
    def validePassword(request):
        if not Utils.whoami(request):
            return redirect('teachers')
        post = request.POST
        if request.method == 'POST':
            user = User.objects.get(id=post['id_user'])
            user.set_password(post['mdp'])
            user.save()
            ask = AskNewPassword.objects.get(user=user.id)
            ask.statue = "old"
            ask.save()
        return render(request,'password.html',{'info':"Mot de passe reinitialisé avec success"})

    @login_required(login_url='login')
    def unNew(request):
        item = Review.objects.get(id=request.GET['id'])
        item.statue = 'old'
        item.save()
        return JsonResponse(True,safe=False)

    @login_required(login_url='login')
    def delete(request):
        if not Utils.whoami(request):
            return redirect('teachers')
        instance = User.objects.get(id=request.GET['id'])
        User.delete(instance)
        return JsonResponse(True,safe=False)

    @login_required(login_url='login')
    def listClassFetch(request):
        if Utils.whoami(request):
            return redirect('controllers')
        data,as_classe = [],Classe.objects.filter(classe__icontains=request.GET['classe'])
        for classe in as_classe:
            data.append(classe.classe)
        return JsonResponse(data,safe=False)

    @login_required(login_url='login')
    def classExist(request):
        if Utils.whoami(request):
            return redirect('controllers')
        if Classe.objects.filter(classe=request.GET['classe']):
            return JsonResponse(True,safe=False)
        else:
            return JsonResponse(False,safe=False)

    def askNewPasswd(request):
        if request.method == 'POST':
            instance = AskNewPassword(user=request.POST['user'],email=request.POST['email'],message=request.POST['message'],ua=request.META['HTTP_USER_AGENT'],statue='New')
            instance.save()
        return render(request,'login.html',{'warn':"Demande Envoyer,Veillez Patienter"})

    @login_required(login_url='login')
    def reviewSave(request):
        info = ''
        if request.method == 'POST':
            if request.POST['state'] == 'TrueRated':
                instance = Review(user=request.user,content=request.POST['message'],rate=request.POST['rate'],statue="New")
                info = "Vote Accepter"
            else:
                instance = Review.objects.get(user=request.user)
                instance.content,instance.rate,instance.statue = request.POST['message'],request.POST['rate'],'upgrade'
                info = "Vote mise à jour avec success"
            instance.save()
            return render(request,'teacher.html',{'warn':info})

    def vuejs(request):

        data = {'prenom': "Assoumailou", 'nom': "ADAM"}
        return JsonResponse(data,safe=False)
