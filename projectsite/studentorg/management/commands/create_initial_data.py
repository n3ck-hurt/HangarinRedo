import random

from django.core.management.base import BaseCommand
from faker import Faker

from studentorg.models import College, OrgMember, Organization, Program, Student

CATEGORIES = ['Handguns', 'Rifles', 'Shotguns', 'Tactical', 'Hunting', 'Competition']
CALIBERS = {
    'Handguns': ['9mm', '.45 ACP', '.40 S&W', '10mm'],
    'Rifles': ['5.56 NATO', '.308 Win', '7.62x39', '.300 BLK'],
    'Shotguns': ['12 Gauge', '20 Gauge'],
    'Tactical': ['5.56 NATO', '9mm', '.308 Win'],
    'Hunting': ['.308 Win', '.30-06', '12 Gauge'],
    'Competition': ['9mm', '.22 LR', '5.56 NATO'],
}
FIREARM_NAMES = [
    'Defender 9', 'Patriot X15', 'Trailblazer 308', 'Guardian 12',
    'Shadow Ops', 'Frontier Hunter', 'Strike One', 'Ironclad Pro',
]


class Command(BaseCommand):
    help = 'Create sample gun store data (categories, calibers, firearms, customers, sales)'

    def handle(self, *args, **kwargs):
        self.create_categories()
        self.create_calibers()
        self.create_firearms(12)
        self.create_customers(40)
        self.create_sales(15)

    def create_categories(self):
        for name in CATEGORIES:
            College.objects.get_or_create(college_name=name)
        self.stdout.write(self.style.SUCCESS(f'{len(CATEGORIES)} categories ready.'))

    def create_calibers(self):
        count = 0
        for college in College.objects.all():
            for caliber in CALIBERS.get(college.college_name, ['9mm', '.308 Win']):
                Program.objects.get_or_create(prog_name=caliber, college=college)
                count += 1
        self.stdout.write(self.style.SUCCESS(f'{count} calibers ready.'))

    def create_firearms(self, count):
        fake = Faker()
        for i in range(count):
            college = College.objects.order_by('?').first()
            name = random.choice(FIREARM_NAMES) + f' Mk-{i + 1}'
            Organization.objects.create(
                name=name,
                college=college,
                description=fake.sentence(nb_words=8),
                price=round(random.uniform(299, 2499), 2),
            )
        self.stdout.write(self.style.SUCCESS(f'{count} firearms added to catalog.'))

    def create_customers(self, count):
        fake = Faker()
        for _ in range(count):
            Student.objects.create(
                student_id=f'CUST-{fake.random_number(digits=6)}',
                lastname=fake.last_name(),
                firstname=fake.first_name(),
                middlename=fake.last_name()[:1],
                program=Program.objects.order_by('?').first(),
            )
        self.stdout.write(self.style.SUCCESS(f'{count} customers created.'))

    def create_sales(self, count):
        fake = Faker()
        for _ in range(count):
            OrgMember.objects.create(
                student=Student.objects.order_by('?').first(),
                organization=Organization.objects.order_by('?').first(),
                date_joined=fake.date_between(start_date='-2y', end_date='today'),
            )
        self.stdout.write(self.style.SUCCESS(f'{count} sales records created.'))
