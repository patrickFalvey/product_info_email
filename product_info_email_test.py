from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from email.MIMEImage import MIMEImage
from .forms import product_info_email_form



@csrf_exempt
def product_info_email(request):
    
    email_form = product_info_email_form(request.POST or None)
    
    if form.is_valid():

        ## Organize Product Info
        user = UserProfile.objects.get(user=request.user)
        product = Product.objects.get(id=request.GET.get('product_id'))
        
        try:
            margin = user.margin
        except:
            margin = 30.0
        price_increased = (product.price * margin) / 100.00
        price = product.price + price_increased

        ## Create & Send Email
        to_email = [form.cleaned_data['Customer_email']]       
        subject = '%s - %s' % (product.model, product.manufacturer) 
        text_content = render_to_string('saas_app/email/product_info_email.txt')
        html_content = render_to_string('saas_app/email/product_info_email.html', {'text_content':text_content,
                                                                                   'product':product,
                                                                                   'price':price})
        msg = EmailMultiAlternatives(subject,
                                     text_content,
                                     [user.email],
                                     to_email)
        
        msg.attach_alternative(html_content, 'text/html')
        msg.mixed_subtype = 'related'
        img_content_id = 'product'
        img_data = open(product.image_url(), 'rb')
        msg_img = MIMEImage(img_data.read())
        img_data.close()
        msg_img.add_header('Content-ID', '<{}>'.format(product.picture))
        msg.attach(msg_img)
        msg.send()        

    return render(request,'saas_app/product-search-result.html',{'email_form':email_form,})



