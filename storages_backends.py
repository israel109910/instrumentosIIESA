from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'   # o 'private' si quieres que no sean públicos
    file_overwrite = False
