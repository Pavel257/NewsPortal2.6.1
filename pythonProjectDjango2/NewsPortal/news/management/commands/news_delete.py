from django.core.management.base import BaseCommand, CommandError

from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаление новостей'  # 'Подсказка вашей команды'
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том,
                                        # что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))

        try:
            category = Category.get(name=options['category'])
            Post.objects.filter(category == category).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Успешно удалены все новости из категории {category.name}'))  # в случае неправильного подтверждения говорим, что в доступе отказано
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не удалось найти категорию {""}'))