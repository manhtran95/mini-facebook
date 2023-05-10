from django.db import models
from users.models import AppUser
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from typing import List
from django.urls import reverse

# Create your models here.


class Friending(models.Model):
    class FriendState(models.TextChoices):
        PENDING = "PE", _("Pending")
        FRIENDED = "FR", _("Friended")

    first = models.ForeignKey(
        AppUser, related_name='first_friending', on_delete=models.CASCADE)
    second = models.ForeignKey(
        AppUser, related_name='second_friending', on_delete=models.CASCADE)
    sent = models.BigIntegerField('request_sent_user')
    state = models.CharField(
        max_length=2,
        choices=FriendState.choices,
        default=FriendState.PENDING,
    )
    friend_datetime = models.DateTimeField(
        'datetime friended', null=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['first', 'second'], name='friend_request')
        ]
        indexes = [
            models.Index(fields=('first', 'second')),
        ]

    @classmethod
    def are_friends(cls, user1, user2):
        smallId, bigId = min(user1.id, user2.id), max(user1.id, user2.id)
        return cls.objects.filter(first_id=smallId, second_id=bigId).filter(state=cls.FriendState.FRIENDED).exists()

    class State:
        self = 'SELF'
        non_friend = 'NON-FRIEND'
        request_sent = 'REQUEST-SENT'
        request_received = 'REQUEST-RECEIVED'
        friend = 'FRIEND'

    @classmethod
    def get_state(cls, user1, user2):
        smallId, bigId = min(user1.id, user2.id), max(user1.id, user2.id)
        if smallId == bigId:
            return cls.State.self
        q = cls.objects.filter(first_id=smallId, second_id=bigId)
        if not q.exists():
            return cls.State.non_friend
        # q exists
        rec = q.get()
        if rec.state == cls.FriendState.FRIENDED:
            return cls.State.friend
        # FriendState == 'PENDING'
        if rec.sent == user1.id:
            return cls.State.request_sent
        else:
            return cls.State.request_received

    @classmethod
    def add_friend(cls, user, second_user):
        smallId, bigId = min(user.id, second_user.id), max(
            user.id, second_user.id)
        if smallId == bigId:
            raise Exception('Can not befriend with oneself.')
        Friending(first_id=smallId, second_id=bigId, sent=user.id).save()
        return

    @classmethod
    def accept_request(cls, user, second_user):
        smallId, bigId = min(user.id, second_user.id), max(
            user.id, second_user.id)
        Friending.objects.filter(first_id=smallId, second_id=bigId).update(
            state=cls.FriendState.FRIENDED)
        return

    @classmethod
    def delete(cls, user, second_user):
        smallId, bigId = min(user.id, second_user.id), max(
            user.id, second_user.id)
        Friending.objects.filter(first_id=smallId, second_id=bigId).delete()
        return

    @classmethod
    def get_all_friend_friendings(cls, user):
        return Friending.objects.filter(Q(first_id=user.id) | Q(second_id=user.id),
                                        state=cls.FriendState.FRIENDED)

    @classmethod
    def get_all_friend_users(cls, user) -> List[AppUser]:
        all_friendings = cls.get_all_friend_friendings(user)
        ids = [fr.second_id if fr.first_id ==
               user.id else fr.first_id for fr in all_friendings]
        l = [AppUser.objects.get(pk=id)
             for id in ids]
        return l

    @classmethod
    def get_all_friendings(cls, user) -> List:
        return Friending.objects.filter(Q(first_id=user.id) | Q(second_id=user.id))

    @classmethod
    def get_friend_requests(cls, user) -> List[AppUser]:
        all_received_pending_friendings = cls.get_all_friendings(user).filter(
            state=cls.FriendState.PENDING).filter(~Q(sent=user.id))
        sent_ids = [fr.second_id if fr.first_id ==
                    user.id else fr.first_id for fr in all_received_pending_friendings]
        sent_users = [AppUser.objects.get(pk=id)
                      for id in sent_ids]
        return sent_users

    @classmethod
    def make_friends(cls, user, second_user):
        smallId, bigId = min(user.id, second_user.id), max(
            user.id, second_user.id)
        if smallId == bigId:
            raise Exception('Can not befriend with oneself.')
        state = cls.get_state(user, second_user)
        if state == cls.State.friend:
            return
        elif state == cls.State.non_friend:
            Friending(first_id=smallId, second_id=bigId, sent=user.id,
                      state=cls.FriendState.FRIENDED).save()
        else:
            Friending.objects.filter(first_id=smallId, second_id=bigId).update(
                state=cls.FriendState.FRIENDED)

    @classmethod
    def make_friend_requests(cls, user, second_user):
        smallId, bigId = min(user.id, second_user.id), max(
            user.id, second_user.id)
        if smallId == bigId:
            raise Exception('Can not befriend with oneself.')
        state = cls.get_state(user, second_user)
        if state == cls.State.non_friend:
            Friending(first_id=smallId, second_id=bigId,
                      state=cls.FriendState.PENDING, sent=user.id).save()
        else:
            Friending.objects.filter(first_id=smallId, second_id=bigId).update(
                state=cls.FriendState.PENDING, sent=user.id)

    @classmethod
    def get_user_info(cls, current_user, user):
        r = {
            'full_name': user.__str__(),
            'profile_picture': user.get_profile_picture_friend(),
            'friend_state': Friending.get_state(current_user, user),
            'profile_url': reverse('main:main', args=(user.id,)),
            'urls': {
                'add_friend': reverse('friending:general', args=(user.id,)),
                'cancel_request': reverse('friending:delete', args=(user.id,)),
                'confirm_request': reverse('friending:update', args=(user.id,)),
                'delete_request': reverse('friending:delete', args=(user.id,)),
                'unfriend': reverse('friending:delete', args=(user.id,)),
            }
        }
        return r