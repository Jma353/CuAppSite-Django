from .models import Candidate, Trainee, AppDevUser

def generate_random_key(length):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


# Making training program applications 
for i in range(10, 100):
	# User Fields 
	first_name = "User" 
	last_name = str(i)
	email = "usr" + str(i) + "@cornell.edu"
	on_email_list = True
	submitted_tp = True 
	year = 2018
	major = "Computer Science"

	# Trainee Fields 
	highest_cs_course = 1110 
	essay = "This is my essay"
	portfolio_link = "http://www.google.com"
	resume_link = "http://www.google.com"
	access_code = generate_random_key(64)
	score = 0 
	status = ""

	t = Trainee(highest_cs_course=highest_cs_course,
							essay=essay,
							portfolio_link=portfolio_link,
							resume_link=resume_link,
							access_code=access_code,
							score=score,
							status=status)
	t.save() 

	u = AppDevUser(first_name=first_name,
								 last_name=last_name,
								 email=email,
								 on_email_list=on_email_list,
								 submitted_tp=submitted_tp,
								 year=year,
								 major=major,
								 trainee=t)
	u.save() 

