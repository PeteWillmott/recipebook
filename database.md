# Database Schema

The MongoDB database consists of two collections, Recipes and Users.

## Recipes

| Title         |                                                         | Data Type |
| :------------ | :------------------------------------------------------ | --------- |
| _id           |                                                         | ObjectId  |
| recipe        | recipe name                                             | string    |
| prep_time     | preparation time in minutes                             | int32     |
| type          |                                                         | array     |
| - recipe type | breakfast, snack, main meal, dessert, baking (multiple) | string    |
| category      | vegan, vegetarian, omnivore                             | string    |
| difficulty    | scale of 1-3                                            | int32     |
| spicyness     | scale of 1-3                                            | int32     |
| instructions  |                                                         | array     |
| - instruction | step by step instructions                               | string    |
| ingredients   |                                                         | array     |
| - ingredient  | ingredient and amount                                   | string    |
| cook_time     | cooking time in minutes                                 | int32     |
| total_time    | prep_time + cook_time                                   | int32     |
| summary       |                                                         | string    |
| allergens     |                                                         | array     |
| - allergen    | gluten, dairy, eggs, sea food, nuts, alliums (multiple) | string    |
| authorisation |                                                         | boolean   |
| votes         |                                                         | int32     |
| author        | email address of author                                 | string    |
| username      | username of author                                      | string    |
| recipe_code   |                                                         | string    |
| url           |                                                         | string    |



## Users

| Title        |                                 | Data Type |
| :----------- | ------------------------------- | :-------: |
| _id          |                                 | ObjectId  |
| email        |                                 |  string   |
| password     |                                 |  string   |
| username     |                                 |  string   |
| admin        |                                 |  boolean  |
| voted        |                                 |   array   |
| - recipe _id | _id of recipes voted for        |  string   |
| favourites   |                                 |   array   |
| - recipe _id | _id of favourite recipes        |  string   |
| recipe_code  | content of note for that recipe |  string   |

