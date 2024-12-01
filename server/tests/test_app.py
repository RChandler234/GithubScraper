from flask_testing import TestCase
from app import create_app
from app.models import db


# Referencing flask_testing docs for setup: https://pythonhosted.org/Flask-Testing/
class MyTest(TestCase):
    def create_app(self):

        return create_app(
            config={"SQLALCHEMY_DATABASE_URI": "sqlite://", "TESTING": True}
        )

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class TestRoot(MyTest):
    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Welcome to GithubScraper!")
