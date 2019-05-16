from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User

from .forms import PlayerForm, EditPlayerForm, CityForm, EditCityOwner, SearchCoordsForm, SearchPlayerForm, UserRegistrationForm, EditProfileForm
import string

""" STILL WRITING TESTS"""

# Test that forms are validating correctly, and don't accept invalid data

class PlayerFormTests(TestCase):

    def test_can_add_player(self):
        form_data = {"name": "Belle", "team": "GRY", "rank": 7}
        form = PlayerForm(form_data)
        self.assertTrue(form.is_valid())

    def test_missing_username(self):
        invalid_texts = list(string.whitespace) + ['   ', '\n\n\n', '\t\t\n\t']
        form_data = {"name": invalid_texts, "team": "GRY", "rank": 7}
        form = PlayerForm(form_data)
        self.assertFalse(form.is_valid())

    def test_duplicate_player(self):
        form_data = {"name": "Belle", "team": "GRY", "rank": 7}
        form = PlayerForm(form_data)
        form_data = {"name": "Belle", "team": "GRY", "rank": 7}
        form = PlayerForm(form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_team_name(self):
        form_data = {"name": "Belle", "team": "GREY", "rank": 7}
        form = PlayerForm(form_data)
        self.assertFalse(form.is_valid())


class CityFormTests(TestCase):

    def test_can_add_city(self):
        form_data = {"coords": "0001,0001", "player": 1, "culture": "CN", "quality": "GLD"}
        form = CityForm(form_data)
        self.assertTrue(form.is_valid())


class RegistrationFormTests(TestCase):


    def test_register_user_with_valid_data_is_valid(self):
        form_data = { 'username' : 'bob' , 'email' : 'bob@bob.com', 'first_name' : 'bob', 'last_name' : 'whatever', 'password1' : 'q!w$er^ty6ui7op', 'password2' : 'q!w$er^ty6ui7op' }
        form = UserRegistrationForm(form_data)
        self.assertTrue(form.is_valid())


    def test_register_user_with_missing_data_fails(self):
        form_data = { 'username': 'bob', 'email' : 'bob@bob.com', 'first_name' : 'bob', 'last_name' : 'whatever', 'password1' : 'q!w$er^ty6ui7op', 'password2' : 'q!w$er^ty6ui7op' }
        # Remove each key-value from dictionary, assert form not valid
        for field in form_data.keys():
            data = dict(form_data)
            del(data[field])
            form = UserRegistrationForm(data)
            self.assertFalse(form.is_valid())


    def test_register_user_with_password_mismatch_fails(self):
        form_data = { 'username' : 'another_bob' , 'email' : 'bob@bob.com', 'first_name' : 'bob', 'last_name' : 'whatever', 'password1' : 'q!w$er^ty6ui7op', 'password2' : 'dr%$ESwsdgdfh' }
        form = UserRegistrationForm(form_data)
        self.assertFalse(form.is_valid())


    def test_register_user_with_email_already_in_db_fails(self):

        # Create a user with email bob@bob.com
        bob = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        bob.save()

        # attempt to create another user with same email
        form_data = { 'username' : 'another_bob' , 'email' : 'bob@bob.com', 'first_name' : 'bob', 'last_name' : 'whatever', 'password1' : 'q!w$er^ty6ui7op', 'password2' : 'q!w$er^ty6ui7op' }
        form = UserRegistrationForm(form_data)
        self.assertFalse(form.is_valid())


    def test_register_user_with_username_already_in_db_fails(self):

        # Create a user with username bob
        bob = User(username='bob', email='bob@bob.com')
        bob.save()

        # attempt to create another user with same username
        form_data = {'username' : 'bob' , 'email' : 'another_bob@bob.com', 'first_name' : 'bob', 'last_name' : 'whatever', 'password1' : 'q!w$er^ty6ui7op', 'password2' : 'q!w$er^ty6ui7op' }
        form = UserRegistrationForm(form_data)
        self.assertFalse(form.is_valid())



class EditProfileFormTests(TestCase):
    """Edit Profile Form Tests"""

    # test that the user can change their profile
    def test_user_can_change_profile_data(self):
        aj = User(username='AJTesting', email='aj@testing.com', first_name='AJ', last_name='TestTest')
        aj.save()
        form_data = { 'username' : 'AJTesting' , 'email' : 'aj@testing.com', 'first_name' : 'AJ', 'last_name' : 'NEWLastName'}
        form = EditProfileForm(form_data)
        self.assertTrue(form.is_valid())

    # test that edit profile does not accept invalid data, in this case that the user cannot change their email to one that exists
    def test_user_edit_profile_invalid_data(self):
        # Create test user
        aj = User(username='AJTesting', email='aj@testing.com', first_name='AJ', last_name='TestTest')
        aj.save()
        # create a second test user
        new_aj = User(username='AJTest2', email='aj2@testing.com', first_name='AJ', last_name='NumberTwo')
        new_aj.save()
        # try to edit the profile form to an email that already exists
        form_data = {'username': 'AJTest2', 'email': 'aj@testing.com', 'first_name': 'AJ', 'last_name': 'NumberTwo'}
        form = EditProfileForm(form_data)
        self.assertFalse(form.is_valid())


class EditPlayerFormTests(TestCase):
    """Test that User can change player"""

    def test_can_edit_player(self):
        # create test player, then edit the player with editPlayerForm
        # if form is valid, test should pass
        form_data = {"name": "Belle", "team": "GRY", "rank": 7}
        form = PlayerForm(form_data)
        edit_form_data = {'player_pk': form.player_pk, "name": "Belle", "team": "DOA", "rank": 7}
        edit_form = EditPlayerForm(edit_form_data)
        self.assertTrue(edit_form.is_valid())


'''TESTS FOR TEMPLATES TO COME'''







