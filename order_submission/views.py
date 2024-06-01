from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from .forms import ShippingForm
from django.http import HttpResponse
from carts.views import _cart_id
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from carts.models import Cart, CartItem
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def shipping_form(request):
	if request.method == 'POST':
		form = ShippingForm(request.POST)
		if form.is_valid():
			# process form data
			subject = "New Shipping Form"
			from_email = 'confidentpalace@gmail.com'
			recipient_list = [settings.EMAIL_HOST_USER]
			#gather form data
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			address = form.cleaned_data['address']
			email = form.cleaned_data['email']
			phone_number = form.cleaned_data['phone_number']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			country = form.cleaned_data['country']

			# retrieve cart items
			# cart_items = CartItem.objects.filter(user=request.user, status='active')
			# cart_items = CartItem()
			cart = Cart.objects.get(cart_id=_cart_id(request))
			cart_items = CartItem.objects.filter(cart=cart, is_active=True)
			cart_items_info = '\n'.join([f"{cart_item.product.product_name}\nQuantity: { cart_item.quantity }" for cart_item in cart_items])
			# grand_total = cart.grand_total()

			# cart_items = CartItem.objects.filter(cart=cart, is_active=True)

			message = f"""
			First Name: {first_name}
			Last Name: {last_name}
			Address: {address}
			City: {city}
			State: {state}
			Country: {country}
			Phone Number: {phone_number}
			Email: {email}

			Cart Items:
			{cart_items_info}
			"""

			try:
				send_mail(subject, message, from_email, recipient_list)

			except BadHeaderError:
				return HttpResponse('Invalid header Found')

			except Exception as e:
				return HttpResponse(f'An error occured: {e}')

			return redirect('success')							


			# email_subject = 'Your Order Details'
			# email_template = 'store/order_email.html'
			# context = {'first_name': first_name, 'last_name': last_name, 'email': email, 'address': address, 'city': city, 'state': state, 'country': country, 'cart_items': cart_items}
			# email_content_html = render_to_string(email_template, context)
			# email_content_text = strip_tags(email_content_html)
			# # send email to website owner
			# subject = 'New Shipping Form'



			# send_mail(
			# 	email_subject,
			# 	email_content_text,
			# 	'lemoaremu@gmail.com',  # Replace with your sender email address
			# 	[email],  # Send email to the user's email address
			# 	html_message=email_content_html,  # Include HTML content in the email
			# )
			
			# message = f'First Name: {first_name}\nLast name: {last_name}\nAddress: {address}\nEmail: {email}\nphone number: {phone_number}\nCity: {city}\nState: {state}\nCountry: {country}'

			# recipient_list = [settings.EMAIL_HOST_USER]

			# send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
			# 	# 'yourwebsite@gmail.com',
			# 	# ['thetechguyneedsjob@gmail.com'],

			# 	# fail_silently=False

		else:
			form = ShippingForm()
			return render(request, 'store/checkout.html', {'cart_items': cart_items, 'error_message': 'Please fill in all required fields'})


		# cart_items = Cart.objects.filter(user=request.user, status='active'
	return render(request, "store/checkout.html", {'cart_items': cart_items, 'form': form})

@login_required(login_url='login')
def success_view(request):
	return render(request, "store/success.html")
