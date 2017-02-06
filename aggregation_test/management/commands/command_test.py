from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('poll_id', nargs='+', type=int)

        # Named (optional arguments)
        parser.add_argument(
            '--add',
            action='store_true',
            dest='add',
            default=False,
            help='add'
        )
        parser.add_argument(
            '--substract',
            action='store_true',
            dest='substract',
            default=False,
            help='substract'
        )
        parser.add_argument(
            '--multiply',
            action='store_true',
            dest='multiply',
            default=False,
            help='multiply'
        )
        parser.add_argument(
            '--divide',
            action='store_true',
            dest='divide',
            default=False,
            help='divide'
        )


    def handle(self, *args, **options):
        s = ''
        result = 0
        tag = sum([options[i] for i in ['add', 'substract', 'multiply', 'divide']])
        if options['add'] or not tag:
            for poll_id in options['poll_id']:
                s += '{} + '.format(poll_id)
                result += poll_id
            self.stdout.write(self.style.SUCCESS('{}= {}'.format(s[:-2], result)))
        elif options['substract']:
            result += options['poll_id'][0]
            s = '{} - '.format(options['poll_id'][0])
            for poll_id in options['poll_id'][1:]:
                s += '{} - '.format(poll_id)
                result -= poll_id
            self.stdout.write(self.style.SUCCESS('{}= {}'.format(s[:-2], result)))
        elif options['multiply']:
            result = 1
            for poll_id in options['poll_id']:
                s += '{} × '.format(poll_id)
                result *= poll_id
            self.stdout.write(self.style.SUCCESS('{}= {}'.format(s[:-2], result)))
        elif options['divide']:
            result = options['poll_id'][0]
            s = '{} ÷ '.format(options['poll_id'][0])
            for poll_id in options['poll_id'][1:]:
                s += '{} ÷ '.format(poll_id)
                result /= poll_id
            self.stdout.write(self.style.SUCCESS('{}= {}'.format(s[:-2], result)))
