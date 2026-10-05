from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Generate API token for a user'
    
    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username')
    
    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} not found'))
            return
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ New token created for {username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'⚠️ Token already exists for {username}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n🔑 API Token: {token.key}'))
        self.stdout.write(self.style.WARNING(f'\nKeep this token secret! Use it in API requests:\n'))
        self.stdout.write(f'curl -H "Authorization: Token {token.key}" http://localhost:8000/api/alerts/')