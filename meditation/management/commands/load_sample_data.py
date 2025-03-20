# meditation/management/commands/load_sample_data.py

from django.core.management.base import BaseCommand
from meditation.models import Category, Subcategory, Technique
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Loads sample meditation data into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample meditation data...')

        # Create Categories
        mindfulness = Category.objects.create(
            name="Mindfulness Meditation",
            description="Techniques that focus on being present and aware in the moment.",
            slug=slugify("Mindfulness Meditation")
        )
        
        spiritual = Category.objects.create(
            name="Spiritual Meditation",
            description="Meditation practices connected to spiritual and religious traditions.",
            slug=slugify("Spiritual Meditation")
        )
        
        focused = Category.objects.create(
            name="Focused Meditation",
            description="Techniques that involve focusing on a specific object, sound, or sensation.",
            slug=slugify("Focused Meditation")
        )
        
        movement = Category.objects.create(
            name="Movement Meditation",
            description="Meditation practices that incorporate physical movement.",
            slug=slugify("Movement Meditation")
        )

        # Create Subcategories
        body_scan = Subcategory.objects.create(
            category=mindfulness,
            name="Body Scan",
            description="A practice that involves paying attention to parts of the body and bodily sensations in a gradual sequence.",
            slug=slugify("Body Scan")
        )
        
        breathing = Subcategory.objects.create(
            category=mindfulness,
            name="Breathing Meditation",
            description="Focusing attention on the breath - a practice present in many meditation traditions.",
            slug=slugify("Breathing Meditation")
        )
        
        zen = Subcategory.objects.create(
            category=spiritual,
            name="Zen Meditation",
            description="Traditional Buddhist meditation practices focusing on posture and breathing.",
            slug=slugify("Zen Meditation")
        )
        
        mantra = Subcategory.objects.create(
            category=focused,
            name="Mantra Meditation",
            description="Repeating a mantra (word or phrase) to prevent distracting thoughts.",
            slug=slugify("Mantra Meditation")
        )
        
        yoga = Subcategory.objects.create(
            category=movement,
            name="Yoga Meditation",
            description="Combines physical postures, breathing exercises, and meditation.",
            slug=slugify("Yoga Meditation")
        )
        
        tai_chi = Subcategory.objects.create(
            category=movement,
            name="Tai Chi",
            description="A gentle form of martial arts focusing on the principle of the flow of qi through the body.",
            slug=slugify("Tai Chi")
        )

        # Create Techniques
        Technique.objects.create(
            subcategory=breathing,
            name="4-7-8 Breathing",
            slug=slugify("4-7-8 Breathing"),
            short_description="A breathing pattern developed by Dr. Andrew Weil, based on pranayama breathing.",
            benefits="Reduces anxiety\nHelps manage food cravings\nControls emotional responses\nImproves sleep",
            instructions="1. Sit or lie down in a comfortable position\n2. Place the tip of your tongue against the roof of your mouth, behind your front teeth\n3. Exhale completely through your mouth, making a whoosh sound\n4. Close your mouth and inhale through your nose for a count of 4\n5. Hold your breath for a count of 7\n6. Exhale completely through your mouth for a count of 8\n7. Repeat this cycle 3-4 times initially, gradually increasing to 8 cycles",
            difficulty_level="beginner",
            duration="5-10 minutes",
            video_url="https://www.youtube.com/embed/YRPh_GaiL8s"
        )
        
        Technique.objects.create(
            subcategory=body_scan,
            name="Progressive Muscle Relaxation",
            slug=slugify("Progressive Muscle Relaxation"),
            short_description="A technique that involves tensing and then relaxing muscle groups throughout the body.",
            benefits="Reduces physical tension\nDecreases anxiety and stress\nHelps with insomnia\nIncreases body awareness",
            instructions="1. Lie down in a comfortable position\n2. Take a few deep breaths to begin relaxing\n3. Start by tensing the muscles in your feet for 5 seconds, then release\n4. Notice the sensation of relaxation in the feet\n5. Move up to your calves, tense for 5 seconds, then release\n6. Continue moving upward through each muscle group\n7. End with the muscles in your face\n8. Take a few more deep breaths and notice the relaxation throughout your body",
            difficulty_level="beginner",
            duration="15-20 minutes",
            video_url="https://www.youtube.com/embed/ihO02wUzgkc"
        )
        
        Technique.objects.create(
            subcategory=zen,
            name="Zazen (Seated Meditation)",
            slug=slugify("Zazen Seated Meditation"),
            short_description="The heart of Zen Buddhist practice, focusing on posture and breathing.",
            benefits="Develops concentration\nCultivates awareness\nReduces mental chatter\nFosters spiritual insight",
            instructions="1. Sit on a cushion with legs crossed or in a chair with feet flat on the floor\n2. Keep your back straight but not rigid\n3. Place hands in the cosmic mudra: left hand on top of right, palms up, thumbs lightly touching\n4. Keep eyes half-open, gaze resting on the floor about 3 feet ahead\n5. Breathe naturally through the nose\n6. Count breaths from 1 to 10, then repeat\n7. When thoughts arise, acknowledge them and return to counting",
            difficulty_level="intermediate",
            duration="25-45 minutes",
            video_url="https://www.youtube.com/embed/Mx0mSNz__Qs"
        )
        
        Technique.objects.create(
            subcategory=mantra,
            name="Om Meditation",
            slug=slugify("Om Meditation"),
            short_description="Using the sacred sound 'Om' (Aum) as a point of focus for meditation.",
            benefits="Improves concentration\nReduces stress and anxiety\nEnhances voice quality\nDeepens spiritual connection",
            instructions="1. Sit comfortably with spine erect\n2. Take a few deep breaths to center yourself\n3. Take a deep breath and on the exhale, chant 'Aum' (pronouncing all three parts: A-U-M)\n4. Feel the vibration in your body as you chant\n5. Repeat for 5-10 minutes\n6. Gradually increase duration as you become more comfortable",
            difficulty_level="beginner",
            duration="10-15 minutes",
            video_url="https://www.youtube.com/embed/8sYK7lm3UKg"
        )
        
        Technique.objects.create(
            subcategory=yoga,
            name="Mindful Sun Salutation",
            slug=slugify("Mindful Sun Salutation"),
            short_description="A flowing sequence of yoga poses with mindful awareness of breath and movement.",
            benefits="Increases flexibility\nBuilds strength\nImproves circulation\nDevelops mind-body connection",
            instructions="1. Begin standing in Mountain Pose (Tadasana)\n2. Bring hands together at heart center\n3. Inhale, raise arms overhead (Urdhva Hastasana)\n4. Exhale, fold forward (Uttanasana)\n5. Inhale, lift halfway up (Ardha Uttanasana)\n6. Exhale, step or jump back to plank, then lower to the ground\n7. Inhale, lift chest into Cobra or Upward-Facing Dog\n8. Exhale, press back to Downward-Facing Dog\n9. Hold for 5 breaths, focusing on the sensation of each breath\n10. Step or jump forward, inhale to halfway lift\n11. Exhale, fold forward\n12. Inhale, rise to standing with arms overhead\n13. Exhale, return to heart center\n14. Repeat 3-6 times with mindful awareness",
            difficulty_level="intermediate",
            duration="15-20 minutes",
            video_url="https://www.youtube.com/embed/8AakYeM23sI"
        )
        
        Technique.objects.create(
            subcategory=tai_chi,
            name="5-Minute Tai Chi Flow",
            slug=slugify("5-Minute Tai Chi Flow"),
            short_description="A brief sequence of flowing Tai Chi movements focused on energy and breath.",
            benefits="Improves balance\nReduces stress\nIncreases energy flow\nCultivates mindfulness in movement",
            instructions="1. Begin standing with feet shoulder-width apart, knees slightly bent\n2. Take three deep breaths, centering yourself\n3. Raise hands slowly to chest height, palms down\n4. Turn palms up and raise hands overhead while inhaling\n5. Turn palms down and lower hands while exhaling\n6. Repeat this flowing movement 5 times\n7. Shift weight to right foot, extend left foot to side\n8. Move arms in a circular motion from left to right\n9. Shift weight gradually to left foot\n10. Continue the circular arm movement\n11. Return to center, feet shoulder-width apart\n12. Place hands over lower abdomen (dantian)\n13. Take three deep breaths to complete the practice",
            difficulty_level="beginner",
            duration="5 minutes",
            video_url="https://www.youtube.com/embed/ZxcNBejxlzs"
        )

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample meditation data!'))