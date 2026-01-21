import os

from django.core.management.base import BaseCommand, CommandError

from azure.storage.blob import BlobServiceClient

from main.models import GalleryImage

class Command(BaseCommand):
    help = "Seed the database from a blob store list of URLs."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Do not write changes to the database.",
        )

    def handle(self, *args, **options):
        blob_path = "https://isobelcalumwedding.blob.core.windows.net/"
        dry_run: bool = options["dry_run"]

        self.stdout.write(self.style.NOTICE(f"Starting seed_from_blob (blob_path={blob_path!r}, dry_run={dry_run})"))

        # Connect to Azure Storage Account Blob Store Container and list all file urls
        # TODO: GET THIS FROM ENV SHHH ITS A SECRET
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_name = "images"
        container_client = blob_service_client.get_container_client(container=container_name)

        # List all blobs in the container
        self.stdout.write(self.style.NOTICE(f"Getting Blobs"))
        blob_list = container_client.list_blobs()
        file_urls = [
            f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob.name}"
            for blob in blob_list
        ]

        if dry_run:
            #print all file urls
            for url in file_urls:
                self.stdout.write(f"Found blob URL: {url}")
        else: 
            # delete all records in GalleryImage
            self.stdout.write(self.style.NOTICE(f"Deleting existing GalleryImage entries."))
            GalleryImage.objects.all().delete()


            # bulk save all urls as a GalleryImage in django db
            gallery_images = [GalleryImage(link=url, description="") for url in file_urls]
            self.stdout.write(self.style.NOTICE(f"Creating GalleryImage entries from blob store."))
            GalleryImage.objects.bulk_create(gallery_images, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f"Seeded {len(gallery_images)} GalleryImage entries from blob store."))

