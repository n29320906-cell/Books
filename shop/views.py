from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, Favorite, CartItem
from .forms import BookForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "shop/register.html", {"form": form})


# --- Башкы бет ---
def home(request):
    return render(request, 'shop/home.html')


# --- Китептер ---
from django.db.models import Q  # Бул сапты жогоруга импортко кошуңуз!


def book_list(request):
    books = Book.objects.all()
    query = request.GET.get('q')

    if query:
        books = books.filter(title__icontains=query)

    return render(request, 'shop/book_list.html', {'books': books, 'query': query})
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'shop/book_detail.html', {'book': book})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'shop/add_book.html', {'form': form})


# --- Избранное (Favorite) ---
@login_required
def toggle_favorite(request, pk):
    book = get_object_or_404(Book, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
    if created:
        messages.success(request, f'"{book.title}" избранного кошулду!')
    else:
        favorite.delete()
        messages.info(request, f'"{book.title}" избранноеден өчүрүлдү.')
    return redirect('book_detail', pk=pk)


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('book')
    return render(request, 'shop/favorite_list.html', {'favorites': favorites})


# --- Корзина (Cart) ---
@login_required
def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    item, created = CartItem.objects.get_or_create(user=request.user, book=book)

    if not created:
        item.quantity += 1
        item.save()

    messages.success(request, f'"{book.title}" корзинага кошулду!')
    return redirect('cart')  # 'cart' аталышына багыттайбыз


@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.book.price * item.quantity for item in items)

    # Эң маанилүүсү: Бул сап сөзсүз болушу керек, антпесе ValueError чыгат.
    return render(request, 'shop/cart.html', {'items': items, 'total': total})

@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    messages.info(request, 'Корзинадан өчүрүлдү.')
    return redirect('cart')


# --- Төлөм (Checkout) ---
@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.book.price * item.quantity for item in items)


    return render(request, 'shop/checkout.html', {
        'items': items,
        'total': total
    })


@login_required
def increase_quantity(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        # Саны 1 болсо, минуска басканда корзинадан өчүрөбүз
        item.delete()
    return redirect('cart')