#  PlatePal

#### Description:
Platepal is a web based, food diary + meal planning app with help from the spoonacular API.

## Key Features:

### Meal Plan Generator (/planrequest, planrequest.html, planresults.html):
One of Platepal's main features is a meal plan generator which creates a customized 1 day meal plan based on the user's dietary preferences and caloric requirements. Users can specify their target calories for a single day along with any dietary restrictions (e.g., gluten-free, vegetarian) to receive tailored meal suggestions. PlatePal generates 3 meals at a time (breakfast, lunch, and dinner) that will come as close to the caloric target as possible. Each recipe is displayed in a card that tells you the time it takes to prepare along with the number of servings, and includes a link to the full recipe.

These results can be regenerated a limited number of times but this is of course due to the use of the free version of this API. And while this generator is programmed for 1 day meal generation, the webpage is not hardcoded for 3 recipes and can display as many grid cards as recipes that are generated. Spoonacular API can actually generate a week of meals so a future improvement for this feature would be to implement that function and style the page so that the recipes are grouped appropriately by day or meal time. But for the time being I decided to stick with 1 day meal plan because it matches the food diary which is used to record 1 day at a time.


###  Food Diary and Macronutrient Tracking [(/), /search, /add, and index.html]:
PlatePal's food diary feature allows users to easily track their daily food intake. Using the search page, users can look up any food item they consumed during the day. After finding the desired food item, users can input the specific serving size, such as grams or cups. Once the serving size is entered, users can save the food item to their daily food log. The food log displays detailed nutritional information for each food item added by the user. This includes the exact amount of calories, carbohydrates, protein, and fat based on the specified serving size. With PlatePal's food diary, users can effortlessly monitor their nutritional intake and make informed decisions about their diet. This feature uses two endpoints, the first one is used when the user searches the food by keyword. Part of the response for this endpoing is spoonaculars ID number for each food result. This endpoint however does not also give the nutrient breakdown for each food so I use the second endpoint to search for the nutrient values as this endpoint only takes ID number and not keywords. Failed API requests render an apology page similar to the one from the finance pset. I started this project using USDA's Food Data Central API however a major issue I encountered with that was that while I was able to find very accurate values of macro and micronutrients; the API documentation was not clear in what kind of parameters I could use with each endpoint which made it very difficult to find relevant information such as the serving size that those nutrient values were based on. Obviously then the values that I was able to find were not of much help for the user and I found spoonaculars API which had much better documentation for each endpoint as well as other fun features like the meal plan generator.

In regards to data management I decided to use a Sqlite3 database to save all the history and food diary entries. At first I thought about using a list of dictionaries, but overall the database path was much more robust for example in terms of data integrity because of unique constraints, foreign key constraints, and data type constraints. This helps maintain data quality and prevents inconsistencies or errors in the data. Using SQl queries was also just  simpler and more flexible in terms of getting the information I needed. Lastly in terms of scalability of course databases are meant to handle large volumes of data which makes this a much stronger choice for maintenance and efficiency down the line.

### History (/history and history.html):
Maintains a history of users' food entries, allowing them to review past activity and track their progress towards their health goals. This page simply queries a table of all food items that have been added to the food diary and displays a table similar to the food diary page but also includes a column for date added. It also features a quick add button for each entry allowing users to input the serving size and add that food to the current daily log in the same way as the search page.

While the history page does include a quick add feature for recent searches, this could further be improved by being able to save favourite foods and even favourite recipes from the meal plan generator. The current page does show the same details as the food diary page plus the date it was added, but another useful feature would be showing the total macronutrient values of each recorded day.

### Fun (/fun, /joke, /trivia and fun.html, joke.html, trivia.html):
This page shows two options one for a food related joke, and one for a food related trivia fact. Pressing any button sends a corresponding spoonacular API request for either one. The response is shown on a new page with a button at the bottom to return to the main fun page.

## Future Features:
These are some things that I would like to add in the future.

### Barcode scanner:
One useful feature of many popular diet trackers is barcode scanning to automatically add food items and nutrient values straight from the label. This would require the use of another API.

### Enhanced User Profiles:
Creating a user profile page to customize their and set personalized goals.

### Data Visualisation:
Providing visual representations of users' dietary data, such as charts and graphs, to help users analyze their eating habits and identify areas for improvement. especially relevant for those on specific diets like low carb/no carb, high protein.
