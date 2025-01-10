from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LogoutView, LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import CustomAuthenticationForm, AvatarForm, MessageForm, ReviewForm
from .models import Avatar, Message, Review
from django.db.models import Q


import json

# _____________________ AUTH VIEWS _____________________
class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = CustomAuthenticationForm


class CustomPasswordChangeView(PasswordChangeView, LoginRequiredMixin):
    template_name="users/change_password.html"
    success_url = reverse_lazy('portfolio:index')

    def form_valid(self, form):
        form.save()
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "navbarChanged": None,
                    "showMessage": "La contraseña se actualizó correctamente."
                })
            }
        )


class CustomLogoutView(LogoutView, LoginRequiredMixin):
    template_name = "portfolio/index.html"

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        return redirect ('portfolio:index')    


# _____________________ AVATAR VIEWS _____________________

class AvatarDetailView(DetailView, LoginRequiredMixin):
    model = Avatar
    


class AvatarCreateView(View, LoginRequiredMixin):
    def get(self, request):
        form = AvatarForm()
        return render(request, 'users/avatar_form.html', {'form': form})

    def post(self, request):
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            Avatar.objects.create(
                user=request.user,
                image=form.cleaned_data.get('image'),
            )
            return HttpResponse(
                status=201,
                headers={
                    'HX-Trigger': json.dumps({
                        "navbarChanged": None,
                        "showMessage": "El Avatar se guardó correctamente."
                    })
                }
            )
        else:
            return render(request, 'users/avatar_form.html', {'form': form})

class AvatarConfirmActionView(View, LoginRequiredMixin):
    def get(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        return render(request, 'users/avatar_confirm_action.html', {'avatar': avatar})
    


class AvatarUpdateView(View, LoginRequiredMixin):
    def get(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        form = AvatarForm(instance=avatar)
        return render(request, 'users/avatar_form.html', {'form': form, 'avatar': avatar})

    def post(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        form = AvatarForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid():
            avatar.image = form.cleaned_data.get('image')
            avatar.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "navbarChanged": None,
                        "showMessage": "El avatar se actualizó correctamente."
                    })
                }
            )
        else:
            return render(request, 'users/avatar_form.html', {'form': form, 'avatar': avatar})


class AvatarDeleteView(View, LoginRequiredMixin):
    def delete(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        avatar.delete()
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "navbarChanged": None,
                    "showMessage":"El avatar se eliminó correctamente."
                })
            }
        )


# _____________________ MESSAGE VIEWS _____________________

class MessageListView(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'users/message_list.html', {})


class LoadMessageListView(View, LoginRequiredMixin):
    def get(self, request):
        consult = request.GET.get("consult", "")
        status = request.GET.get("status", "")
        date=request.GET.get("date",)

        messages= Message.objects.all()

        consult_words = consult.split(" ")
        if consult:
            query = Q()
            for word in consult_words:
                query |= Q(name__icontains=word) | Q(email__icontains=word)
            messages = messages.filter(query)

        if status:
            if status == "1":
                messages = messages.filter(is_read=False)
            elif status == "2":
                messages = messages.filter(is_read=True)
            else:
                pass
        
        if date == "1" or not date:
            messages = messages.order_by("-id")
        if date == "2":
            messages = messages.order_by("id")

        paginator = Paginator(messages, 10)
        page = request.GET.get('page')
        messages = paginator.get_page(page)

        context = {
            'object_list': messages,
            'consult': consult,
        }
        return render(request, 'users/partials/message_list.html', context)
    

class MessageDetailView(View, LoginRequiredMixin):
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
       
        return render(request, 'users/message_detail.html', {'message': message})
    
    def post(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        message.is_read = True
        message.save()
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "messageListChanged": None,
                })
            }
        )


class MessageCreateView(View):
    def get(self, request):
        form = MessageForm()
        return render(request, 'users/message_form.html', {'form': form})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                name=form.cleaned_data.get('name'),
                email=form.cleaned_data.get('email'),
                phone=form.cleaned_data.get("phone"),
                content=form.cleaned_data.get('content'),
            )
            return HttpResponse(
                status=201,
                headers={
                    'HX-Trigger': json.dumps({
                        "messageListChanged": None,
                        "showMessage": "El mensaje se envió correctamente."
                    })
                }
            )
        else:
            return render(request, 'users/message_form.html', {'form': form})


class MessageConfirmActionView(View, LoginRequiredMixin):
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        return render(request, 'users/message_confirm_action.html', {'message': message})
    

class MessageUpdateView(View, LoginRequiredMixin):
    def patch(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        if message.is_read:
            message.is_read = False
            message_status = "El mensaje se marcó como no leido."
        else:
            message.is_read = True
            message_status = "El mensaje se marcó como leido."
        message.save()
        return HttpResponse(
            status=200,
            headers={
                'HX-Trigger': json.dumps({
                    "messageListChanged": None,
                    "showMessage": message_status
                })
            }
        )
    

class MessageDeleteView(View, LoginRequiredMixin):
    def delete(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        message.delete()
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "messageListChanged": None,
                    "showMessage":"El mensaje se eliminó correctamente."
                })
            }
        )
    
class LoadNavbarView(View):
    def get(self, request):
        context={}
        return render(request, 'components/navbar.html', context)
    
    
    
# _____________________ REVIEW VIEWS _____________________

class ReviewListView(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'users/review_list.html', {})
    

class LoadReviewListView(View, LoginRequiredMixin):
    def get(self, request):
        consult = request.GET.get("consult", "")
        reviews = Review.objects.filter(Q(name__icontains=consult) | Q(email__icontains=consult)).order_by("-id")
       
        paginator = Paginator(reviews, 10) 
        page = request.GET.get('page')

        reviews = paginator.get_page(page)
        context = {
            'object_list': reviews,
            'consult': consult,
        }
        return render(request, 'users/partials/review_list.html', context)
    

class ReviewDetailView(View, LoginRequiredMixin):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        return render(request, 'users/review_detail.html', {'review': review})


class ReviewCreateView(View):
    def get(self, request):
        form = ReviewForm()
        return render(request, 'users/review_form.html', {'form': form})

    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                name=form.cleaned_data.get('name'),
                email=form.cleaned_data.get('email'),
                content=form.cleaned_data.get('content'),
            )
            return HttpResponse(
                status=201,
                headers={
                    'HX-Trigger': json.dumps({
                        "reviewListChanged": None,
                        "showMessage": "La reseña se envió correctamente."
                    })
                }
            )
        else:
            return render(request, 'users/review_form.html', {'form': form})


class ReviewConfirmActionView(View, LoginRequiredMixin):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        return render(request, 'users/review_confirm_action.html', {'review': review})
    

class ReviewUpdateView(View, LoginRequiredMixin):
    def patch(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        if review.is_approved:
            review.is_approved = False
            message_status="La reseña se marcó como no aprobado."
        else:
            review.is_approved = True
            message_status="La reseña se marcó como aprobado."
        review.save()
        return HttpResponse(
            status=200,
            headers={
                'HX-Trigger': json.dumps({
                    "reviewListChanged": None,
                    "showMessage": message_status
                })
            }
        )
    
class ReviewDeleteView(View, LoginRequiredMixin):
    def delete(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        review.delete()

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "reviewListChanged": None,
                    "showMessage":"La reseña se eliminó correctamente."
                })
            }
        )