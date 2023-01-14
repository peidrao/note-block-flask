from src.services.hello import HelloWorld
# from services.authentication import ProfileLoginView, ProfileSignupView
# from services.profile import ProfileMeView, ProfileListView, ProfileDetailsView
# from services.note import NoteListView, ProfileMeNotes


def register_endpoints(app):
    app.add_url_rule('/', view_func=HelloWorld.as_view(name='helloworld'))

    # app.add_url_rule('/signup', view_func=ProfileSignupView.as_view(name='signup'))
    # app.add_url_rule('/login', view_func=ProfileLoginView.as_view(name='login'))

    # app.add_url_rule('/me', view_func=ProfileMeView.as_view(name='profile_me'))
    # app.add_url_rule('/profile', view_func=ProfileListView.as_view(
    # name='profile_list'))
    # app.add_url_rule('/profile/<int:profile_id>',
    # view_func=ProfileDetailsView.as_view(name='profile_details'))

    # app.add_url_rule('/notes', view_func=NoteListView.as_view(name='notes_list'))
    # app.add_url_rule('/me/notes', view_func=ProfileMeNotes.as_view(name='notes_me'))
