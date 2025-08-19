from django.shortcuts import render,redirect
from django.views.generic import View, ListView, TemplateView
from .forms import *
from django.db import connection
from .models import *
from django.http import JsonResponse

class MafiaWinView(TemplateView):
    template_name = 'win-mafia.html'
class MafiaLoseView(TemplateView):
    template_name = 'lose-mafia.html'

def check_mafia_result(request):
    result = request.session.get("is_mafia", None)
    return JsonResponse({"result": result})

# Create your views here.
class CreateGameView(View):
    def get(self, request):
        
        formset = GamersFormSet(queryset=Gamers.objects.all())
        request.session.flush()
        Gamers.objects.all().update(is_dead = False, is_linchead = False, role = None)
        
        request.session['pk_role'] = 1
        return render(request, "add-gamers.html", {"formset": formset})

    def post(self, request):
        formset = GamersFormSet(request.POST, queryset=Gamers.objects.none())
        if formset.is_valid():
            formset.save()
            return redirect('set-role', pk = Role.objects.filter(name = 'Мафія').first().pk) 
        return render(request, "add-gamers.html", {"formset": formset})
    
class ListGamersView(ListView):
    model = Gamers
    template_name = 'base.html'
    context_object_name = 'gamers'

class SetRoleView(View):

    def get(self, request, pk):
        
        role = Role.objects.filter(pk = pk).first()
        is_mafia = None
        
        if request.session['pk_role'] == 1:
            request.session['is_mafia'] = True
            formset = SetRoleFormSet()
            if formset.is_valid():
                formset.save()
            return render(request, "set-role.html", {"formset": formset, 'role':role.name, 'is_mafia':request.session['is_mafia']})

        else:
            form = UpdateRoleForm()
            request.session['is_mafia']  = False
            return render(request, "set-role.html", {"form": form, 'role':role.name, 'is_mafia':request.session['is_mafia'] })

    def post(self, request, pk):
        if request.session['is_mafia']:
            formset =SetRoleFormSet(request.POST)
            if formset.is_valid():
                for form in formset:
                    gamer = Gamers.objects.filter(name = form.cleaned_data['gamer'].name).first()
                    gamer.role = Role.objects.filter(pk = 1).first()
                    gamer.save()
            request.session['pk_role'] += 1
        else:
            form = UpdateRoleForm(request.POST)
            role = Role.objects.filter(pk = pk).first()
            request.session['pk_role'] += 1
            if form.is_valid():
                
                gamer = Gamers.objects.filter(name = form.cleaned_data['gamer'].name).first()
                gamer.role = role
                gamer.save()
                if request.session['pk_role']==6:
                    request.session['time'] = 'night'
                    request.session['pk_role'] = 1
                    citizen_role = Role.objects.get(name="Мирний житель")
                    Gamers.objects.filter(role__isnull=True).update(role=citizen_role)
                    return redirect('game', pk = request.session['pk_role'])
                return redirect('set-role', pk = request.session['pk_role'])
            
        return redirect('set-role', pk = request.session['pk_role'])

class GameView(View):
    def get(self, request, pk):
        
        if request.session['time'] == 'night':
            context = {}
            
            form = UpdateRoleForm()
            
            if pk != 0:
                role = Role.objects.filter(pk = pk).first()
                context['role'] = role.name
            context = {}
            context['form'] = form
            context['role'] = role.name

            return render(request, 'night.html', context)
        else:
            mafia = len(Gamers.objects.filter(pk = 1).all())
            citizen = len(Gamers.objects.filter(pk != 1).all())
            if mafia >= citizen:
                return redirect('win-mafia')
            elif mafia == 0:
                return redirect('lose-mafia')

            context = {}
            context['mafia_choose'] = request.session['mafia_choose']
            context['killer_choose'] = request.session['killer_choose']
            context['doctor_choose'] = request.session['doctor_choose']
            context['whore_choose'] = request.session['whore_choose']
            context['form'] = UpdateRoleForm()
            context['dead'] = Gamers.objects.filter(is_dead = True).all()
            print(Gamers.objects.filter(is_dead = True).all())

            return render(request, 'day.html', context)

    def post(self, request, pk):
        if request.session['time'] == 'night':
            if request.session['pk_role'] == 1:
                form = UpdateRoleForm(request.POST)
                if form.is_valid():
                    gamer = form.cleaned_data['gamer']
                    gamer.is_dead = True
                    gamer.save()
                    request.session['mafia_choose'] = gamer.name
                    request.session['pk_role'] += 1
                return redirect('game', pk = request.session['pk_role'])

            elif request.session['pk_role'] == 2:
                form = UpdateRoleForm(request.POST)
                if form.is_valid():
                    gamer = form.cleaned_data['gamer']
                    gamer.is_dead = True
                    gamer.save()
                    request.session['killer_choose'] = gamer.name
                    request.session['pk_role'] += 1
                return redirect('game', pk = request.session['pk_role'])
            
            elif request.session['pk_role'] == 3:
                form = UpdateRoleForm(request.POST)
                if form.is_valid():
                    gamer = form.cleaned_data['gamer']
                    if not gamer.is_linchead:
                        gamer.is_dead = True
                    else:
                        
                        gamer.is_dead = False
                    

                            
                    gamer.save()
                    request.session['doctor_choose'] = gamer.name
                    request.session['pk_role'] += 1
                return redirect('game', pk = request.session['pk_role'])
            
            elif request.session['pk_role'] == 4:
                form = UpdateRoleForm(request.POST)
                if form.is_valid():
                    gamer = form.cleaned_data['gamer']
                    
                    gamer.save()
                    request.session['whore_choose'] = gamer.name
                    request.session['pk_role'] += 1
                return redirect('game', pk = request.session['pk_role'])
            
            elif request.session['pk_role'] == 5:
                form = UpdateRoleForm(request.POST)
                if form.is_valid():
                    gamer = form.cleaned_data['gamer']
                    result = None
                    if not gamer.is_linchead or gamer.is_dead:
                        gamer.is_dead = True
                        gamer.save()
                    if gamer.role.pk == 1:
                        result = "Підар👍"
                    else:
                        result = "Не підар👎"

                    request.session['is_mafia'] = result
                    request.session['pk_role'] = 0
                    request.session['time'] = 'day'

                    # якщо це AJAX → повертаємо JSON
                    if request.headers.get("x-requested-with") == "XMLHttpRequest":
                        return JsonResponse({"result": result})

                    return redirect('game', pk=request.session['pk_role'])
           
            
        
        else:
            context = {}
            form = UpdateRoleForm(request.POST)
            if form.is_valid():
                gamer = form.cleaned_data['gamer']
                if gamer is not None:
                    gamer = form.cleaned_data['gamer']
                    gamer.is_linchead = True
            request.session['time'] = 'night'
            request.session['pk_role'] = 1
            return redirect('game', pk = request.session['pk_role'])

            
