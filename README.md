[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/jMyw1QQk)
# Homework 6: Building an interactive web application

In this homework, your task will be to build an interactive web application, using a couple of Web APIs. In contrast to the class, project, where the work has to be driven by a problem or possibility that _you_ define, in this homework, the end-product is mostly pre-defined for you.

For this homework, instead of directly using web APIs (as we did in HW 5), we will use wrapper Python modules for the corresponding APIs. As a reminder, wrapper modules are ones that hide away some low-level details of working with an API.

> _Note: Compared to the previous homework assignments, there will be less detailed instructions on how to complete tasks in this homework. Most of the instructions are on this file, and the source files do not have detailed instructions. As a result of this, and the fact that we are quite close to the end-of-quarter, it is even more important for you to get started on this homework as soon as you can._

## The end-product

For a successful submission for this homework, you will produce a web application that gives users a list of Wikipedia articles on topics which are geographically close to a point (address, name of a place) that they specify. In other words, a given user comes to the web app, inputs the name of a location or an address. Your app will return a list of Wikipedia articles (with their summaries) that are about topics that are geographically close to what the user inputted in a search results page. If no results are found for any reason, the search results page will show an error message.

This builds on some of the conceptual ideas that we saw in HW4, but it involves using a different set of techniques, and the end-product will be interactive.  

## Modules you will need to use

Apart from Flask, you will need to use two more modules to interact with a couple of Web APIs.

### Wikipedia

