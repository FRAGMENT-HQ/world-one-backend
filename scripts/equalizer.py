from QBank.models import Chapter, Topic, Questions
from django.db.models import Q
from Backend.utils.constants import PrirorityConstants

def run():

    
        questions = Questions.objects.all()
        for question in questions:
            if question.explanationImg or question.explanation != "</>":
                question.priority = PrirorityConstants.MEDIUM
                question.save()
            else:
                question.priority = PrirorityConstants.LOW
                question.save()
        


                
            