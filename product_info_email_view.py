from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.views.generic.edit import FormView
from email.MIMEImage import MIMEImage
from .forms import ProductInfoEmailForm





class ProductInfoEmail(FormView):
    @method_decorator(csrf_exempt)
    form_class = ProductInfoEmailForm
    success_url = '/product-search/'
    template_name = 'saas_app/search-result.html'
    
    def form_valid(self, form):
        user = UserProfile.objects.get(user=request.user)
        product = Product.objects.get(id=request.GET.get('product_id'))     
        try:
            margin = user.margin
        except:
            margin = 30.0
        price_increased = (product.price * margin) / 100.00
        price = product.price + price_increased
        to_email = [form.cleaned_data['Customer_email']]       
        subject = '%s - %s' % (product.model, product.manufacturer) 
        text_content = render_to_string('saas_app/email/product_info_email.txt')
        html_content = render_to_string('saas_app/email/product_info_email.html',
                                       {'text_content':text_content,
                                        'price':price,
                                        'product':product})
        
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

    return super(ProductInfoEmail, self).form_valid(form)



