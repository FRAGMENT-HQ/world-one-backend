from storages.backends.gcloud import GoogleCloudStorage
from google.cloud import storage
import dj_database_url
import os



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MediaStorage(GoogleCloudStorage):
    # authenticated users can read and write
    storage.Client.from_service_account_json(
        os.path.join(BASE_DIR, 'world-one.json'))

    location = 'media/'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False