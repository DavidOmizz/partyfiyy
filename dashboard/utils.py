# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.conf import settings

# def send_registration_email(to_email, user_name):
#     subject = 'Welcome to the OTC Cohort!'
#     plain_message = f"Hi {user_name},\n\nYou've successfully registered for the OTC Cohort, starting on September 9, 2024. We're looking forward to having you on board!\n\nIf you have any questions or need assistance, please don't hesitate to reach out.\n\nBest regards,\nOTC"

#     # Render the HTML template
#     html_message = render_to_string('registration_email.html', {'user_name': user_name})

#     email = EmailMultiAlternatives(
#         subject,
#         plain_message,
#         settings.EMAIL_HOST_USER,
#         [to_email]
#     )

#     # Attach the HTML version of the message
#     email.attach_alternative(html_message, "text/html")

#     # Send the email
#     email.send(fail_silently=False)
