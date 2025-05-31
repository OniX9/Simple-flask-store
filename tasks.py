# import os
# import requests
# from dotenv import load_dotenv
# import jinja2

# load_dotenv()

# domain_name = os.getenv("MAILGUN_DOMAIN")

# template_loader = jinja2.FileSystemLoader("templates")
# template_env = jinja2.Environment(loader= template_loader)


# def render_template(template_filename, **context):
#     return template_env.get_template(template_filename).render(**context)

# def send_email(to_email: str, body:str, subject:str, html:str):
#     url = f"https://api.mailgun.net/v3/{domain_name}/messages"

#     data = {
#         "from": f"SafeCash <mailgun@{domain_name}>",
#         "to": to_email,
#         "subject": subject,
#         "text": body,
#         "html": html
#     }

#     return requests.post(
#         url,
#         data=data, 
#         auth= ("api", os.getenv("MAILGUN_API_KEY"),
#         ),
#     )

 
# def send_user_registered_email(email:str, username: str):
#     print ('TEST Queuing')
#     send_email(
#         email,
#         "Successfully signed up",
#         f"Hi {username}! You have successfully signed up to the Stores REST API.",
#         html= render_template("email/action.html", username= username)
#     )

# def send_message_template(email:str, username:str):
# 	return requests.post(
# 		"https://api.mailgun.net/v3/sandbox6d23c011610646debcdbd332caad4150.mailgun.org/messages",
# 		auth=("api", os.getenv("MAILGUN_API_KEY")),
# 		data={"from": "Mailgun Sandbox <postmaster@sandbox6d23c011610646debcdbd332caad4150.mailgun.org>",
# 			"to": f"{username} <{email}>",
# 			"subject": f"Hello {username}",
# 			"template": "Simple app store",
# 			"h:X-Mailgun-Variables": '{"test": "test"}'
#             })
#     # Send an email using your active template with the above snippet
#     # You can see a record of this email in your logs: https://app.mailgun.com/app/logs.