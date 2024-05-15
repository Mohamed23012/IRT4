from django.shortcuts import get_object_or_404, redirect, render

from Enseignant.forms import CategoryForm, EnseignantForm
from Enseignant.models import Category, Enseignant

# Create your views here.
def ajoutercategory(request):  
    if request.method == "POST" :  
        formcategory = CategoryForm(request.POST, request.FILES)  
        if formcategory.is_valid():  
             
                formcategory.save()  
                return redirect('list_category')
                print("ah")  
            
        else :
            print ("ah1")   
    else:  
        formcategory = CategoryForm() 
        print("err")
        
    return render(request,'ajoutercategory.html',{'formcategory':formcategory}) 

def list_category(request):  
    categoryts = Category.objects.all()  
    return render(request,"liste_category.html",{'categoryts':categoryts})  

def modifier(request, id):  
    category = Category.objects.get(id=id)  
    if request.method == 'POST':
        formcategory = CategoryForm(request.POST, instance=category)  
        if formcategory.is_valid():  
            formcategory.save()  
            return redirect("list_category")  
    else:
        formcategory= CategoryForm(instance=category)
        print("ah1")

    return render(request, 'modifier_category.html', {'category': category, 'formcategory': formcategory})
 
def suprimer(request, id):
    category = get_object_or_404(Category, id=id)
    return render(request, 'suprimer.html', {'category': category})

     

     
def destroycategory(request, id):
        category = Category.objects.get(id=id)  
        category.delete()  
        return redirect("list_category" )   


def ajouterenseignant(request):  
    if request.method == "POST" :  
        form = EnseignantForm(request.POST, request.FILES)  
        if form.is_valid():  
             
                form.save()  
                return redirect('liste_enseignant')
                print("ah")  
            
        else :
            print ("ah1")   
    else:  
        form = EnseignantForm() 
        print("err")
        
    return render(request,'ajouterenseignant.html',{'form':form}) 
def liste_enseignant(request):  
    enseignants = Enseignant.objects.all()  
    return render(request,"liste_enseignants.html",{'enseignants':enseignants})   


def update(request, id):  
    enseignant = Enseignant.objects.get(id=id)  
    if request.method == 'POST':
        form = EnseignantForm(request.POST, request.FILES, instance=enseignant)  
        if form.is_valid():  
            form.save()  
            return redirect("liste_enseignant")  
    else:
        form = EnseignantForm(instance=enseignant)
        print("ah1")

    return render(request, 'modifier_enseignant.html', {'enseignant': enseignant, 'form': form})

def confirm_delete(request, id):
    enseignant = get_object_or_404(Enseignant, id=id)
    return render(request, 'confirme.html', {'enseignant': enseignant})

     

     
def destroy(request, id):
        enseignant = Enseignant.objects.get(id=id)  
        enseignant.delete()  
        return redirect("liste_enseignant" )  



from django.db.models import Count

def graphiques_enseignants(request):
    # Données pour le graphique d'âge
    enseignants = Enseignant.objects.all()
    ages = [enseignant.age for enseignant in enseignants]

    # Données pour le graphique de sexe
    sexes_count = Enseignant.objects.values('sexe').annotate(nombre=Count('sexe'))
    sexes = {sex['sexe']: sex['nombre'] for sex in sexes_count}

    # Données pour le graphique de catégorie
    categories_count = Enseignant.objects.values('categories__nom').annotate(total=Count('categories'))
    categories = {cat['categories__nom']: cat['total'] for cat in categories_count}

    # Données pour le graphique de niveau
    niveaux_count = Enseignant.objects.values('niveau').annotate(total=Count('niveau'))
    niveaux = {niveau['niveau']: niveau['total'] for niveau in niveaux_count}

    return render(request, 'graphiques_enseignants.html', {
        'ages': ages,
        'sexes': sexes,
        'categories': categories,
        'niveaux': niveaux
    })