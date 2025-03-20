# Create a file named 'load_data.py' in your project root
import os
import django
import random
from datetime import datetime, timedelta
from meditation.models import Category, Subcategory, Technique, User, Comment


# Now you can import your models


# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meditation_project.settings')
django.setup()

from meditation.models import Category, Subcategory, Technique, User, Comment
from django.contrib.auth.models import User

def create_sample_data():
    # Create Categories
    categories = [
        {
            'name': 'Breathing Based Meditation',
            'description': 'Meditation techniques that focus on breath awareness and control.',
            'image_path': 'categories/breathing.jpg'
        },
        {
            'name': 'Silent Meditation',
            'description': 'Techniques that emphasize stillness and silence.',
            'image_path': 'categories/silent.jpg'
        },
        {
            'name': 'Movement Meditation',
            'description': 'Dynamic meditation techniques that incorporate physical movement.',
            'image_path': 'categories/movement.jpg'
        },
        {
            'name': 'Tratak',
            'description': 'Techniques that involve fixed gazing at a single point or object.',
            'image_path': 'categories/tratak.jpg'
        },
        {
            'name': 'Reiki',
            'description': 'Energy healing techniques for balance and well-being.',
            'image_path': 'categories/reiki.jpg'
        },
    ]
    
    # Create categories
    category_objects = []
    for category_data in categories:
        category = Category.objects.create(
            name=category_data['name'],
            description=category_data['description'],
            # image=category_data['image_path']  # Uncomment if you have actual images
        )
        category_objects.append(category)
    
    # Create Subcategories
    subcategories = [
        # Breathing Based
        {
            'category': category_objects[0],
            'name': 'Vipassana',
            'description': 'Ancient meditation technique focusing on breath and bodily sensations.',
            'image_path': 'subcategories/vipassana.jpg'
        },
        {
            'category': category_objects[0],
            'name': 'Anapanasati',
            'description': 'Mindfulness of breathing practice from Buddhist traditions.',
            'image_path': 'subcategories/anapanasati.jpg'
        },
        {
            'category': category_objects[0],
            'name': 'Nadbrahma',
            'description': 'Sound-based meditation focusing on natural rhythm of breath.',
            'image_path': 'subcategories/nadbrahma.jpg'
        },
        # Silent
        {
            'category': category_objects[1],
            'name': 'Zazen',
            'description': 'Zen Buddhist practice of sitting meditation.',
            'image_path': 'subcategories/zazen.jpg'
        },
        {
            'category': category_objects[1],
            'name': 'Transcendental Meditation',
            'description': 'Technique using mantras to transcend ordinary thinking.',
            'image_path': 'subcategories/tm.jpg'
        },
        # Movement
        {
            'category': category_objects[2],
            'name': 'Dynamic Meditation',
            'description': 'Active meditation techniques involving physical movement.',
            'image_path': 'subcategories/dynamic.jpg'
        },
        {
            'category': category_objects[2],
            'name': 'Walking Meditation',
            'description': 'Mindful walking practices for present-moment awareness.',
            'image_path': 'subcategories/walking.jpg'
        },
    ]
    
    # Create subcategories
    subcategory_objects = []
    for subcategory_data in subcategories:
        subcategory = Subcategory.objects.create(
            category=subcategory_data['category'],
            name=subcategory_data['name'],
            description=subcategory_data['description'],
            # image=subcategory_data['image_path']  # Uncomment if you have actual images
        )
        subcategory_objects.append(subcategory)
    
    # Create sample techniques
    techniques = [
        # Vipassana
        {
            'subcategory': subcategory_objects[0],
            'name': 'Basic Vipassana',
            'short_description': 'Foundational vipassana practice focusing on breath awareness.',
            'benefits': 'Reduces stress and anxiety.\nImproves concentration.\nEnhances self-awareness.\nPromotes emotional well-being.',
            'instructions': '''1. Sit in a comfortable position with your back straight.
2. Close your eyes and focus on your breath.
3. Notice the sensation of the breath entering and leaving your nostrils.
4. When your mind wanders, gently bring attention back to the breath.
5. Gradually expand awareness to include bodily sensations.
6. Observe sensations without judgment or reaction.
7. Practice for 20-30 minutes daily.''',
            'difficulty_level': 'beginner',
            'duration': '20-30 minutes',
            'image_path': 'techniques/basic_vipassana.jpg',
            'video_url': 'https://www.youtube.com/embed/example1'
        },
        {
            'subcategory': subcategory_objects[0],
            'name': 'Body Scanning Vipassana',
            'short_description': 'Systematic awareness of bodily sensations from head to toe.',
            'benefits': 'Deepens body awareness.\nReleases physical tension.\nCalms the nervous system.\nImproves concentration and focus.',
            'instructions': '''1. Lie down or sit comfortably with your eyes closed.
2. Start by bringing attention to the top of your head.
3. Slowly move your attention down through your body.
4. Notice any sensations in each part without judgment.
5. If you find tension, breathe into that area and release.
6. Continue until you reach your toes.
7. Practice for 30-45 minutes daily.''',
            'difficulty_level': 'intermediate',
            'duration': '30-45 minutes',
            'image_path': 'techniques/body_scan.jpg',
            'video_url': 'https://www.youtube.com/embed/example2'
        },
        {
            'subcategory': subcategory_objects[0],
            'name': 'निष्क्रिय ध्यान',
            'short_description': 'A passive meditation technique for morning practice.',
            'benefits': 'Calms the mind.\nReaches zero thoughts state.\nEnables self-realization.\nReduces stress and anxiety.',
            'instructions': '''यह ध्यान प्रातःकाल के लिए है। इस ध्यान में रीढ़ को सीधा रख कर, आंखे बंद करके, गर्दन को सीधा रखना है। ओठ बंद हो और जीभ ताल से लगी हो। श्वास धीमी पर गहरी लेना है। और ध्यान नाभि के पास रखना है। नाभि-केंद्र पर श्वास के कारण जो कपन गालूम होता है, उसके प्रति जागे हुए रहना है। बस इतना ही करना है। यह प्रयोग चित्त को शांत करता है और विचारों को शून्य कर देता है। इस शून्य से अंततः स्वयं में प्रवेश हो जाता है।

इस प्रयोग में हम क्या करेंगे? शांत बैठेंगे। शरीर को शिथिल, रिलैक्स्ड और रीढ़ को सीधा रखेंगे। शरीर के सारे हलन चलन, मूवमेंट को छोड़ देगे। शांत, धीमी, पर गहरी श्वास लेंगे। और मौन, अपनी श्वास को देखते रहेंगे और बाहर की जो ध्वनियां सुनाई पड़ें, उन्हें सुनते रहेंगे। कोई प्रतिक्रिया नहीं करेंगे। उन पर कोई विचार नहीं करेंगे। शब्द न हों और हम केवल साक्षी हैं, जो भी हो रहा है, हम केवल उसे दूर खड़े जान रहे हैं, ऐसे भाव में अपने को छोड़ देंगे।''',
            'difficulty_level': 'beginner',
            'duration': '20-30 minutes',
            'image_path': 'techniques/passive_meditation.jpg',
            'video_url': ''
        },
        # Add more sample techniques for other subcategories
    ]
    
    # Create techniques
    technique_objects = []
    for technique_data in techniques:
        technique = Technique.objects.create(
            subcategory=technique_data['subcategory'],
            name=technique_data['name'],
            short_description=technique_data['short_description'],
            benefits=technique_data['benefits'],
            instructions=technique_data['instructions'],
            difficulty_level=technique_data['difficulty_level'],
            duration=technique_data['duration'],
            # image=technique_data['image_path'],  # Uncomment if you have actual images
            video_url=technique_data['video_url']
        )
        technique_objects.append(technique)
    
    # Create sample comments if you have a Comment model
    if User.objects.count() > 0:
        for i in range(10):
            user = User.objects.first()
            technique = random.choice(technique_objects)
            Comment.objects.create(
                user=user,
                technique=technique,
                content=f"This is a sample comment about {technique.name}. I found this technique very helpful for my meditation practice.",
                created_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
    
    print("Sample data created successfully!")

if __name__ == "__main__":
    print("Creating sample data...")
    create_sample_data()