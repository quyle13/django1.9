import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
    python_pages = [{"title":"Official Python Tutorial",
                     "url":"http://docs.python.org/2/tutorial/",
                     "views":"100"
                     }
                    ,{"title":"How to think like a Computer Scientist",
                      "url":"http://www.greenteapress.com/thinkpython/",
                      "views":"10"

                      },
                    {"title":"Learn Python in 10 Minutes"
                     ,"url":"http://www.korokithakis.net/tutorials/python",
                     "views": "50"
                     }
                    ]

    django_pages = [{"title":"Official Django Tutorial",
                     "url":"https://docs.djangoproject/com/en/1/9/intro/tutorial01/",
                     "views":"34"
                     },
                    {"title":"Django Rocks",
                     "url":"http://www.djangorocks.com/",
                     "views": "44"},
                    {"title":"How to Tango with Django",
                     "url":"http://www.tangowithdjango.com",
                     "views": "54"}
                    ]
    other_pages = [{"title":"Bottle",
                    "url":"http://bottlepy.org/docs/dev/",
                    "views": "74"},
                   {"title":"Flask",
                    "url":"http://flask.pocoo.org",
                    "views": "14"
                    }]
    cats = {"Python":{"pages":python_pages},
            "Django":{"pages":django_pages},
            "Other Frameworks":{"pages":other_pages}
            }
    for cat,cat_data in cats.items():
        if cat == "Python":
            c = add_cat(cat,128,64)
        elif cat == "Django":
            c = add_cat(cat, 64, 32)
        else:
            c = add_cat(cat, 32, 16)
        for p in cat_data["pages"]:
            add_page(c,p["title"],p["url"],p["views"])

    for c in Category.objects.all():
        for p in Page.objects.filter(category = c):
            print ("- Category Name: {0} - Page Name {1} ".format(str(c),str(p)))

def add_cat(name,views,likes):
    c = Category.objects.get_or_create(name=name,views=views,likes=likes)[0]
    c.save()
    return c
def add_page(cat,title,url,views = 0):
    p = Page.objects.get_or_create(category = cat,title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

if __name__=='__main__':
    print ("Starting Rango population script...")
    populate()