from graphene_django import DjangoObjectType
import graphene
from .models import PersonalNote as PersonalNoteModel


class PersonalNote(DjangoObjectType):

    class Meta:
        model = PersonalNoteModel
        # Describe the data as a node in the graph
        interface = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    notes = graphene.List(PersonalNote)

    def resolve_notes(self, info):
        """Decide which notes to return."""
        # import pdb; pdb.set_trace()
        user = info.context.user # Find with pdb

        if user.is_anonymous:
            return PersonalNoteModel.objects.none()
        else:
            return PersonalNote.Model.objects.filter(user = user)