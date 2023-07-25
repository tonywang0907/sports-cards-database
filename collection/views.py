from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import SportsCard, Tag, TagCard
from django.core.paginator import Paginator
# Create your views here.

# Searching incorporate in index for simplicity 
from django.core.paginator import Paginator

def home(request):
    cards = SportsCard.objects.all()
    total_cards = cards.count()

    base_card_tag = Tag.objects.get(name='Base Card')
    base_cards = base_card_tag.cards.count()

    non_base_cards = total_cards - base_cards

    base_card_percent = (base_cards / total_cards) * 100 

    context = {
        'cards': cards,
        'total_cards': total_cards,
        'base_cards': base_cards,
        'non_base_cards': non_base_cards,
        'base_card_percent': base_card_percent,
    }

    return render(request, 'home.html', context)

def index(request):
    query = request.GET.get('query', '')
    cards = SportsCard.objects.all()

    # Search Card   
    if query:
        cards = cards.filter(
            Q(tagcard__tag__name__icontains=query) |
            Q(sport__icontains=query) |
            Q(player__icontains=query) |
            Q(product__icontains=query) |
            Q(variation__icontains=query)
        ).distinct()

    # Sort Alphabetically 
    sort_field = request.GET.get('sort_field')
    sort_order = request.GET.get('sort_order', 'asc')


    if sort_field == 'player':
        # Perform sorting by player column
        if sort_order == 'asc':
            cards = cards.order_by('player')  # Sort in ascending order
        else:
            cards = cards.order_by('-player')  # Sort in descending order


    player_count = cards.values('player').distinct().count()
    total_count = cards.count()

    # Configure pagination
    paginator = Paginator(cards, 15)  # Show 15 cards per page
    page_number = request.GET.get('page')
    cards = paginator.get_page(page_number)

    if cards:
        first_card_on_pg = (cards.number - 1) * cards.paginator.per_page + 1
        last_card_on_pg = cards.end_index()
    else:
        first_card_on_pg = 0
        last_card_on_pg = 0

    context = {
        'cards': cards,
        'total_count': total_count,
        'player_count': player_count,
        'first_card_on_pg': first_card_on_pg,
        'last_card_on_pg': last_card_on_pg,
        'query': query,
        'sort_field': sort_field,
        'sort_order': sort_order,
    }

    return render(request, 'index.html', context)


def add_card(request):
    return render(request, 'add_card.html')

# Store Card
def store_card(request):
    if request.method == 'POST':
        card_type = request.POST.get('option') == 'yes'
        sport = request.POST.get('sport')
        player = request.POST.get('player')
        product = request.POST.get('product')
        variation = request.POST.get('variation')
        tag_names = request.POST.get('tags').split(',')

        base_card = None
        non_base_card = None

        if card_type:
            # Check if the base card already exists
            base_card = SportsCard.objects.filter(
                sport=sport,
                player=player,
                product=product,
                variation=variation
            ).first()

            if base_card:
                # Base card already exists, increment the quantity by 1
                base_card.quantity += 1
                base_card.save()
            else:
                # Base card does not exist, create a new card
                base_card = SportsCard.objects.create(
                    sport=sport,
                    player=player,
                    product=product,
                    variation=variation
                )
            # Add "Base Card" tag to the card
            base_card_tag, _ = Tag.objects.get_or_create(name="Base Card")
            tag_card, _ = TagCard.objects.get_or_create(tag=base_card_tag, card=base_card)
        else:
            # Check if the non-base card already exists
            non_base_card = SportsCard.objects.filter(
                sport=sport,
                player=player,
                product=product,
                variation=variation
            ).first()

            if non_base_card:
                # Non-base card already exists, increment the quantity by 1
                non_base_card.quantity += 1
                non_base_card.save()
            else:
                # Non-base card does not exist, create a new card
                picture = request.FILES.get('import-pic')
                non_base_card = SportsCard.objects.create(
                    sport=sport,
                    player=player,
                    product=product,
                    variation=variation,
                    picture=picture
                )

            # Add "Non-Base Card" tag to the card
            non_base_card_tag, _ = Tag.objects.get_or_create(name="Non-Base Card")
            tag_card, _ = TagCard.objects.get_or_create(tag=non_base_card_tag, card=non_base_card)

        # Process tags if the tag_names list is not empty
        if tag_names and tag_names[0]:    
            # Process other tags
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                tag_card, _ = TagCard.objects.get_or_create(tag=tag, card=base_card or non_base_card)

        return redirect('add_card')
    return render(request, 'add_card.html')

