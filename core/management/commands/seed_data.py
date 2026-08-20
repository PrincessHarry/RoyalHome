import os
import random
from datetime import date, timedelta, datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth.models import User
from django.utils import timezone

from rooms.models import RoomType, RoomImage
from bookings.models import Booking, AddOn
from restaurant.models import MenuCategory, MenuItem
from amenities.models import Amenity
from events.models import EventSpace, EventInquiry
from gallery.models import GalleryImage
from blog.models import BlogPost
from core.models import Testimonial, ContactInquiry
from guestportal.models import ServiceOrder
from dashboard.models import StaffProfile, ShiftSchedule

# Use relative path from project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS = os.path.join(BASE_DIR, 'assets_src')


def img(name):
    """Load an image file. Returns None if the file doesn't exist."""
    file_path = os.path.join(ASSETS, name)
    if os.path.exists(file_path):
        return File(open(file_path, 'rb'), name=name)
    return None


class Command(BaseCommand):
    help = 'Seed the database with realistic demo data for Xceptional Place Hotel'

    def handle(self, *args, **options):
        self.stdout.write('Clearing old demo data...')
        ServiceOrder.objects.all().delete()
        Booking.objects.all().delete()
        AddOn.objects.all().delete()
        RoomImage.objects.all().delete()
        RoomType.objects.all().delete()
        MenuItem.objects.all().delete()
        MenuCategory.objects.all().delete()
        Amenity.objects.all().delete()
        EventInquiry.objects.all().delete()
        EventSpace.objects.all().delete()
        GalleryImage.objects.all().delete()
        BlogPost.objects.all().delete()
        Testimonial.objects.all().delete()
        ContactInquiry.objects.all().delete()
        ShiftSchedule.objects.all().delete()
        StaffProfile.objects.all().delete()
        User.objects.all().delete()

        # ---------- ROOM TYPES ----------
        self.stdout.write('Creating room types...')
        standard = RoomType.objects.create(
            name='Standard Room', slug='standard-room', category='standard',
            tagline='Cosy comfort with everything you need.',
            description='Our Standard Room offers a plush queen bed, city views and all the essentials for a restful stay — a smart TV, fibre WiFi, and a marble en-suite bathroom. Ideal for solo travellers and couples visiting Jos for business or leisure.',
            base_price=Decimal('65000'), capacity_adults=2, capacity_children=1,
            bed_type='1 Queen Bed', size_sqm=24, total_rooms=40, is_featured=True,
            floor_range='1st - 3rd Floor',
            amenities='Free Fibre WiFi, Smart TV, Air Conditioning, Mini Fridge, Work Desk, En-suite Bathroom, Daily Housekeeping, 24/7 Room Service',
        )
        img_file = img('standard-room.jpg')
        if img_file:
            standard.cover_image.save('standard-room.jpg', img_file, save=True)

        deluxe = RoomType.objects.create(
            name='Deluxe Room', slug='deluxe-room', category='deluxe',
            tagline='More space, a garden view, and a touch more indulgence.',
            description='The Deluxe Room adds extra square footage, a seating area and garden views to everything you love about our Standard Room — perfect for guests who want a little more room to unwind.',
            base_price=Decimal('92000'), capacity_adults=2, capacity_children=2,
            bed_type='1 King or 2 Twin Beds', size_sqm=32, total_rooms=30,
            floor_range='2nd - 4th Floor',
            amenities='Free Fibre WiFi, 55" Smart TV, Air Conditioning, Mini Bar, Seating Area, Bathtub, Rainfall Shower, Nespresso Machine',
        )
        img_file = img('standard-room.jpg')
        if img_file:
            deluxe.cover_image.save('standard-room.jpg', img_file, save=True)

        exclusive = RoomType.objects.create(
            name='Exclusive Suite', slug='exclusive-suite', category='exclusive',
            tagline='Panoramic Plateau views and a private lounge.',
            description='The Exclusive Suite is our most requested room — floor-to-ceiling windows framing the Plateau rock formations, a separate living area, a king bed dressed in premium linens, and personalised turn-down service.',
            base_price=Decimal('145000'), capacity_adults=2, capacity_children=2,
            bed_type='1 King Bed', size_sqm=48, total_rooms=15, is_featured=True,
            floor_range='4th - 5th Floor',
            amenities='Free Fibre WiFi, 65" Smart TV, Private Lounge, Premium Mini Bar, Rainfall Shower & Bathtub, Nespresso Machine, Turn-down Service, Complimentary Breakfast',
        )
        img_file = img('exclusive-room.jpg')
        if img_file:
            exclusive.cover_image.save('exclusive-room.jpg', img_file, save=True)

        presidential = RoomType.objects.create(
            name='Presidential Villa', slug='presidential-villa', category='presidential',
            tagline='A private pool-facing villa fit for VIP guests.',
            description='Our Presidential Villa is a self-contained residence with its own pool-facing terrace, private butler service, a full living and dining area, and unmatched privacy — designed for VIPs, dignitaries and honeymooners.',
            base_price=Decimal('220000'), capacity_adults=4, capacity_children=2,
            bed_type='1 King Bed + 1 Sofa Bed', size_sqm=85, total_rooms=4, is_featured=True,
            floor_range='Ground Floor Villa',
            amenities='Private Pool Access, Butler Service, Full Kitchenette, Private Terrace, 75" Smart TV, Premium Bar, Jacuzzi, Complimentary Airport Transfer',
        )
        img_file = img('poolside.jpg')
        if img_file:
            presidential.cover_image.save('poolside.jpg', img_file, save=True)

        for room, extra_imgs in [
            (standard, ['standard-room.jpg', 'relaxation-area.jpg']),
            (exclusive, ['exclusive-room.jpg', 'relaxation-area.jpg']),
            (presidential, ['poolside.jpg', 'exclusive-room.jpg']),
        ]:
            for name in extra_imgs:
                img_file = img(name)
                if img_file:
                    ri = RoomImage(room_type=room, caption=room.name)
                    ri.image.save(name, img_file, save=True)

        # ---------- ADD-ONS ----------
        self.stdout.write('Creating add-ons...')
        AddOn.objects.bulk_create([
            AddOn(name='Airport Pickup', description='One-way transfer from Yakubu Gowon Airport', price=Decimal('18000'), icon='car'),
            AddOn(name='Breakfast Package', description='Daily breakfast for the length of your stay', price=Decimal('8000'), icon='coffee'),
            AddOn(name='Spa Session (60 min)', description='Full-body massage at our Wellness Spa', price=Decimal('25000'), icon='flower-2'),
            AddOn(name='Late Checkout', description='Checkout extended to 4:00pm', price=Decimal('10000'), icon='clock'),
            AddOn(name='Romantic Room Setup', description='Rose petals, candles & a bottle of wine', price=Decimal('20000'), icon='heart'),
            AddOn(name='Airport Drop-off', description='One-way transfer to Yakubu Gowon Airport', price=Decimal('18000'), icon='car'),
        ])

        # ---------- RESTAURANT ----------
        self.stdout.write('Creating restaurant menu...')
        cat_starters = MenuCategory.objects.create(name='Starters & Small Plates', order=1)
        cat_mains = MenuCategory.objects.create(name='Main Courses', order=2)
        cat_grill = MenuCategory.objects.create(name='From the Grill', order=3)
        cat_desserts = MenuCategory.objects.create(name='Desserts', order=4)
        cat_drinks = MenuCategory.objects.create(name='Beverages', order=5)

        MenuItem.objects.bulk_create([
            MenuItem(category=cat_starters, name='Peppered Snail', description='Garden snails sautéed in a smoky pepper sauce', price=Decimal('8500')),
            MenuItem(category=cat_starters, name='Chicken Suya Skewers', description='Grilled chicken with traditional suya spice', price=Decimal('6500'), is_signature=True),
            MenuItem(category=cat_starters, name='Plantain Chips & Guacamole', description='Crisp plantain with house guacamole', price=Decimal('4500')),
            MenuItem(category=cat_mains, name='Jollof Rice & Grilled Chicken', description="Xceptional Place's signature smoky jollof", price=Decimal('9500'), is_signature=True),
            MenuItem(category=cat_mains, name='Egusi Soup & Pounded Yam', description='Melon seed soup with assorted meat', price=Decimal('11000')),
            MenuItem(category=cat_mains, name='Fried Rice & Turkey', description='Nigerian-style fried rice with roast turkey', price=Decimal('10500')),
            MenuItem(category=cat_mains, name='Grilled Tilapia & Ayamase', description='Whole tilapia with pepper sauce and plantain', price=Decimal('13500')),
            MenuItem(category=cat_grill, name='Suya Platter for Two', description='Beef, chicken and tripe suya with sides', price=Decimal('15000'), is_signature=True),
            MenuItem(category=cat_grill, name='Grilled T-Bone Steak', description='300g steak, pepper sauce, herb butter', price=Decimal('18500')),
            MenuItem(category=cat_grill, name='BBQ Ribs', description='Slow-cooked ribs with house BBQ glaze', price=Decimal('16500')),
            MenuItem(category=cat_desserts, name='Chocolate Lava Cake', description='Warm cake with molten centre & vanilla ice cream', price=Decimal('5500')),
            MenuItem(category=cat_desserts, name='Chin Chin Parfait', description='Layered cream, chin chin crumble & berries', price=Decimal('4500')),
            MenuItem(category=cat_drinks, name='Chapman', description='Nigeria\'s classic mocktail', price=Decimal('3500'), is_signature=True),
            MenuItem(category=cat_drinks, name='Zobo (House-made)', description='Hibiscus drink with ginger & pineapple', price=Decimal('2500')),
            MenuItem(category=cat_drinks, name='Fresh Juice (Watermelon/Pineapple)', description='Freshly pressed, no added sugar', price=Decimal('3000')),
            MenuItem(category=cat_drinks, name='Espresso / Cappuccino', description='Locally roasted beans', price=Decimal('2500')),
        ])

        # ---------- AMENITIES ----------
        self.stdout.write('Creating amenities...')
        amenity_data = [
            ('Infinity Pool & Sundeck', 'wellness', 'Solar-heated outdoor pool with cabanas and a swim-up bar.', 'waves', 'poolside.jpg', '6:00am – 9:00pm', True),
            ('Spa & Wellness Centre', 'wellness', 'Massages, facials and an open-air relaxation lounge.', 'flower-2', 'relaxation-area.jpg', '6:00am – 10:00pm', True),
            ('Fully-Equipped Gym', 'wellness', 'Modern cardio and strength equipment with a personal trainer on request.', 'dumbbell', '', '24 Hours', True),
            ('Grand Event Hall', 'business', 'A 600-capacity hall for weddings, galas and conferences.', 'presentation', 'event-hall.jpg', 'By Booking', True),
            ('Business Centre', 'business', 'Private meeting rooms, printing and high-speed WiFi.', 'briefcase', '', '7:00am – 9:00pm', False),
            ('High-Speed Fibre WiFi', 'convenience', 'Complimentary fibre internet throughout the property.', 'wifi', '', '24 Hours', True),
            ('Airport Shuttle', 'convenience', 'Scheduled and on-demand transfers to Yakubu Gowon Airport.', 'car', '', 'On Request', False),
            ('Laundry & Dry Cleaning', 'convenience', 'Same-day laundry service, item-based pricing.', 'shirt', '', '7:00am – 8:00pm', False),
            ('24/7 Power Backup', 'safety', 'Solar-backed generators ensure uninterrupted power at all times.', 'battery-charging', '', 'Always On', True),
            ('Gated Security & CCTV', 'safety', '24-hour manned security, CCTV coverage and secure parking.', 'shield-check', '', '24 Hours', False),
        ]
        for name, category, desc, icon, image_name, hours, highlight in amenity_data:
            a = Amenity(name=name, category=category, description=desc, icon=icon, hours=hours, is_highlighted=highlight)
            if image_name:
                img_file = img(image_name)
                if img_file:
                    a.image.save(image_name, img_file, save=False)
            a.save()

        # ---------- EVENT SPACES ----------
        self.stdout.write('Creating event spaces...')
        grand_hall = EventSpace.objects.create(
            name='Grand Event Hall', description='A soaring double-height hall with a private balcony, professional lighting rig and full catering capability — built for weddings, galas and large conferences.',
            capacity_seated=600, capacity_standing=800, price_per_hour=Decimal('250000'),
            features='Stage, Professional PA System, LED Lighting Rig, Balcony Seating, Full Catering, Bridal Suite, Ample Parking',
        )
        img_file = img('event-hall.jpg')
        if img_file:
            grand_hall.image.save('event-hall.jpg', img_file, save=True)

        conf_room = EventSpace.objects.create(
            name='Conference Room', description='A boardroom-style space with natural light, ideal for corporate meetings, training sessions and small conferences.',
            capacity_seated=80, capacity_standing=120, price_per_hour=Decimal('80000'),
            features='Projector, Video Conferencing, Whiteboard, High-Speed WiFi, Coffee Station, Breakout Area',
        )
        img_file = img('restaurant.jpg')
        if img_file:
            conf_room.image.save('restaurant.jpg', img_file, save=True)

        # ---------- GALLERY ----------
        self.stdout.write('Creating gallery...')
        gallery_data = [
            ('Hotel Exterior at Dusk', 'exterior', 'building.jpg'),
            ('Grand Entrance', 'exterior', 'building.jpg'),
            ('Exclusive Suite', 'rooms', 'exclusive-room.jpg'),
            ('Standard Room', 'rooms', 'standard-room.jpg'),
            ('The Seemetric Room Restaurant', 'restaurant', 'restaurant.jpg'),
            ('Grand Event Hall', 'events', 'event-hall.jpg'),
            ('Infinity Pool', 'pool', 'poolside.jpg'),
            ('Spa & Relaxation Lounge', 'spa', 'relaxation-area.jpg'),
        ]
        for i, (title, category, name) in enumerate(gallery_data):
            img_file = img(name)
            if img_file:
                g = GalleryImage(title=title, category=category, order=i)
                g.image.save(name, img_file, save=True)

        # ---------- BLOG ----------
        self.stdout.write('Creating blog posts...')
        posts = [
            dict(title='5 Must-Visit Spots Near Rayfield, Jos', slug='must-visit-spots-rayfield-jos', category='local',
                 excerpt='From Rayfield Park to the Riyom Rock formations, here is how to spend a weekend around our neighbourhood.',
                 content='Jos is one of Nigeria\'s most scenic cities, and Rayfield sits right at its heart.\n\nStart your morning at Rayfield Park, a short walk from the hotel, before heading out to the dramatic Riyom Rock formations. In the afternoon, the Jos Wildlife Park offers a relaxed safari experience for the whole family.\n\nEnd the day back at Xceptional Place — our rooftop offers one of the best sunset views in the city.',
                 image='building.jpg', date=date.today() - timedelta(days=14)),
            dict(title='Introducing Our AI Concierge: Ask, Order, Relax', slug='introducing-ai-concierge', category='hotel-news',
                 excerpt='Meet Xcep, the AI concierge now available to every guest on web and WhatsApp.',
                 content='We\'re excited to introduce Xcep, our new AI concierge. Available 24/7 on our website and WhatsApp, Xcep can answer questions about your stay, recommend the right room for your needs, and even place conversational orders — just say "bring towels and jollof to room 204" and it\'s done.\n\nEvery request is tracked live in your My Stay dashboard, from New through to Delivered.',
                 image='poolside.jpg', date=date.today() - timedelta(days=5)),
            dict(title='A Taste of Plateau: The Story Behind Our Jollof', slug='taste-of-plateau-jollof-story', category='food',
                 excerpt='Our Executive Chef shares what makes the Xceptional Place jollof rice a signature dish.',
                 content='Every hotel claims to have the best jollof — we let our guests be the judge. Our Executive Chef sources tomatoes and peppers from Plateau\'s highland farms, slow-smoking the rice over charcoal for a depth of flavour you won\'t find on a stovetop.\n\nPair it with our suya-spiced grilled chicken, available all day through room service.',
                 image='restaurant.jpg', date=date.today() - timedelta(days=30)),
        ]
        for p in posts:
            bp = BlogPost(title=p['title'], slug=p['slug'], category=p['category'], excerpt=p['excerpt'], content=p['content'], published_date=p['date'])
            img_file = img(p['image'])
            if img_file:
                bp.cover_image.save(p['image'], img_file, save=True)
            else:
                bp.save()

        # ---------- TESTIMONIALS ----------
        self.stdout.write('Creating testimonials...')
        Testimonial.objects.bulk_create([
            Testimonial(guest_name='Amaka O.', location='Lagos', rating=5, room_stayed='Exclusive Suite', stay_date=date.today() - timedelta(days=20),
                        comment='The AI concierge on WhatsApp genuinely surprised me — I ordered dinner without leaving the bed! Rooms are immaculate and the pool view is stunning.'),
            Testimonial(guest_name='David T.', location='Abuja', rating=5, room_stayed='Presidential Villa', stay_date=date.today() - timedelta(days=40),
                        comment='Booked our company retreat here. The event hall handled 300 of us effortlessly and the front desk team was sharp and professional throughout.'),
            Testimonial(guest_name='Grace M.', location='Jos', rating=4, room_stayed='Standard Room', stay_date=date.today() - timedelta(days=8),
                        comment='Great value, spotless room, and the power never went out once during our 3-night stay — a rarity in Jos! Restaurant jollof is excellent.'),
            Testimonial(guest_name='Ibrahim S.', location='Kano', rating=5, room_stayed='Deluxe Room', stay_date=date.today() - timedelta(days=55),
                        comment='Booking and paying with Paystack took two minutes. Check-in was seamless and the staff remembered my name the whole stay.'),
            Testimonial(guest_name='Chidinma A.', location='Port Harcourt', rating=5, room_stayed='Exclusive Suite', stay_date=date.today() - timedelta(days=3),
                        comment='My Stay portal made ordering laundry and extra towels so easy — I tracked every request in real time from my phone.'),
            Testimonial(guest_name='Emeka N.', location='Enugu', rating=4, room_stayed='Presidential Villa', stay_date=date.today() - timedelta(days=65),
                        comment='Proposed to my now-fiancée in the Presidential Villa — the romantic setup add-on made it unforgettable. Highly recommend.'),
        ])

        # ---------- BOOKINGS + SERVICE ORDERS ----------
        self.stdout.write('Creating sample bookings...')
        today = date.today()
        sample_bookings = [
            dict(room=exclusive, ci=today, co=today + timedelta(days=3), name='Ngozi Adeyemi', email='ngozi.a@example.com', phone='+2348012345671', status='checked_in', pay='paid'),
            dict(room=standard, ci=today, co=today + timedelta(days=2), name='Tunde Balogun', email='tunde.b@example.com', phone='+2348012345672', status='confirmed', pay='paid'),
            dict(room=presidential, ci=today - timedelta(days=1), co=today + timedelta(days=4), name='Fatima Bello', email='fatima.bello@example.com', phone='+2348012345673', status='checked_in', pay='paid'),
            dict(room=deluxe, ci=today + timedelta(days=2), co=today + timedelta(days=5), name='Samuel Okafor', email='samuel.okafor@example.com', phone='+2348012345674', status='confirmed', pay='paid'),
            dict(room=standard, ci=today - timedelta(days=3), co=today, name='Blessing Eze', email='blessing.eze@example.com', phone='+2348012345675', status='checked_in', pay='paid'),
            dict(room=exclusive, ci=today + timedelta(days=7), co=today + timedelta(days=10), name='Yakubu Danladi', email='yakubu.d@example.com', phone='+2348012345676', status='confirmed', pay='partial'),
        ]
        addons_all = list(AddOn.objects.all())
        created_bookings = []
        for sb in sample_bookings:
            nights = (sb['co'] - sb['ci']).days
            room_total = sb['room'].base_price * nights
            picked_addons = random.sample(addons_all, k=random.randint(0, 2))
            addon_total = sum([a.price for a in picked_addons], Decimal('0'))
            booking = Booking.objects.create(
                room_type=sb['room'], check_in=sb['ci'], check_out=sb['co'],
                adults=random.choice([1, 2, 2, 3]), children=random.choice([0, 0, 1]),
                full_name=sb['name'], email=sb['email'], phone=sb['phone'],
                special_requests='', room_total=room_total, addon_total=addon_total,
                grand_total=room_total + addon_total, status=sb['status'], payment_status=sb['pay'],
                payment_method='Paystack',
            )
            booking.addons.set(picked_addons)
            created_bookings.append(booking)

        # Feature one memorable reference code for demo purposes
        demo_booking = created_bookings[0]
        demo_booking.reference_code = 'XPH-DEMO001'
        demo_booking.save()

        # Service orders on a couple of in-house bookings
        self.stdout.write('Creating service orders...')
        in_house = [b for b in created_bookings if b.status == 'checked_in']
        order_templates = [
            ('food', '2x Jollof Rice & Grilled Chicken, 1x Chapman', 22500, 'new'),
            ('laundry', '3x Shirts, 1x Trousers', 6500, 'acknowledged'),
            ('housekeeping', 'Extra towels and fresh bedding, please', 0, 'in_progress'),
            ('extra', 'Airport Pickup — arriving 6:40pm, Air Peace flight', 18000, 'ready'),
            ('food', '1x Suya Platter for Two, 2x Zobo', 20000, 'delivered'),
        ]
        for b in in_house:
            for order_type, details, amount, status in random.sample(order_templates, k=min(3, len(order_templates))):
                ServiceOrder.objects.create(
                    booking=b, order_type=order_type, details=details, amount=amount,
                    payment_option=random.choice(['charge_to_room', 'pay_instantly']), status=status,
                )
        # ensure demo booking has a full spread of statuses for the live tracker
        ServiceOrder.objects.filter(booking=demo_booking).delete()
        demo_statuses = ['new', 'acknowledged', 'in_progress', 'ready', 'delivered']
        for i, (order_type, details, amount, _) in enumerate(order_templates):
            ServiceOrder.objects.create(
                booking=demo_booking, order_type=order_type, details=details, amount=amount,
                payment_option='charge_to_room', status=demo_statuses[i % len(demo_statuses)],
            )

        # ---------- EVENT INQUIRIES ----------
        self.stdout.write('Creating event inquiries...')
        EventInquiry.objects.create(full_name='Peace Momoh', email='peace.momoh@example.com', phone='+2348012349001',
                                     event_type='wedding', event_space=grand_hall, preferred_date=today + timedelta(days=60),
                                     guest_count=450, message='Looking for a full wedding package including decor and catering.', status='new')
        EventInquiry.objects.create(full_name='Solomon Danjuma', email='solomon.d@example.com', phone='+2348012349002',
                                     event_type='conference', event_space=conf_room, preferred_date=today + timedelta(days=25),
                                     guest_count=60, message='2-day corporate training, need projector and breakout catering.', status='quoted')

        # ---------- CONTACT INQUIRIES ----------
        ContactInquiry.objects.create(name='Mary Johnson', email='mary.j@example.com', phone='+2348012349999', subject='feedback', message='Wonderful stay — just wanted to say thank you to the housekeeping team!')

        # ---------- STAFF USERS ----------
        self.stdout.write('Creating staff accounts...')
        staff_data = [
            ('admin', 'admin12345', 'super_admin', 'Halima', 'Yusuf', True),
            ('frontdesk', 'staff12345', 'front_desk', 'Peter', 'Obi', False),
            ('kitchen', 'staff12345', 'kitchen', 'Rose', 'Nkem', False),
            ('laundry', 'staff12345', 'laundry', 'Musa', 'Aliyu', False),
            ('housekeeping', 'staff12345', 'housekeeping', 'Joy', 'Effiong', False),
        ]
        for username, password, role, first, last, is_super in staff_data:
            user = User.objects.create_user(username=username, password=password, first_name=first, last_name=last, is_staff=True, is_superuser=is_super)
            profile = StaffProfile.objects.create(user=user, role=role, phone='+23480' + str(random.randint(10000000, 99999999)))
            for d in range(3):
                ShiftSchedule.objects.create(staff=profile, date=today + timedelta(days=d), shift=random.choice(['morning', 'afternoon', 'night']))

        self.stdout.write(self.style.SUCCESS('\n✔ Demo data seeded successfully!'))
        self.stdout.write(self.style.SUCCESS(f'  Demo booking reference: {demo_booking.reference_code} (email: {demo_booking.email})'))
        self.stdout.write(self.style.SUCCESS('  Staff logins: admin/admin12345, frontdesk/staff12345, kitchen/staff12345, laundry/staff12345, housekeeping/staff12345'))
