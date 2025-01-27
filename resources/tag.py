from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import TagModel, StoreModel
from schemas import TagSchema

blp = Blueprint('tags', __name__, description='Operations on tags')

@blp.route('/store/<string:store_id>/tag')
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Tag with the same name already exists.")
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message="An error occurred while creating the tag.")
    
        return tag

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        return TagModel.query.get_or_404(tag_id)  
