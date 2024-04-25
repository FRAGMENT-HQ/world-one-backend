from QBank.models import Chapter, Topic, Questions
from django.db.models import Q
from Backend.utils.constants import PrirorityConstants

def run():

    chapters = Chapter.objects.all()

    for chapter in chapters:
        print(chapter.name)
        topics = Topic.objects.filter(chapter=chapter)
        for topic in topics:
            # get question whose explanation is not empty or explanation image is not empty
            questions = Questions.objects.filter(Q(topic=topic) & (  ~Q(explanationImg__isnull=True) | ~Q(explanation="</>")) )

            if len(questions) <100:
                for question in questions:
                    question.priority = PrirorityConstants.HIGH
                    question.save()
            else:
                level1 = questions.filter(level=1)
                level2 = questions.filter(level=2)
                level3 = questions.filter(level=3)
                level4 = questions.filter(level=4)
                level5 = questions.filter(level=5)
                number = [20,20,20,20,20]
                if len(level1) < 20:
                    number[0]=20-len(level1)
                    number[1]=20 + len(level1)
                if len(level5) < 20:
                    number[4]=20-len(level5)
                    number[3]=20 + len(level5)
                counter = 0
                for question in level1:
                    question.priority = PrirorityConstants.HIGH
                    question.save()
                    counter+=1
                    if counter == number[0]:
                        break
                counter = 0
                for question in level2:
                    question.priority = PrirorityConstants.HIGH
                    question.save()
                    counter+=1
                    if counter == number[1]:
                        break
                counter = 0
                for question in level3:
                    question.priority = PrirorityConstants.HIGH
                    question.save()
                    counter+=1
                    if counter == number[2]:
                        break
                counter = 0
                for question in level4:
                    question.priority = PrirorityConstants.HIGH
                    question.save()
                    counter+=1
                    if counter == number[3]:
                        break
                counter = 0
                for question in level5:
                    question.priority = PrirorityConstants.HIGH
                    question.save()
                    counter+=1
                    if counter == number[4]:
                        break
            print("Done")
                    


                
            