The [Wikipedia](https://wikipedia.readthedocs.io/en/latest/) module in Python gives you basic access to access data from Wikipedia.

### GeoPy

[GeoPy](https://geopy.readthedocs.io/en/stable/) gives you access to a range of Web APIs which let you _geocode_, or figure out the latitude/longitude, of a given address. For example, geocoding `University of Washington` should give me `47.65435, -122.30806`, which are the latitude and longitudes of the UW campus.

GeoPy enables access to a range of different Web APIs that do the same thing, i.e., geocoding. This is useful as some Web APIs may work better or worse along certain dimensions which may be better or worse suited for your application's needs. The GeoPy documentation has a [helpful diagram](https://geopy.readthedocs.io/en/stable/#geopy-is-not-a-service) that illustrates this. For this homework, we will be using the [_Nominatim_ geocoder](https://nominatim.org/) that is supported by GeoPy. Nominatim is free-to-use, but restricts how often you can query the servers in a given period of time (which should be fine for a homework project).

## Getting started: Task 0

> Reference: The “Managing external modules in your Python projects” article on Canvas.

To get started, create a Python virtual environment called `venv` in this directory (the one that you cloned from Github). Activate the virtual environment, and then install the following Python modules with `pip`.
 
 - `flask`
 - `wikipedia`
 - `geopy`

Record the modules that you installed to the `requirements.txt` file. Add the and commit this file to Git. If you are successful, the file should look something like this (it may look different depending on your development editor, but at least there should be lines that start with `Flask`, `wikipedia`, and `geopy`).

```
beautifulsoup4==4.11.2
certifi==2022.12.7
charset-normalizer==3.0.1
click==8.1.3
Flask==2.2.3
geographiclib==2.0
geopy==2.3.0
idna==3.4
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.2
requests==2.28.2
soupsieve==2.4
urllib3==1.26.14
Werkzeug==2.2.3
wikipedia==1.4.0
```

## Task 1: Defining the functions

The next task is to define the functions that you are going to use, all of them in the file `functions.py`. The functions that you need to define are:

### `geocode(place)`

#### Parameters:

* `place`: A string that denotes the name of a place, or an address (e.g., "University of Washington" or "1410 NE Campus Parkway, Seattle, WA 98195") for which the latitude and longitude should be returned.

#### Returns

`geocode(place)` return the latitude-longitude pair for place as a Python _tuple_, or None if no results are found.

#### Implementation details

To implement `geocode()` you will need to create an instance of the [`Nominatim` class](https://geopy.readthedocs.io/en/stable/#nominatim) that is offered by the `geopy` module. The class definition is already imported for you in the file, you need to create an instance, and then call the [`.geocode()` method](https://geopy.readthedocs.io/en/stable/#geopy.geocoders.Nominatim.geocode) on it with the appropriate arguments. For an example, take a look at the [Geocoders section](https://geopy.readthedocs.io/en/stable/#module-geopy.geocoders) of the geopy documentation.

__Important Note:__ The constructor of the _Nominatim_ class takes a `user_agent` parameter. Set that to the string `Learning Python` (or something similar such as `Learning Flask` that is not the default value).

### `wikipedia_locationsearch(place, max_results=10, radius=2.0, sort=False)` 

#### Parameters
 
 * `place`: A string that denotes the name of a place, or an address (e.g., "University of Washington" or "1410 NE Campus Parkway, Seattle, WA 98195") around which the search results should be returned.
 * `max_results`: An integer that denotes the maximum number of results that should be returned by the function. Default value: 10.
 * `radius`: A float that denotes the number of miles within which the search results should be restricted. Default value: 2.0
 * `sort`: A boolean value indicating whether the results should be sorted by the length of the articles or not. Default value: False.

#### Returns

 A list of [`wikipedia.WikipediaPage`](https://wikipedia.readthedocs.io/en/latest/code.html#wikipedia.WikipediaPage) objects that match the search parameters. If no results are found, either while trying to convert the place name to a latitude longitude pair, or from the Wikipedia search, a blank list (`[]`) should be returned.

#### Implementation details

In this function, you need to

 1. Call the previously defined `geocode()` function with the value of the place parameter to get the latitude and longitude. Return the appropriate value if no latitude and longitude could be found.
 2. Call the `wikipedia.geosearch()` method to get the results. Some arguments to `wikipedia.geosearch()` will come from the parameters of this function (e.g., `max_results` of this function will map to `results` of `wikipedia.geosearch()`). Make sure you pass those accordingly. Also make sure that you convert the unit of `radius`; this function expects miles, whereas `wikipedia.geosearch()` expects meters. Further, the `wikipedia.geosearch()` function expect `radius` to be an integer, so you should call Python's `round()` function to the converted value to make sure that it is an integer. For reference, there are approximately 1609 meters in a mile (approximation is okay here).
 3. The `wikipedia.geosearch()` function returns a list of page titles (strings). Generate a list of instances of `wikipedia.WikipediaPage` from the page title list using list comprehension.
 4. If `sort` is `True`, use [`sorted()`](https://docs.python.org/3/library/functions.html#sorted) (which we covered in class) to sort the results by length of the pages. To do this you can
    1. Define a function that returns the page length of a supplied `wikipedia.WikipediaPage` object. To access the content of the page, you can access the [`.content` attribute](https://wikipedia.readthedocs.io/en/latest/code.html#wikipedia.WikipediaPage.content) and use `len()` to get the length of the content.
    2. Use the `key` parameter for `sorted()` to use this function and sort the list by content. Note that the sort order should be longest-article-first.
 5. Return the finalized list.

### Testing the functions

If all goes well, if you run the file, you should get an output that looks something like the following (it may look a little different as Wikipedia articles are being updated all the time).

```
-- Trying to find the latitude and longitude of UW --
(47.6543466, -122.30806059473039)
-- Trying to find the latitude and longitude of a non-existent place --
None
-- Getting 5 articles close to UW --
Content length	URL
45025		https://en.wikipedia.org/wiki/University_of_Washington
3313		https://en.wikipedia.org/wiki/University_of_Washington_College_of_Arts_and_Sciences
8521		https://en.wikipedia.org/wiki/University_of_Washington_Information_School
822		https://en.wikipedia.org/wiki/Drumheller_Fountain
15959		https://en.wikipedia.org/wiki/Alaska%E2%80%93Yukon%E2%80%93Pacific_Exposition
-- Getting 5 articles close to UW (sorted by article length, longest first) --
Content length	URL
45025		https://en.wikipedia.org/wiki/University_of_Washington
15959		https://en.wikipedia.org/wiki/Alaska%E2%80%93Yukon%E2%80%93Pacific_Exposition
8521		https://en.wikipedia.org/wiki/University_of_Washington_Information_School
3313		https://en.wikipedia.org/wiki/University_of_Washington_College_of_Arts_and_Sciences
822		https://en.wikipedia.org/wiki/Drumheller_Fountain
-- Getting results for a non-existent place --
[]
```

## Task 2: Defining your templates

You will need to create a couple of templates for your web application. Both these templates should inherit from a base template (`base.html`). The base template should define a header (`<h1>`) element at the top that says “Search local Wikipedia articles” (without quotes). It should also include a footer element at the bottom (`<footer>`) that says “Data from [Wikipedia](https://wikipedia.org/) and [OpenStreetMap](https://www.openstreetmap.org/).” (make sure that the links are present and correct). The base template should also include the `<link>` element for any CSS file that you may need. Once you have the base template, make sure that the following two templates inherit from it.

 1. In your first template (`index.html`), you need to define an HTML form. Each component of the form should map to the parameters of the `wikipedia_locationsearch()` function that you defined earlier in Task 1. For `max_results` and `radius`, use the `value` attribute of the `<input>` element to pre-define the default value for the user. For example, `<input type="number" name="radius" id="radius" value="2">`. Your form should have:
    * A text input field for the place name
    * A number input field for the number of results to return. 
    * A number input field for the search radius.
    * A checkbox to sort by length of pages (longest-article-first)
 2. In your second template (`results.html`), your template code should show the name of the place that was provided by the user. Then, it should loop over a supplied list of `wikipedia.WikipediaPage` objects, and render them. The first example on the [Jinja](https://palletsprojects.com/p/jinja/) project page shows you how to loop over a list of objects within the template. For each object, you should include the title of the page that is linked to the page on Wikipedia, and a page summary. To get these attributes, use the `.title`, `.url`, and `.summary` attributes of each object. You can also look at the test code for `functions.py` to see how this is done with a different mode of interaction. _Note: In addition to the above, if the list is empty, you need to show an error message saying that no results were found for the search term. For this, you will need to use a "[filter](https://jinja.palletsprojects.com/en/3.1.x/templates/#filters)" in Jinja, called [length](https://jinja.palletsprojects.com/en/3.1.x/templates/#jinja-filters.length). For example, if your variable in the template is called `results`, `results|length` will give you the number of items in `results`._

 > __Note:__ You can decide how you want your HTML templates to look visually. The only rule is that you need to use at least a couple of CSS rulesets in the templates. You can use more, but a total of two across the two templates is the minimum that we require. You can either define your own rulesets in a CSS file, or you can use pre-existing rulesets from a framework such as Bootstrap. The screenshots that I have included at the end of this document are illustrative as far a visual layout goes; it is okay if your visual layout looks different, as long as the all the form elements are there in the index page, and all the attributes (including a link for each article) are rendered in the results page.


## Task 3: Defining your view functions

The functions that handle URLs in Flask are called _view functions_ (during our class sessions, we defined these functions in the `app.py` file).

Defines two view functions in your `app.py` file, for the two URLs.

 1. `index()` should render the template `index.html` for the URL path `/`
 2. `results()` should accept either `GET` or `POST` requests for the URL path `/results`. For a `POST` request, the function should call `wikipedia_locationsearch()` and then render the template `results.html` with the results returned by the function. Note that everything in the forms data dictionary comes as a string, so you will need to convert the `max_result` and `radius` data from string to int and float with the `int()` and `float()` functions. For a `GET` request, it should return an HTTP 400 error with a “Wrong HTTP method” message (this does not need to be styled or be a fully-formed HTML page).

## Sample web application screenshots

The screenshots below show what a complete web application may look like; however, as explained earlier in the Task 2 section, you do not need to recreate this exact visual look. I used Bootstrap in my templates (e.g., I used the [list group](https://getbootstrap.com/docs/5.2/components/list-group/) components in my results page, and the [alert](https://getbootstrap.com/docs/5.2/components/alerts/) component, that I showed in class, for the error message when there are no results). You do not need to follow this exact same layout, but you do need to apply at least a couple of CSS rulesets across your templates.

### Search form (the index page)
![Search form](images/form.png)

### Results page

#### When there are results
![Results page](images/results.png)

#### Error message when there are no results
![Error message in the results page](images/error.png)

## Additional tasks
 This homework walks you through the process of creating a web application that uses a couple of web APIs. There are some additional things you can do (these will not count toward your grades for this homework) if you want to explore these techniques further.

 * Use the `required` attribute of the HTML `<input>` element to require the user to type in something in the place field of your form
 * Use the `max` and `min` attributes of the HTML `<input>` element to set reasonable ranges for the numerical form components (e.g., restrict the number of results from 1 to 100, restrict the radius from 1 to 50 miles)
 * Allow the user to specify the language edition of Wikipedia that they want the results from. For example, the user should be able to specify that they want results from the [Spanish language version of Wikipedia](https://es.wikipedia.org/). The [set_lang()](https://wikipedia.readthedocs.io/en/latest/code.html#wikipedia.set_lang) function in the Wikipedia module should help you achieve this. As further step, you can even consider how to generate the search form dynamically so that the choices for the languages are pre-populated for the user, using the [wikipedia.languages()](https://wikipedia.readthedocs.io/en/latest/code.html#wikipedia.languages) function.