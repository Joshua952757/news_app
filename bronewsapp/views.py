from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.core.mail import send_mail
from django.conf import settings
from .forms import PublisherForm, ArticleForm, NewsletterForm
from .models import Article, Newsletter, Publisher, User, Profile
from .tweety import post_tweet


def home(request):
    return render(request, "home.html")


@login_required
def create_publisher(request):
    """Handles creating a new publisher."""
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save(commit=False)
            publisher.admin = request.user
            publisher.save()
            messages.success(request, "Publisher created successfully!")
            return redirect('home')  
    else:
        form = PublisherForm()
    return render(request, 'create_publisher.html', {'form': form})


@login_required
def publisher_list(request):
    """Displays a list of all publishers."""
    publishers = Publisher.objects.all()
    return render(request, 'publisher_list.html', {'publishers': publishers})


def publisher_detail(request, publisher_id):
    """Displays details of a specific publisher and their articles and newsletters."""
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    articles = Article.objects.filter(publisher=publisher)
    newsletters = Newsletter.objects.filter(publisher=publisher)

    # Check subscription status for the current logged-in user if they are a READER
    is_subscribed = False
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.READER:
        is_subscribed = request.user.profile.sub_publisher.filter(pk=publisher.pk).exists()

    return render(request, 'publisher_detail.html', {
        'publisher': publisher, 
        'articles': articles, 
        'newsletters': newsletters,
        'is_subscribed': is_subscribed, # Pass subscription status to template
    })


def article_create(request):
    """
    Handles creating a new article, associating it with the logged-in journalist.
    Access restricted to authenticated journalists.
    """
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to create an article.")
        return redirect('login')

    if not (hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.JOURNALIST): # Use Profile.Role
        messages.error(request, "You must be a journalist to create articles.")
        return redirect('home')

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Article created successfully!")
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'article_form.html', {'form': form, 'action': 'Create Article'})


def article_update(request, pk):
    """
    Handles updating an existing article.
    Access restricted to authenticated journalists (author) OR editors.
    """
    article = get_object_or_404(Article, pk=pk)

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to edit this article.")
        return redirect('login') 

    is_authorized = (request.user == article.author) or \
                    (hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.EDITOR) # Use Profile.Role

    if not is_authorized:
        messages.error(request, "You are not authorized to edit this article.")
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully!")
            return redirect('article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'article_form.html', {'form': form, 'action': 'Update Article'})


def article_delete(request, pk):
    """
    Handles deleting an article.
    Access restricted to authenticated journalists (author) OR editors.
    """
    article = get_object_or_404(Article, pk=pk)
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to delete this article.")
        return redirect('login') 

    is_authorized = (request.user == article.author) or \
                    (hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.EDITOR) # Use Profile.Role

    if not is_authorized:
        messages.error(request, "You are not authorized to delete this article.")
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        article.delete()
        messages.success(request, "Article deleted successfully!")
        return redirect('article_list')
    
    return render(request, 'article_confirm_delete.html', {'article': article})


def article_list(request):
    """
    Displays a list of all articles.
    """
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})


def article_detail(request, pk):
    """
    Displays the details of a specific article.
    """
    article = get_object_or_404(Article, pk=pk) 
    return render(request, 'article_detail.html', {'article': article})


def article_approve(request, pk):
    """
    Allows an editor to approve an article. 
    Sends approval emails and twitter posts.
    """
    article = get_object_or_404(Article, pk=pk)

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to approve this article.")
        return redirect('login') 

    if not (hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.EDITOR): # Use Profile.Role
        messages.error(request, "You must be an editor to approve articles.")
        return redirect('article_detail', pk=pk)

    if request.method == 'POST':
        article.is_approved = True
        article.save()
        emails = [
            profile.user.email
            for profile in article.author.subscribers.all()
            if profile.user.email
        ]
        if emails:
            send_mail(
                f"This article has been approved: {article.title}",
                f"Check out: {article.title} - Written by {article.author.username}",
                settings.DEFAULT_FROM_EMAIL,
                emails
            )
            
        tweet = f"Check out: {article.title} - Written by {article.author.username}"
        post_tweet(tweet)
        messages.success(request, f"Article '{article.title}' has been approved!")
        return redirect('article_detail', pk=pk)

    messages.warning(request, "Invalid request method for approval.")
    return redirect('article_detail', pk=pk)


def newsletter_create(request):
    """
    Handles creating a new newsletter, associating it with the logged-in journalist.
    Access restricted to authenticated journalists.
    """
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to create a newsletter.")
        return redirect('login')

    if not (hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.JOURNALIST): # Use Profile.Role
        messages.error(request, "You must be a journalist to create newsletters.")
        return redirect('home')

    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            messages.success(request, "Newsletter created successfully!")
            return redirect('newsletter_list')
    else:
        form = NewsletterForm()
    return render(request, 'newsletter_form.html', {'form': form, 'action': 'Create Newsletter'})


