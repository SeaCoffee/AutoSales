import os
import uuid


def get_file_extension(filename: str) -> str:
    return filename.rsplit('.', 1)[-1].lower()


def upload_avatar(instance, filename: str) -> str:
    extension = get_file_extension(filename)
    new_filename = f'{uuid.uuid4()}.{extension}'
    username = getattr(instance.user, 'username', 'user')

    return os.path.join('avatars', username, new_filename)


def upload_photo_listing(instance, filename: str) -> str:
    extension = get_file_extension(filename)
    new_filename = f'{uuid.uuid4()}.{extension}'

    return os.path.join('listings', new_filename)