# Edit or Update Card
def edit_card(request, card_id):
    try:
        card = SportsCard.objects.get(id=card_id)
        if request.method == 'POST':
            # Retrieve the updated data from the form
            sport = request.POST.get('sport')
            player = request.POST.get('player')
            product = request.POST.get('product')
            variation = request.POST.get('variation')
            picture = request.FILES.get('picture')
            tag_names = request.POST.get('tags').split(',')
            option = request.POST.get('option')

            # Update the card object with the new data
            card.sport = sport
            card.player = player
            card.product = product
            card.variation = variation

            # Update the picture if a new file was uploaded
            if picture:
                card.picture = picture

            # Update the card type based on the selected option
            # TagCard.objects.filter(card=card).delete() # Clear existing tags
            TagCard.objects.filter(card=card).delete()
            if option == 'yes':
                base_card_tag, _ = Tag.objects.get_or_create(name='Base Card')
                card.tag_set.add(base_card_tag)
            elif option == 'no':
                non_base_card_tag, _ = Tag.objects.get_or_create(name='Non-Base Card')
                card.tag_set.add(non_base_card_tag)

            # Add the new tags
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                TagCard.objects.get_or_create(tag=tag, card=card)

            # Save the changes to the database
            card.save()
                
            return redirect('index')
        else:
            base_card_tag = card.tag_set.filter(name='Base Card').exists()
            non_base_card_tag = card.tag_set.filter(name='Non-Base Card').exists()
            context = {
                'card': card,
                'base_card_tag': base_card_tag,
                'non_base_card_tag': non_base_card_tag
            }
            return render(request, 'edit_card.html', context)

    except SportsCard.DoesNotExist:
        return redirect('index')

# Delete Card 
def delete_card(request, card_id):
    try:
        card = get_object_or_404(SportsCard, id=card_id)

        # Delete the associated picture from the database and filesystem
        if card.picture:
            card.picture.delete()

        card.delete()
        return redirect('index')
    
    except SportsCard.DoesNotExist:
        return redirect('index')  

def toggle_tag(request, card_id, tag_name):
    card = get_object_or_404(SportsCard, id=card_id)
    tag, _ = Tag.objects.get_or_create(name=tag_name)

    if card.tagcard_set.filter(tag=tag).exists():
        # Tag exists, remove it from the card
        tag_card = card.tagcard_set.get(tag=tag)
        tag_card.delete()
    else:
        # Tag doesn't exist, add it to the card
        tag_card = TagCard.objects.create(tag=tag, card=card)

    return redirect('card_info', card_id=card_id)

# Card Info
def card_info(request, card_id):
    try:
        card = get_object_or_404(SportsCard, id=card_id)
        tags = card.tagcard_set.all()

        watchlist_tag = None
        if tags.filter(tag__name='Watchlist').exists():
            watchlist_tag = Tag.objects.get(name='Watchlist')

        favorite_tag = None
        if tags.filter(tag__name='Favorite').exists():
            favorite_tag = Tag.objects.get(name='Favorite')

        context = {'card': card,
                   'favorite_tag': favorite_tag,
                   'watchlist_tag': watchlist_tag
                   }
        return render(request, 'card_info.html', context)

    except SportsCard.DoesNotExist:
        return render(request, 'card_info.html')
    
def market(request):
    return render(request, 'market.html')
