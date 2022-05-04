
## Main purpose:
Provide an opportunity for users to read and write reviews on the movies of interest.
____
## Key concepts:
* Movies are added to the database by the admin;
* Published movies can be found at "Recent", "Popular" and "Best rated" pages. Every page contains list of published movies sorted by appropriate key. Published movies can be reviewed;
* Besides that, every movie (anticipated or published) can be found via site search. Searching system can be used in 2 ways:
* By typing a request into the search bar. In this case the search is carried out in all categories (movie title, director name, writer name, actor name, genre and release year). It means that, if "Fight club" is typed, list of results will contain all movies having "Fight club" in it's title;
* By clicking director, writer, actor, country, genre or release year links. In this case search is carried out in a specific category. For example, if some movie is released in 2000 year, and "2000" year link is clicked, list of results will only contain movies released in this year;
* Non-authenticated users can read movie info, description and reviews, but they can't write reviews;
* Authenticated users can write reviews, edit or delete them. Every authenticated user has a limit of maximum one review per movie;
* After any authentication action (registration, login or logout) user will be redirected to his previous page.
____
## To run application on local machine:
1. Clone the repository:
```git clone https://github.com/Kirastel/films_review.git && cd films_review```


2. Create a virtual environment:
```python3 -m venv venv```

3. Activate the virtual environment:
```source venv/bin/activate```

4. Install all required dependencies:
```pip install -r requirements.txt```

5. Collect static files:
```python manage.py collectstatic```

6. Apply the migrations:
```python manage.py migrate```

7. Create superuser:
```python manage.py createsuperuser```

8. Run server:
```python manage.py runserver```

9. From now local version is available at ```http://localhost:8000```