def newsletter_update(request, pk):
    """
    Handles updating an existing newsletter.
    Access restricted to authenticated journalists (author) OR editors.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to edit this newsletter.")
        return redirect('login') 

    is_authorized = (request.user == newsletter.author) or \
                    (hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.EDITOR) # Use Profile.Role

    if not is_authorized:
        messages.error(request, "You are not authorized to edit this newsletter.")
        return redirect('newsletter_detail', pk=pk)

    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, "Newsletter updated successfully!")
            return redirect('newsletter_detail', pk=pk)
    else:
        form = NewsletterForm(instance=newsletter)
    return render(request, 'newsletter_form.html', {'form': form, 'action': 'Update Newsletter'})


def newsletter_delete(request, pk):
    """
    Handles deleting a newsletter.
    Access restricted to authenticated journalists (author) OR editors.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to delete this newsletter.")
        return redirect('login') 

    is_authorized = (request.user == newsletter.author) or \
                    (hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.EDITOR) # Use Profile.Role

    if not is_authorized:
        messages.error(request, "You are not authorized to delete this newsletter.")
        return redirect('newsletter_detail', pk=pk)

    if request.method == 'POST':
        newsletter.delete()
        messages.success(request, "Newsletter deleted successfully!")
        return redirect('newsletter_list')
    
    return render(request, 'newsletter_confirm_delete.html', {'newsletter': newsletter})


def newsletter_list(request):
    """
    Displays a list of all newsletters.
    """
    newsletters = Newsletter.objects.all()
    return render(request, 'newsletter_list.html', {'newsletters': newsletters})


def newsletter_detail(request, pk):
    """
    Displays the details of a specific newsletter.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(request, 'newsletter_detail.html', {'newsletter': newsletter})


def newsletter_approve(request, pk):
    """
    Allows an editor to approve a newsletter.
    """
    newsletter = get_object_or_404(Newsletter, pk=pk)

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to approve this newsletter.")
        return redirect('login') 
    
    if not (hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.EDITOR): # Use Profile.Role
        messages.error(request, "You must be an editor to approve newsletters.")
        return redirect('newsletter_detail', pk=pk)
    
    if request.method == 'POST':
        newsletter.is_approved = True
        newsletter.save()
        messages.success(request, f"Newsletter '{newsletter.title}' has been approved!")
        return redirect('newsletter_detail', pk=pk)
    
    messages.warning(request, "Invalid request method for approval.")
    return redirect('newsletter_detail', pk=pk)


def journalist_dashboard_view(request):
    """
    Renders the journalist dashboard HTML page.
    """
    return render(request, 'journalist_dashboard.html')


def editor_dashboard_view(request):
    """
    Renders the editor dashboard HTML page.
    """
    return render(request, 'editor_dashboard.html')


def admin_dashboard_view(request):
    """
    Renders the admin dashboard HTML page.
    """
    return render(request, 'admin_dashboard.html')


@login_required
def subscribe_publisher(request, publisher_id):
    """
    Allows a Reader to subscribe to or unsubscribe from a Publisher.
    """
    if not request.method == 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('publisher_detail', publisher_id=publisher_id)

    if not (hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.READER):
        messages.error(request, "Only readers can subscribe to publishers.")
        return redirect('publisher_detail', publisher_id=publisher_id)

    publisher = get_object_or_404(Publisher, pk=publisher_id)
    user_profile = request.user.profile

    if user_profile.sub_publisher.filter(pk=publisher.pk).exists():
        user_profile.sub_publisher.remove(publisher)
        messages.success(request, f"You have unsubscribed from {publisher.name}.")
    else:
        user_profile.sub_publisher.add(publisher)
        messages.success(request, f"You have subscribed to {publisher.name}.")
        return redirect('publisher_detail', publisher_id=publisher_id)


def journalist_detail(request, user_id):
    """
    Displays details of a specific journalist user.
    """
    journalist = get_object_or_404(User, pk=user_id)
    if not (hasattr(journalist, 'profile') and journalist.profile.role == Profile.Role.JOURNALIST):
        messages.error(request, "User is not a journalist.")
        return redirect('home') # Redirect to home or a list of journalists

    is_subscribed = False
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.READER:
        is_subscribed = request.user.profile.sub_journalist.filter(pk=journalist.pk).exists()

    return render(request, 'journalist_detail.html', {
        'journalist': journalist,
        'is_subscribed': is_subscribed
    })


@login_required
def subscribe_journalist(request, user_id):
    """
    Allows a Reader to subscribe to or unsubscribe from a Journalist.
    """
    if not request.method == 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('journalist_detail', user_id=user_id)

    if not (hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.READER):
        messages.error(request, "Only readers can subscribe to journalists.")
        return redirect('journalist_detail', user_id=user_id)

    journalist_user = get_object_or_404(User, pk=user_id)

    if not (hasattr(journalist_user, 'profile') and journalist_user.profile.role == Profile.Role.JOURNALIST):
        messages.error(request, f"{journalist_user.username} is not a journalist.")
        return redirect('home')

    user_profile = request.user.profile

    if user_profile.sub_journalist.filter(pk=journalist_user.pk).exists():
        user_profile.sub_journalist.remove(journalist_user)
        messages.success(request, f"You have unsubscribed from {journalist_user.username}.")
    else:
        user_profile.sub_journalist.add(journalist_user)
        messages.success(request, f"You have subscribed to {journalist_user.username}.")
    
    return redirect('journalist_detail', user_id=user_id)