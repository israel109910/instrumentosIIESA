from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'  # Carpeta raíz en el bucket para archivos media (ajusta si usas otra)
    default_acl = None
    region_name = 'us-east-2'
