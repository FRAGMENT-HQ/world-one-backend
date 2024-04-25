from QBank.models import user_chapter,Submision,Practice,Questions
from User.models import User,user_analytics
from datetime import datetime,timedelta

def user_chapter_map():
    submisions = Submision.objects.all()
    for sub in submisions:
        if user_chapter.objects.filter(user=sub.user,chapter=sub.practice.chapter).exists():
            user_chapter_obj = user_chapter.objects.get(user=sub.user,chapter=sub.practice.chapter)
            user_chapter_obj.total_questions += 1
            user_chapter_obj.total_time += (sub.end_time - sub.start_time).seconds
            if sub.correct:
                user_chapter_obj.correct_questions += 1
            user_chapter_obj.save()
        else:
            user_chapter_obj = user_chapter.objects.create(user=sub.user,chapter=sub.practice.chapter,rating=sub.user.rating,total_questions=1,correct_questions=1,total_time=(sub.end_time - sub.start_time).seconds)
            user_chapter_obj.save()
    

def user_analytics_map():
    for user in User.objects.all():
        for i in range(1,10):
            ua = user_analytics.objects.create(user=user.pk,total_questions=0,rating_change=0.0,time_spent=0.0,created_at=today,updated_at=today)
            ua.save()
            ua.created_at = today
            ua.updated_at = today
            ua.save()
            today = today - timedelta(days=1)
    print("Done")

        

def question_elo():
    rating_map = {
        "1":400,
        "2":800,
        "3":1200,
        "4":1600,
        "5":2000,
    }
    def convert_rating(rating):
        for key in rating_map:
            if rating_map[key] == rating:
                return key
        return 0
    questions = Questions.objects.all()
    for count,question in enumerate(questions):
        try:
            question.level = rating_map[str(question.level)]
            question.save()
        except:
            try:
                question.level = rating_map[str(convert_rating(question.level))]
                question.save()
            except:
                pass
        print(count,question.topic)
    print("Done")

def run():
    question_elo()
    user_analytics_map()

    