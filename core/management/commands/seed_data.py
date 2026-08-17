import os
import io
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from core.models import Item

class Command(BaseCommand):
    help = 'Seeds database with demo users, sample lost/found items, and generated demonstration photos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Beginning CampusFind sample data seeding...'))

        # 1. Create or get Admin / Staff user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@campusfind.edu',
                'first_name': 'Campus',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('campus2026!')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        if created:
            self.stdout.write(self.style.SUCCESS('Created superuser/admin: admin / campus2026!'))

        # 2. Create Student users
        student_alex, _ = User.objects.get_or_create(
            username='student_alex',
            defaults={
                'email': 'alex.miller@campus.edu',
                'first_name': 'Alex',
                'last_name': 'Miller',
            }
        )
        student_alex.set_password('campus2026!')
        student_alex.save()

        student_maya, _ = User.objects.get_or_create(
            username='student_maya',
            defaults={
                'email': 'maya.patel@campus.edu',
                'first_name': 'Maya',
                'last_name': 'Patel',
            }
        )
        student_maya.set_password('campus2026!')
        student_maya.save()

        student_kwame, _ = User.objects.get_or_create(
            username='student_kwame',
            defaults={
                'email': 'kwame.mensah@campus.edu',
                'first_name': 'Kwame',
                'last_name': 'Mensah',
            }
        )
        student_kwame.set_password('campus2026!')
        student_kwame.save()

        # Helper to generate a placeholder PNG image
        def create_sample_image(label, bg_color=(49, 46, 129), text_color=(255, 255, 255)):
            img = Image.new('RGB', (600, 400), color=bg_color)
            d = ImageDraw.Draw(img)
            # Draw decorative border & simple geometry
            d.rectangle([(15, 15), (585, 385)], outline=(255, 255, 255, 120), width=3)
            d.text((40, 180), f"CampusFind Item Demo\n{label}", fill=text_color)
            
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return ContentFile(buffer.getvalue(), name=f"{label.lower().replace(' ', '_')}.png")

        # 3. Seed Items
        demo_items = [
            {
                'user': student_alex,
                'title': 'Space Grey MacBook Air (M2) in Black Sleeve',
                'category': Item.CAT_ELECTRONICS,
                'status': Item.STATUS_LOST,
                'location': 'Central Library, 2nd Floor Study Desk 14',
                'date_event': timezone.now().date() - timedelta(days=1),
                'description': 'Left my 13-inch M2 MacBook Air inside a black Tomtoc protective sleeve. Has a small GitHub sticker in the top right corner. Very important for capstone presentation!',
                'contact': 'Alex Miller - alex.miller@campus.edu / +1 (555) 234-8890',
                'bg_color': (30, 41, 59),
            },
            {
                'user': student_maya,
                'title': 'Blue Herschel Canvas Backpack',
                'category': Item.CAT_BAGS_WALLETS,
                'status': Item.STATUS_FOUND,
                'location': 'Campus Cafeteria & Dining Hall (Near juice bar)',
                'date_event': timezone.now().date() - timedelta(days=2),
                'description': 'Found a navy blue backpack left on a dining chair. Contains CSBC 252 notebook, blue spiral pad, and pencil case. Handed to Cafeteria Lost Desk.',
                'contact': 'Dining Hall Info Desk / maya.patel@campus.edu',
                'bg_color': (2, 132, 199),
            },
            {
                'user': student_kwame,
                'title': 'University Student ID Card & Gym Pass',
                'category': Item.CAT_CARDS_ID,
                'status': Item.STATUS_FOUND,
                'location': 'Sports Complex & Gymnasium, Locker Room Hallway',
                'date_event': timezone.now().date() - timedelta(days=1),
                'description': 'Found a green campus student ID card belonging to Kwame Mensah along with a recreation gym access fob. Currently held at the Gym reception.',
                'contact': 'Sports Complex Reception / 555-SPORTS-01',
                'bg_color': (16, 185, 129),
            },
            {
                'user': student_alex,
                'title': 'Set of Dorm Keys with Red BMW Lanyard',
                'category': Item.CAT_KEYS,
                'status': Item.STATUS_LOST,
                'location': 'Hostel & Student Residence Halls (Block C)',
                'date_event': timezone.now().date() - timedelta(days=3),
                'description': 'Three silver keys on a red lanyard with a miniature silver car bottle opener attached. Lost somewhere between the laundry room and Block C stairs.',
                'contact': 'Alex - alex.miller@campus.edu / +1 555-234-8890',
                'bg_color': (225, 29, 72),
            },
            {
                'user': student_maya,
                'title': 'Texas Instruments TI-84 Plus CE Graphing Calculator',
                'category': Item.CAT_ELECTRONICS,
                'status': Item.STATUS_FOUND,
                'location': 'Science Complex / Block B, Room 204',
                'date_event': timezone.now().date() - timedelta(days=4),
                'description': 'Black graphing calculator left on the podium after Advanced Calculus class. White initials "J.D." engraved on the back casing.',
                'contact': 'Prof. Office Block B-310 / maya.patel@campus.edu',
                'bg_color': (79, 70, 229),
            },
            {
                'user': student_kwame,
                'title': 'Hydro Flask 32oz Insulated Bottle (Cobalt Blue)',
                'category': Item.CAT_SPORTS_BOTTLES,
                'status': Item.STATUS_CLAIMED,
                'location': 'Engineering Lecture Theatre 2 (LT-2)',
                'date_event': timezone.now().date() - timedelta(days=5),
                'description': 'Dark blue metal water bottle with campus outdoor club stickers. Successfully retrieved by owner at security desk.',
                'contact': 'Kwame Mensah - kwame.mensah@campus.edu',
                'bg_color': (5, 150, 105),
                'claimed': True,
            },
            {
                'user': student_alex,
                'title': 'Apple AirPods Pro 2 in MagSafe Charging Case',
                'category': Item.CAT_ELECTRONICS,
                'status': Item.STATUS_LOST,
                'location': 'Student Union Building (SUB), 1st Floor Lounge',
                'date_event': timezone.now().date() - timedelta(days=2),
                'description': 'White AirPods Pro 2 inside a clear silicone case with a small metal clip. Serial number registered on my Apple ID.',
                'contact': 'alex.miller@campus.edu / Text: +1 555-234-8890',
                'bg_color': (147, 51, 234),
            },
            {
                'user': student_maya,
                'title': 'Calculus: Early Transcendentals Textbook (9th Edition)',
                'category': Item.CAT_BOOKS_DOCS,
                'status': Item.STATUS_FOUND,
                'location': 'Computer Labs / IT Center, Lab 3',
                'date_event': timezone.now().date() - timedelta(days=3),
                'description': 'Hardcover Stewart Calculus textbook with yellow sticky flags on Chapter 7 and 8. Left near workstation 19.',
                'contact': 'IT Helpdesk / ext. 3320',
                'bg_color': (217, 119, 6),
            },
            {
                'user': student_kwame,
                'title': 'Ray-Ban Wayfarer Sunglasses (Matte Black)',
                'category': Item.CAT_ACCESSORIES,
                'status': Item.STATUS_CLAIMED,
                'location': 'Main Auditorium Courtyard',
                'date_event': timezone.now().date() - timedelta(days=7),
                'description': 'Matte black classic sunglasses in brown leather Ray-Ban case. Returned to owner after ID verification.',
                'contact': 'Kwame Mensah - kwame.mensah@campus.edu',
                'bg_color': (13, 148, 136),
                'claimed': True,
            }
        ]

        for data in demo_items:
            bg_col = data.pop('bg_color', (49, 46, 129))
            is_claimed = data.pop('claimed', False)
            title = data['title']

            item, created = Item.objects.get_or_create(
                title=title,
                defaults=data
            )
            if created:
                # Attach generated sample image
                item.image = create_sample_image(title, bg_color=bg_col)
                if is_claimed:
                    item.is_verified_returned = True
                    item.resolved_at = timezone.now()
                item.save()
                self.stdout.write(self.style.SUCCESS(f"Created demo item: {title}"))

        self.stdout.write(self.style.SUCCESS('Successfully completed database seeding!'))
