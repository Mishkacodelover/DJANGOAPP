import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone


from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_quesstion(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quién es el mejor Coure Director de Platzi?",pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

def create_question(question_text,days):
    """Create a question with the given "question_text, nad publish the 
    given numer of days ofset to no
    (negative for question published on the past. POsitive for question that have yet to be published)"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date = time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """If not question exist, an appropiate message is display"""
        response = self.client.get(reverse("polls:index"))  
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[]) 
        #el método reverse me permite no hardcodear la url  poder traermela en una variable

    def test_future_question(self):
        """
        questions wiht a pub_date in the fture are not publish in th index
        """
        create_question("Future question",days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response,"No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_past_question(self):   
        """
        questions wiht a pub_date in the past are not publish in th index
        """
        question = create_question("Past question",days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])


    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions are
        displayed
        """
        past_question = create_question(question_text="Past question",days=-30)
        future_question = create_question(question_text="Future question",days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )


    def test_two_past_questions(self):
        """
        the question index page may display multiple questions
        """
        past_question1 = create_question(question_text="Past question 1",days=-30)
        past_question2 = create_question(question_text="Past question 2",days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1,past_question2]
        )

    def test_two_future_questions(self):
        """
        the question index page may display multiple questions
        """
        future_question1 = create_question(question_text="Future question 1",days=30)
        future_question2 = create_question(question_text="Future question 2",days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        the detail view of a question with a pub_date in the future 
        returns a 404 error not found
        """
        future_question = create_question(question_text="Future question 1",days=30)
        url = reverse("polls:detail",args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        """
        the detail view of a question with a pub_date in the past 
        dispplays the question's text
        """
        past_question = create_question(question_text="Past question",days=-30)
        url = reverse("polls:detail",args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)