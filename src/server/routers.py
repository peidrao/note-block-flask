from src.services.hello import HelloWorld
from src.services.authentication import (
    ProfileLoginView,
    ProfileSignupView,
    TokenRefresh,
)

from src.services.profile import (
    ProfileMeView,
    ProfileListView,
    ProfileDetailsView,
    ProfileUpdatePasswordView,
)
from src.services.note import (
    NoteDetailsView,
    NoteListView,
    NotesTrashView,
    ProfileMeNotes,
)
from src.services.tag import TagsListView, TagDetailsView


def register_endpoints(app):
    app.add_url_rule("/", view_func=HelloWorld.as_view(name="helloworld"))

    app.add_url_rule("/signup", view_func=ProfileSignupView.as_view(name="signup"))
    app.add_url_rule("/login", view_func=ProfileLoginView.as_view(name="login"))
    app.add_url_rule("/refresh", view_func=TokenRefresh.as_view(name="refresh"))

    app.add_url_rule("/me", view_func=ProfileMeView.as_view(name="profile_me"))
    app.add_url_rule("/profile", view_func=ProfileListView.as_view(name="profile_list"))
    app.add_url_rule(
        "/profile/update_password",
        view_func=ProfileUpdatePasswordView.as_view(name="profile_update_password"),
    )

    app.add_url_rule(
        "/profile/<int:profile_id>",
        view_func=ProfileDetailsView.as_view(name="profile_details"),
    )

    app.add_url_rule("/notes", view_func=NoteListView.as_view(name="notes_list"))
    app.add_url_rule("/me/notes", view_func=ProfileMeNotes.as_view(name="notes_me"))
    app.add_url_rule("/tags", view_func=TagsListView.as_view(name="tags_list"))
    app.add_url_rule("/tag/<int:tag_id>", view_func=TagDetailsView.as_view(name="tags_detail"))

    app.add_url_rule(
        "/notes/<int:note_id>", view_func=NoteDetailsView.as_view(name="notes_detail")
    )

    app.add_url_rule(
        "/notes/trash/", view_func=NotesTrashView.as_view(name="note_trash")
    )
