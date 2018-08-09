from graphene_django import DjangoObjectType
import graphene
from .models import PersonalNote as PersonalNoteModel

class PersonalNote(DjangoObjectType):

    class Meta:
        model = PersonalNoteModel
        # Describe the data as a node in the graph
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    personalnotes = graphene.List(PersonalNote)

    def resolve_personalnotes(self, info):
        """Decide which notes to return."""
        # import pdb; pdb.set_trace()
        user = info.context.user # Find with pdb

        if user.is_anonymous:
            return PersonalNoteModel.objects.none()
        else:
            return PersonalNoteModel.objects.filter(user = user)

class CreatePersonalNote(graphene.Mutation):

    class Arguments:
        title = graphene.String()
        content = graphene.String()
    
    personalnote = graphene.Field(PersonalNote)
    ok = graphene.Boolean()

    def mutate(self, info, title, content):
        user = info.context.user

        if user.is_anonymous:
            return CreatePersonalNote(ok=False)
        else:
            new_note = PersonalNoteModel(title=title, content=content, user=user)
            new_note.save()
            return CreatePersonalNote(personalnote=new_note, ok=True)

class Mutation(graphene.ObjectType):
    create_personal_note = CreatePersonalNote.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)