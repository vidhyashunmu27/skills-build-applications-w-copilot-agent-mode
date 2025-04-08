from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import timedelta
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB and drop collections directly
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users
        users = [
            User(username='thundergod', email='thundergod@mhigh.edu', password='password1'),
            User(username='metalgeek', email='metalgeek@mhigh.edu', password='password2'),
            User(username='zerocool', email='zerocool@mhigh.edu', password='password3'),
            User(username='crashoverride', email='crashoverride@mhigh.edu', password='password4'),
            User(username='sleeptoken', email='sleeptoken@mhigh.edu', password='password5'),
        ]
        User.objects.bulk_create(users)

        # Save users to the database
        for user in users:
            user.save()

        # Create teams
        team1 = Team(name='Blue Team')
        team2 = Team(name='Gold Team')
        team1.save()
        team2.save()

        # Create activities with duration in seconds
        activities = [
            Activity(user=users[0], activity_type='Cycling', duration=3600),  # 1 hour
            Activity(user=users[1], activity_type='Crossfit', duration=7200),  # 2 hours
            Activity(user=users[2], activity_type='Running', duration=5400),  # 1 hour 30 minutes
            Activity(user=users[3], activity_type='Strength', duration=1800),  # 30 minutes
            Activity(user=users[4], activity_type='Swimming', duration=4500),  # 1 hour 15 minutes
        ]
        for activity in activities:
            activity.save()

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(team=team1, points=100),
            Leaderboard(team=team2, points=90),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event'),
            Workout(name='Crossfit', description='Training for a crossfit competition'),
            Workout(name='Running Training', description='Training for a marathon'),
            Workout(name='Strength Training', description='Training for strength'),
            Workout(name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
