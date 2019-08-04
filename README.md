

# Milestone 3

## [Pete's Cookbook]([http://petes-cookbook.herokuapp.com](http://petes-cookbook.herokuapp.com/)) ![logo](/static/images/logo.png)

Pete's cookbook is user driven recipe project with the potential to expand into a social network for like minded enthusiasts. 

Users are able to browse and search the site reading any of the recipes without requiring to register. Members can add their own recipes, select favourites and upvote recipes they like, they may also edit their recipes later if required. Members may also annotate the recipes, perhaps noting substitute ingredients or unit conversions but limited only by their needs and imagination.

## Table of Contents

1. UX
2. Features
3. Technologies Used
4. Testing
5. Database
6. Deployment
7. Credits

## UX

### User Goals

The user is envisioned as a cooking enthusiast or home cook rather than a professional chef. The site aims to provide:

- An easy to view collection of recipes for use and inspiration.
- A platform to showcase your creativity as a cook by adding my recipes. 
- The ability to note any changes to the recipe to make it better suit my needs, eg substituting ingredients to suit personal taste or food restrictions or changing units.

### Business Goals

As the site currently exists there is no business but the design process has been conducted as if there were and further thoughts about how this could be developed will be touched upon in the Features to Implement section.

With two basic methodologies in mind this site could easily become either a user owned recipe exchange social networking site or with the addition of either adverts or with premium content a pay to use site. In either case certain probable criteria for the site owner were established.

As the site owner I want:

- An easy to navigate site that will display my content to visitors.
- A straightforward way of entering my content.
- The ability to manage my content in a simple and rapid manner, to deal with inappropriate content copyright concerns and such like.
- Value for money. Since the business behind this site is notional this aspect has not been addressed but it should be noted that in a real world setting it would be of great importance.

### Planning

Looking at these two sets of goals allowed me to settle the top level design. Strategically the site must:

- Permit the display, storage and creation of recipes. 
- Arrange the recipes in such a way they can be searched returning only those those that fit the user's criteria.
- Provide a way for the recipe owner and the site owner to edit recipes.

Clearly a database is the simplest way to store and filter all the required information. Going back to the goals and thinking about the user the following user stories were scoped.

- As the business owner I want to be able to edit recipes.
- As the business owner I want to be able to preview new content.
- As the business owner I want to know who is using the site.
- As the business owner I want to be able to add new content.
- As a user I want to be able to search recipes to specific criteria.
- As a user I want tot be able to browse for inspiration.
- As a user I want to view recipes.
- As a user I want to annotate recipes.
- As a user I want to share my own recipes.
- As a user I want to be able to mark my favourite recipes for easy access later.
- As a user I want to be able to upvote recipes I like.

Structurally a fairly linear scheme seemed the best fit with three main sections, an open area where recipes can be searched and viewed, a registered area where recipes can be added, edited, annotated, marked and upvoted, and finally an admin area where recipes and users can be reviewed and edited.  This permitted the maximum freedom to the end user to use the site their way with access controls designed to gently remind people to login without taking them away from the page they were on, in so far as possible. Modals were considered as a seamless way of doing this but ultimately rejected since they do not always interact gracefully with pop up blockers.

I decided to use a MongoDB Atlas database, it seems probable a recipe web app could function with either a SQL or NoSQL database but as I am creating only two database driven projects for this course and the other is created with Django where a SQL database will integrate more gracefully this project seemed the best chance to demonstrate my capabilities with NoSql databases. The database schema can be found [here](database.md). The milestone guidelines have since been changed to clarify this project should use a NoSQL database.

To allow the navigation to be simple and intuative a familiar top navigation was selected with options being removed where not required or inappropriate. For example a logged in user will not planning to register so the link is removed. likewise the link to the admin dashboard only appears after an admin login is recognised. The footer links are identical throughout and until the user logs in the log in form is present above the footer, except on the registration page. Since the site allows non users to browse and only requires log in for certain sections it was desirable to make the user experience as smooth as possible while transitioning from open areas to sections where a log in was required and so a repeated form was used in place of a specific log in page.

While considering the interface design and looking forwards to design ideas for the surface level found myself thinking as much of printed cookbooks as of recipe websites which formed an inital design idea of an old fashioned cookbook with the sort of familiar old fashioned recipes. While ultimately this was discarded as something that was best left to ebook readers and traditional publishers it did influence the visual design of the site. The colour scheme reflects a leather bound book with gold lettering though only the titles retain the original cursive style as sans serif is simply more readable. Likewise away from the index page the colour scheme is remanisant of ink on old paper and gives good contrast and readability., while the brown of the index page body reflects the front cover of a book.

