from QBank.models import  Questions
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