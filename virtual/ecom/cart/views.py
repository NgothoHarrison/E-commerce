from django.shortcuts import render


def cart_summary(request):
    return render(request, 'cart_summary.html', {})

# def cart_add(request):
#     return redirect('cart_summary')

# def cart_delete(request):
#     return redirect('cart_summary')

# def cart_update(request):
#     return redirect('cart_summary')