from flask import request
from flask.views import MethodView

from src.database import Session

from flask_jwt_extended import jwt_required, get_jwt_identity
from src.schemas.tag import TagSchema
from src.utils.auth import token_required
from src.models import Tag

from src.utils import status


class TagsListView(MethodView):
    @token_required
    def get(self, _):
        with Session() as session:
            tags = session.query(Tag).filter(Tag.profile_id == self.id)
            return TagSchema(many=True).dump(tags)

    @token_required
    def post(self, _):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No payload"}, status.HTTP_400_BAD_REQUEST

        tag_text = json_data["tag"]

        with Session() as session:
            tag = Tag(tag=tag_text, profile_id=self.id)
            session.add(tag)
            session.commit()
            return (
                TagSchema().dump(tag),
                status.HTTP_201_CREATED,
            )


class TagDetailsView(MethodView):
    @jwt_required()
    def get(self, tag_id):
        profile_id = get_jwt_identity()
     
        with Session() as session:
            tag = session.query(Tag).filter(Tag.profile_id == profile_id, Tag.id == tag_id).one_or_none()
            if tag:
                return TagSchema().dump(tag), status.HTTP_200_ACCEPTED
            return {'message': 'Tag not found'}, status.HTTP_404_NOT_FOUND

