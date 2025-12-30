from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import models as app_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        app_models.Activity.objects.all().delete()
        app_models.Workout.objects.all().delete()
        app_models.Leaderboard.objects.all().delete()
        app_models.Team.objects.all().delete()
        get_user_model().objects.all().delete()

        # Create Teams
        marvel = app_models.Team.objects.create(name='Team Marvel')
        dc = app_models.Team.objects.create(name='Team DC')

        # Create Users (Superheroes)
        users = [
            {'email': 'tony@stark.com', 'username': 'IronMan', 'team': marvel},
            {'email': 'steve@rogers.com', 'username': 'CaptainAmerica', 'team': marvel},
            {'email': 'bruce@wayne.com', 'username': 'Batman', 'team': dc},
            {'email': 'clark@kent.com', 'username': 'Superman', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = get_user_model().objects.create_user(email=u['email'], username=u['username'], password='password')
            user.team = u['team']
            user.save()
            user_objs.append(user)

        # Create Activities
        activities = [
            app_models.Activity.objects.create(user=user_objs[0], type='Run', duration=30),
            app_models.Activity.objects.create(user=user_objs[1], type='Swim', duration=45),
            app_models.Activity.objects.create(user=user_objs[2], type='Bike', duration=60),
            app_models.Activity.objects.create(user=user_objs[3], type='Yoga', duration=20),
        ]

        # Create Workouts
        workouts = [
            app_models.Workout.objects.create(name='Morning Cardio', description='Cardio for all'),
            app_models.Workout.objects.create(name='Strength Training', description='Strength for all'),
        ]

        # Create Leaderboard
        app_models.Leaderboard.objects.create(user=user_objs[0], points=100)
        app_models.Leaderboard.objects.create(user=user_objs[1], points=90)
        app_models.Leaderboard.objects.create(user=user_objs[2], points=80)
        app_models.Leaderboard.objects.create(user=user_objs[3], points=70)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
