import os
import django
import sys

def main():
    fake = Faker('ru')
    user = User.objects.all()[:1].get()
    for _ in range(20):
        post = Post(author = user, title = fake.sentence(), 
                    text = fake.paragraph(nb_sentences=5))
        post.save()

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))
    sys.path.append(BASE_DIR)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','djangoinfire.settings')
    django.setup()
    
    from faker import Faker
    from blog.models import Post
    from django.contrib.auth.models import User
    
    main()        