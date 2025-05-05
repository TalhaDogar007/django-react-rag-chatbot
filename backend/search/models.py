from django.db import models
from .utils import load_and_split_pdf, index_documents

class PDF(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the file first
        docs = load_and_split_pdf(self.file.path)  # Extract text from the PDF
        index_documents(str(self.id), docs)  # Index the text into ChromaDB

    def __str__(self):
        return self.file.name