Balsamic [wireframes](https://petes-gp-bucket.s3.eu-central-1.amazonaws.com/milestone3.bmpr)

## Features

### Existing Features

#### Standard Features

The top navigation and footer are standard on all pages. The **registration** and **admin** links appear only when required. If the user if logged in the **register** link will not be displayed and the **admin ** link will only display when the logged in user has admin priviledges.

The login form will be replaced by a log out button when a registered user logs in.

The footer with its social media links and mail link is a constant fixture placed to meet expectations that contat and social media links will be at the foot of the page.

#### Index

The main image of the index page is the image provided for the recipe with the most votes. Either below, in mobile, or beside on a desktop view are the three next most popular recipies.

#### Browse

This along with the search page is the main workhorse of this site allowing users in search of inspiration to click their way through recipes until they see something that tickles their fancy. Logged in users will be reminded of things they have liked by favourite and like icons. To ensure they areboth visible and evident to a new user the next and previous buttons are placed high on the page. The darkening background emphasising that they should be clicked.

##### Individual Recipe Pages

The recipes layout in a simple and clear form the ingredients and the method.
When the user is logged in they may mark a recipe as a **favourite** or **like** to upvote a recipe. They may also **add note** to create a note that will be displayed for them with the recipe in future. Alowing a user to 'pencil in' and helpful notes and modifications. 

##### Edit Recipe

The recipe's author, and any admins, may edit a recipe. This page follows the style of the add recipe page for ease of use. It is currently set so that an authorised recipe remains authorised even after editing, though it would be very easy to enforce re-authorisation be modiying the **update_recipe** function to unset the authorisation on editing. This has not been done since having recipes 'disappear and reappear' would irritate other users.

#### Register

The registration form is vertically stacked for ease of reading and use. It uses email address as the unique identifier as some users struggle to remember user names but most will remeber their email. Since logging in occurs automatically as part of registering there is no need for a login form on this page. It also removes a potential source of confusion for less experienced users if there are not two forms both asking for email and password in such close proximity. This also removes one point of potential faliure since it prevents a logged in user trying to register with the same credentials.

#### Favourites

Essentially taking the role of a bookmark this page is minimalist in its styling giving the user an uninterupted route directly to their choosen recipes. 

#### Add

The add recipe page sets the pattern that a user may later use to edit their recipes allowing them to learn the system as they share their first recipe.

Again the form is simply laid out without distractions to facilitate ease of use with the inputs set over each other to guide the eye in a simple downwards path without having to scan back and forth all the time.

#### Search

Along with **browse** the main component of the user interface allowing those users that don't wish to 'thumb through' a list of possibilities but go direct to what they need a direct route to a specific subset of recipes. With several filters they can select from as well as the option of selecting a specific ingredient.

A text input here had the potential to cause poor user experience as any free text is prone to mistakes, especially on devices with smaller keyboards. Early versions of the site had a **main ingredient** category for each recipe and while this worked well for searching it was clumbersome to use in adding a recipe. It was quite intuative when searching but when entering a recipe there were times it was not clear which ingredients were the important ones and the feature would not work as well for searching if every ingredient were added as a main ingredient. So that category was removed from the database and the templates and autocompletion was considered to reduce Adminthe chance of typos while avoiding a huge drop down list. The **datalist** element prooved ideal for this role.

#### Admin

The admin dashboard gives access to three menus for:

- Authorising new recipes.
- Administering users
- Adminstering recipes

The visual design is very simple so as not to distract from the data while maintaining the design and familiar layout of the site.

### Features to Implement

Emailing activation codes after registration would be desirable given the difficulties of seperating well formatted fake email addresses from real ones with form validation. For example one of the registered users of the site has an email address ending @testemail.com

In a related vein it would be desirable to have minimum standards set for passwords as well.

Email alert to admin on new recipes being added, Flask-Mail would do this but it seems ( https://pythonprogramming.net/flask-email-tutorial/ ) this would require setting my gmail account to be less than secure. With the site set on a commercial footing and running a mail server and not relying on my personal email account this shouldn't be a problem. A further consideration is that might be better not to have admin approval of new recipes, but without an actual site owner it is difficult to know where the correct balance between control of the site content and administrator workload lies. 

Since the author is displayed with each recipe it might be desirable when time permits to add a feature allowing the user to view other recipes by that author. Similarly if it were desired this could be one logical entry into some form of social exchange if the site were to be developed in that direction.

## Technologies Used

### Languages

The logic of the app was created in Python with templates written in HTML, styled with SCSS and a little JavaScript.

### Libraries

[JQuery](https://jquery.com/) was used to simplify DOM manipulation.
[Bootstrap](https://getbootstrap.com/docs/3.4/) was used to simplify the SCSS.
[Font Aweseome](https://fontawesome.com/) was used for icons.
[Flask](https://flask.palletsprojects.com/en/1.0.x/) was used to render templates.
[Flask PyMongo](https://flask-pymongo.readthedocs.io/en/latest/) and [PyMongo](https://api.mongodb.com/python/current/) were jointly used faciltate communication between Python and MongoDB.
[Google Fonts](https://fonts.google.com/) was used to provide fonts.

### Tools

[VSCode](https://code.visualstudio.com/) was my IDE after switching from Cloud9.
[PIP](https://pip.pypa.io/en/stable/installing/) was used to install tools.
[Git](https://gist.github.com/derhuerst/1b15ff4652a867391f03) was used for version control.
[GitHub](https://github.com/) was used to store the project and make it avvailable remotely.
[MongoDB Atlas](https://www.mongodb.com/cloud/atlas) was the database used for this project.
[Balsamic](https://balsamiq.com/) was used for wireframes during the design of this project.


## Testing

The code was tested and validated and the site manually checked on a range of devices and screen sizes, additionally my friends and family were asked to test the site and pass along any observations and critique.

The test results section can be found [here](testing.md).

## Database

As mentioned in the **UX** and **Technologies Used** sections a MongoDB Atlas database was used. The deatails of the two collections in the database can be found [here](database.md).

## Deployment

### GitHub

#### GitHub repository - https://github.com/PeteWillmott/recipebook

To run locally you can either download direct from GitHub, using the green "Clone or download" button, or clone by entering `git clone https://github.com/PeteWillmott/recipebook`. To sever the link to my repository use the command `git remote rm origin`. 

The exact details of how to proceed from this point will depend on your IDE.

1. Unzip the zip file if you downloaded the project.
2. Ensure python 3 is [downloaded](https://www.python.org/downloads/). 
3. A virtual environment is recommended, I ran the following command `python -m venv env`
4. Activate your virtual environment, in my case that meant running first `Python: Select Interpreter`and then `Terminal: Create New Integrated Terminal`in the command palette , again this may vary by IDE.
5. When your environment is set up run `pip -r requirements.txt`you may need to run `pip install --upgrade pip`
6. create a `.env` file inside it create a MONGODB_URI and SECRET_KEY
7. In mongoDB database create a database called `project` with two collections `recipe` and `users` the specifics of the collections can be found in the [database schema](database.md). Details on setting up a mongoDB database can be found at https://www.mongodb.com/cloud/atlas if required.
8. You should now be able to run the app with `flask -m flask run` or the equivalent for your IDE. The app should now be running at `http://127.0.0.1:5000`.



### Heroku

#### Heroku Deployment - http://petes-cookbook.herokuapp.com/

To deploy to [Heroku]( https://www.heroku.com/), create an account if you don't have one.

1. Create a `requirements.txt` file using the `pip freeze > requirements.txt` command.

2. create a `Procfile` with the command `echo web: python app.py > Procfile` in the terminal.

3. `git add ` any unstaged files, `git commit` the project and `git push` to heroku or to GitHub. Deploying to GitHub allows updates to implement directly from GitHub when pushed.

4. Create a new app on Heroku with the "New" button, name it and set the region appropriately. If deploying from GitHub select "GitHub" from "Deploy > Deployment method"

5. In the dashboard for your app select  "Settings > Reveal Config Vars".

   DEBUG to FALSE

   IP to 0.0.0.0

   PORT to 5000

   SECRET_KEY to your secret_key variable

   MONGO_URI to the connection string provided by mongoDB. 

   (The connection tab of the cluster menu provides the required information)

6. From "Manual deploy > Deploy Branch". Your application is now deployed.

## Credits

### Content

The site text is my own and all recipes entered by the user Fred are recipes that have been in the family for long enough their original provenance is unclear.

### Media

The logo was drawn for me by my daughter, other images were found with google searches and linked to directly, with the exception of the staffordshire oatcake image which is linked to from my s3 bucket as I could not directly link to the image just the page.