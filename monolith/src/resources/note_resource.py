from flask_restx import Blueprint, Resource

bp = Blueprint("note", description="Endpoint focused in the users notes")

@bp.route("/<id:note_id>")
class UserNotes(Resource):
    @bp.doc("Getting a note based on the id of the note")
    def get(self) -> None:
        pass




