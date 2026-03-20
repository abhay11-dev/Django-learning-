from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.wallets.models import Wallet

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test users with wallets for development'

    def handle(self, *args, **options):
        # Create test users
        test_users = [
            {'username': 'abhay', 'email': 'abhay@example.com', 'balance': 5000.00},
            {'username': 'test', 'email': 'test@example.com', 'balance': 3500.50},
        ]

        for user_data in test_users:
            username = user_data['username']
            balance = user_data['balance']
            
            # Check if user already exists
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': user_data['email']}
            )

            # Create or update wallet
            wallet, wallet_created = Wallet.objects.get_or_create(
                user=user,
                defaults={'balance': balance}
            )

            if wallet_created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created user "{username}" with wallet balance ₹{balance}'
                    )
                )
            else:
                # Update balance if wallet already existed
                wallet.balance = balance
                wallet.save()
                self.stdout.write(
                    self.style.WARNING(
                        f'⟳ Updated user "{username}" wallet balance to ₹{balance}'
                    )
                )

        self.stdout.write(self.style.SUCCESS('\n✓ Test data setup complete!'))
