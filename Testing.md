# Testing

## HTML

HTML validated with W3 [validator](https://www.w3schools.com/) with only warnings on section elements without heading elements for the flash messages and login sections.

W3 link [validation](https://validator.w3.org/checklink), all links validate, with the exception that the link checker will not check the Facebook link because of robot exclusion rules or mailto links because of the link checker's own rules..

### Manual Testing

The following features were checked on these pages.

#### Index

- Login

  Flash message appears after login.

  The eye icon toggles the password from obscured to visible.

- Logout

- Links

  Footer links open a new window or open an email window. They don't open social media pages only the respective home pages since there is no company.

  Recipe links all open to the correct recipes.

#### Browse

- Login

  Extra features appear, favourites and likes, after login.

- Logout

- Links

  As per index.

- Next

  Tested through the collection all the way back to the start.

- Previous

  Tested through the collection all the way back to the start.

#### Recipes

- Login

  Extra features appear, edit (if author or admin), like, favourite, add notes.

- Logout

- Links

  As per index.

#### Edit Recipe

- Logout

- Like and favourites are displayed.

- Links

  As per index.

- Update recipes

  Unchanged values remain as set and new values are stored.

  Preparation and cooking time will not accept non numeric input. Times can be entered by keyboard or up and down arrows. Negative times are not allowed, nor are values of over 59 minutes.

#### Register

- Links

  As per index.

- Form

  Email requires an @ to validate, the eye icon toggles the password from obscured to visible.

#### Favourites

- Access control, log in access only.

- Links

  As per index.

#### Add Recipe

- Access control, log in access only.

- Links

  As per index.

- Add recipe form

  Preparation and cooking time will not accept non numeric input. Times can be entered by keyboard or up and down arrows. Negative times are not allowed, nor are values of over 59 minutes.

  On text inputs return does not submit.

#### Search

- Login

- Logout

- Links

  As per index.

- Form

  Ingredients auto suggests from the datalist.

  Searches return the expected values, a search on an empty form returns all recipes.

#### Admin

- Authorisation 

  Unauthorised recipes are displayed and can be authorised, edited or deleted.

- Users

  Users are displayed, can be set as user or admin or deleted.

- Recipes

  All recipes are listed and can be edited or deleted.



## CSS

CSS validated with [Jigsaw](https://jigsaw.w3.org/css-validator/validator.html.en) and passed as CSS level 3 + SVG with 16 warnings on main.css. 1 warning on the font import and 15 on vendor extensions. The numerous warnings on vendor CSS have been ignored.

## Python

Flake8 for style suggestions and pylint used with VSCode IDE.

All routes correctly display and link to the appropriate things via url_for().

Admin only or user only views can only be viewed when logged in appropriately and times are converted proving correct functioning of is_user, is_admin and hrs_to_mins.

Recipes were added via the app and consequently the functions of the queries are well tested.

## JavaScript

Index.js and recipeCard.js have been proved by both addition of recipes and testing of other features.