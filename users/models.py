from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, User
from django.core.validators import RegexValidator
from users.managers import CustomUserManager
from django.db.models import Q
from enum import Enum
import names
import random
# from friending.models import Friending
from django.apps import apps
from django.urls import reverse

# Create your models here.


class AppUser(AbstractUser):
    username = models.CharField(
        max_length=49, unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures', default='media/profile_pictures/default-profile-picture_xdklkn.jpg')
    cover_photo = models.ImageField(null=True, upload_to='cover_photos')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [username]
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_profile_picture(self, h, w):
        if self.profile_picture and 'upload/' in self.profile_picture.url:
            return self.profile_picture.url.replace('upload/', f'upload/c_fill,h_{h},w_{w}/')
        else:
            return 'https://res.cloudinary.com/dtgokkyl1/image/upload/v1683470568/media/basic_images/default-profile-picture_me5ztx.jpg'

    def get_profile_picture_round(self):
        return self.get_profile_picture(160, 160)

    def get_profile_picture_mini(self):
        return self.get_profile_picture(40, 40)

    def get_profile_picture_search(self):
        return self.get_profile_picture(60, 60)

    def get_profile_picture_friend(self):
        return self.get_profile_picture(80, 80)

    def get_cover_photo(self):
        if self.cover_photo and 'upload/' in self.cover_photo.url:
            return self.cover_photo.url.replace('upload/', 'upload/c_fill,h_463,w_1241/')
        else:
            return 'https://res.cloudinary.com/dtgokkyl1/image/upload/v1683470571/media/basic_images/default-cover-photo_furh0o.jpg'

    """
    NEW
    """
    @classmethod
    def get_users_data(cls, current_user, users, mode='friend'):
        Friending = apps.get_model('friending.Friending')
        friending_states = Friending.get_friend_states_from_users(
            current_user, users)
        data = []
        for user in users:
            user_info = {
                'full_name': user.__str__(),
                'profile_picture': user.get_profile_picture_friend() if mode == 'friend' else user.get_profile_picture_search(),
                'friend_state': friending_states[user.id],
                'main_url': reverse('main:main', args=(user.id,)),
                'urls': {
                    'add_friend': reverse('friending:general', args=(user.id,)),
                    'cancel_request': reverse('friending:delete', args=(user.id,)),
                    'confirm_request': reverse('friending:update', args=(user.id,)),
                    'delete_request': reverse('friending:delete', args=(user.id,)),
                    'unfriend': reverse('friending:delete', args=(user.id,)),
                }
            }
            data.append(user_info)
        return data

    @classmethod
    def get_profile_data(cls, current_user, second_user_id):
        Friending = apps.get_model('friending.Friending')

        qs = AppUser.objects.filter(pk=second_user_id)
        if not qs:
            return None
        second_user = qs.get()
        current_user_raw_friending = {
            'uid': second_user_id,
            'state': None,
            'sent': None,
        }

        def get_friend_ids(set):
            data = []
            for fr in set:
                if fr.second_id == current_user.id or fr.first_id == current_user.id:
                    current_user_raw_friending['state'] = fr.state
                    current_user_raw_friending['sent'] = fr.sent
                if fr.state == Friending.FriendState.FRIENDED:
                    data.append(fr.first_id if fr.second_id ==
                                second_user_id else fr.second_id)
            return data

        all_friendings = Friending.get_all_friendings(second_user)
        fr_ids = get_friend_ids(
            all_friendings)

        data = {
            'second_user_id': second_user_id,
            # urls
            'posts_index_url': reverse('posts:create_index', args=(second_user_id,)),
            'posts_create_url': reverse('posts:create_index', args=(second_user_id,)),
            'upload_cover_photo_url': reverse('users:upload_cover', args=()),
            'upload_profile_picture_url': reverse('users:upload_profile', args=()),
            'friending_index_url': reverse('friending:index', args=(second_user_id,)),
            'friending_requests_url': reverse('friending:requests', args=()),
            # profile info
            'profile_picture_url_round': second_user.get_profile_picture_round(),
            'cover_url': second_user.get_cover_photo(),
            'first_name': second_user.first_name,
            'last_name': second_user.last_name,
            'num_friends': len(fr_ids),
            'main_friending_state': Friending.get_friend_state(current_user, current_user_raw_friending),
            'friending_urls': {
                'add_friend': reverse('friending:general', args=(second_user_id,)),
                'cancel_request': reverse('friending:delete', args=(second_user_id,)),
                'confirm_request': reverse('friending:update', args=(second_user_id,)),
                'delete_request': reverse('friending:delete', args=(second_user_id,)),
                'unfriend': reverse('friending:delete', args=(second_user_id,)),
            }
        }
        return data

    """
    FOR SEEDING
    """
    @classmethod
    def make_user(cls, isTestUser=False):
        images = [
            'media/profile_pictures/anne-hathaway_wtefas.jpg',
            'media/profile_pictures//tuong_san_pzuffr.jpg',
            'media/profile_pictures/A-Hau-Tuong-San-2-01_zyvldm.jpg',
            'media/profile_pictures/tang_thanh_ha_rbryku.jpg',
            'media/profile_pictures/chris_e9yeky.jpg',
            'media/profile_pictures/casemiro_xwaave.jpg',
            'media/profile_pictures/elizabeth_olsen_etrm8v.jpg',
            'media/profile_pictures/Cristiano_Ronaldo_2018_llglx2.jpg',
            'media/profile_pictures/scarlett_johansson_p7ctuy.jpg',
            'media/profile_pictures/katheryn_winnick_i00jun.jpg',
        ]
        if isTestUser:
            first_name = 'Test'
            last_name = 'User'
            username = 'test'
            email = username + "@gmail.com"
            password = 'test1234'
        else:
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            username = first_name.lower() + str(random.randint(100, 10000))
            email = username + "@gmail.com"
            password = 'abc123'
        try:
            user = AppUser.objects.create_user(
                username, email, password, first_name=first_name, last_name=last_name, profile_picture=images[random.randint(0, len(images) - 1)])
        except Exception as e:
            print(e)
            return None
        return user

    """
    OLD
    """


"""
    def get_user_info(self, user, mode='friend'):
        Friending = apps.get_model('friending.Friending')
        r = {
            'full_name': user.__str__(),
            'profile_picture': user.get_profile_picture_friend() if mode == 'friend' else user.get_profile_picture_search(),
            'friend_state': Friending.get_state(self, user),
            'main_url': reverse('main:main', args=(user.id,)),
            'urls': {
                'add_friend': reverse('friending:general', args=(user.id,)),
                'cancel_request': reverse('friending:delete', args=(user.id,)),
                'confirm_request': reverse('friending:update', args=(user.id,)),
                'delete_request': reverse('friending:delete', args=(user.id,)),
                'unfriend': reverse('friending:delete', args=(user.id,)),
            }
        }
        return r
"""
