import random
import os
import argparse

import django


def get_schoolkid(name):
    schoolkid = Schoolkid.objects.get(full_name__contains=name)
    return schoolkid


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=['2', '3'])
    for mark in bad_marks:
        mark.points = '5'
        mark.save()


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject):
    commendations = [
        'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!',
        'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!',
        'Очень хороший ответ!', 'Талантливо!',
        'Ты сегодня прыгнул выше головы!', 'Я поражен!',
        'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!',
        'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!',
        'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!', 'Я вижу, как ты стараешься!',
        'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!']

    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject
    ).order_by('?').first()

    Commendation.objects.create(
        text=random.choice(commendations),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
    )


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    django.setup()
    from datacenter.models import Mark, Chastisement, Schoolkid, Lesson, \
        Commendation

    parser = argparse.ArgumentParser(
        description='Скрипт исправляет плохие оценки, удаляет замечания'
                    'и добавляет хороший отзыв'
    )
    parser.add_argument('name', help='ФИО ученика')
    parser.add_argument('subject', help='Название предмета')
    args = parser.parse_args()

    try:
        schoolkid = get_schoolkid(args.name)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid, args.subject)
    except Schoolkid.DoesNotExist:
        print('Не найден ученик')
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено более одного ученика')
    except AttributeError:
        print('Неверное название предмета')
