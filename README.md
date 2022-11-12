# Project Introduction
'AjkeKiKorbo'(An English translation would be 'What to do today?') is an app that lets you plan your day(and the next) and help you achieve your goals by keeping track of the tasks that you complete and the tasks that are yet to be completed. You can generalize this as a 'todo' app. However, what makes this better is that this app can track your progress and let you see how you've been doing in the past. There is a reminder feature as well, where you can have as many reminders as you want and the app will show them to you in various pages in a random order. That's pretty much it, even tho 
there are some other stuff going on.


# Features Explanation
Here are the primary features that the application offers.

## Tasks For Today
In the 'today's-task' page, you can see the tasks for today. You can add/delete tasks as you please. You can see the pending and the completed tasks in two different columns and in another column, you can view your yesterday's performance which might come handy at times. Tho I admit it's something
not necessary to have in the today's tasks page. 

## Tasks For Tomorrow
Like people normally plan their day the night before(or anytime you please), the app lets you plan your next day in advance and those tasks will be your today's tasks after midnight. And the tasks you already had for today will be gone. Well, not 'gone'. They will be stored in the database and you
can access them anytime you want.

## Progress 
The most interesting part of this application I think is the progress feature. By default you can see how you've been doing this month and if you wish you can see your progress of some other month, given that you used the app in that month. On the left you have some tabular data telling you
how much you've completed and an automated verdict that sort of tells you how you've performed. On the right, you have a graph that shows you your 
performance in a bar graph. The graph also has nice animations which makes this page look really nice. Shout out to chart.js for helping me out
with this. The graphing part would have been a nightmare if this framework didn't exist. 

## Details of A Particular Day
In the progress bar, you can click on a date and that will take you to a page where you can see how you've performed that day. All the tasks that you
did and the ones that you did not will be in front of you. It's not a necessary feature to have but doesn't hurt to have, does it? Might come in handy sometimes as well.

## Reminders
This is something I personally added for me(Since I deployed the app and will be using myself), I wanted to have some reminders shown to me throughout the application randomly and this feature serves the purpose of that. You can have any reminders you want, as many as you want. They will
be shown to you. Automation is nice, innit?

## Reviews
This is something that I hope would increase the user experience. Though reviews, users can let me know anything they want, be it a bug or an idea or whatever. I used javascript to do this part completely client-side. You can see a small animation of a confirmation message as well once you submit a review.

## Email Features
I had some fancier idea in mind but looked like I needed to learn celery or something similar to accomplish that so I ended up sending confirmation and welcome messages to users upon registration. Haha, being 100% honest here. The fact that we start some project with high hopes and ideas and lose motivation midway is real and brutal.

## Proper Functionality For All Time-zones Around The World
This is something I realized I had to implement after deploying the app and this is something that caused me some pain. The server is running at UTC
timezone but the users needed differnet timezones according to where they live, for this application to run properly. Cause the tasks should switch at midnight remember? How can we do that flawlessly if we didn't have differnt timezones? I took leverage from datetime, calender, pytz etc to accomplish this feature. 


# Other Requirements:
Here are some other requirements that were mentioned in the project specifications.

## Distinctiveness and Complexity
It's needless to say the this application is very distinctive from other projects so let's talk about the complexity now. 

First of all, it wasn't easy for me to figure out how to flawlessly distinguish the today's tasks with the ones of tomorrow. I had to give this a lot of thought to eventually come up with the ideas of using python modules. I have put so much effort into making the app as nice and responsive as I could since I had the intention of deploying it and letting my friends use it. In the review section I did all of that client-side work using vanilla JS and that was not something simple. I had to figure out how to make the animation happen again without the user having to reload the page. The progress feature took a lot of effort into thinking and building that up. I had to research so much about graphs and stuff and finally chart.js came in for the rescure. I had to use different timezones for users all over the world and that took me so much time to implement. I also have this email feature and that took a lot of research as well since I used environment variables and all that to make this as secure as possible. Had to come up with styling ideas for the placements of the reminders. With client-side validation, I had server side validation for each and every post request. I used a custom 404 error template just to make this more professional. You need to turn debug = False in settings.py to view that. Since I wanted to publish the app, I had to make sure the code was efficient enough so that took a lot of effort as well. Finally I invested a lot of time into researching about hosting services and finally chose pythonanywhere.

Many other things are going on under the hood and I can't even remember anything else right now but I assure you, this was complex enough to be a final project of this effortful course and I'm really proud of this application.

## What Each Files Contain
I have only one app in this project and that takes care of pretty much everything. The template and the views outside of the app directory takes care of the custom 404 not found page. I have all the required things in requirements.txt and I have my environment variables in gitignore. That's 
pretty much it. I think you can just have a look and understand what the rest of the files are doing.

## How to Run The Application
Locally, 'python manage.py runserver' should get you up and running. However read the next part if you do not wanna run this locally.

# The Application is Live!
The good news is the application is live at ajkekikorbo.pythonanywhere.com!! This todo app is designed for solo use only(not for teams). So if you like all the features that I added and appreciate the effort, feel free to use the app in your everyday life.

Unfortunately tho, I used this using a free account so they don't really offer that much processing power so writing to the database(sometimes reading too) can be a bit sluggish but it's not something that will enrage you so don't worry too much about that. 


# Ending
Wow!! What an amazing course you guys provided. Really thankful to the CS50 team, specially, Brian and David. You guys are making people's lives easier and I'm grateful and thankful to you and to the rest of the staff for making this possible. I learned a ton. Thank you again. Have a good one!


