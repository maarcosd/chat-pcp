import json
from pathlib import Path
from typing import List

from chromadb import PersistentClient
from chromadb.config import Settings
from google.cloud import storage
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from ..config import (
    CHROMA_GCS_PATH,
    CHROMA_LOCAL_PATH,
    EMBEDDINGS_BUCKET_NAME,
    PROJECT_ROOT,
)


class TranscriptEmbedder:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        """
        Initialize the EmbeddingPersister.

        Args:
            chunk_size: Size of each text chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap

        # Initialize GCS client
        self._storage_client = storage.Client()
        self._bucket = self._storage_client.bucket(EMBEDDINGS_BUCKET_NAME)

        # Ensure local directory exists
        Path(CHROMA_LOCAL_PATH).mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        self._chroma_client = PersistentClient(
            path=CHROMA_LOCAL_PATH,
            settings=Settings(anonymized_telemetry=False),
        )

        # Initialize the text splitter
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,
        )

    def _sync_to_gcs(self):
        """Sync local ChromaDB files to GCS."""
        # Upload the entire chroma directory to GCS
        for local_path in Path(CHROMA_LOCAL_PATH).rglob("*"):
            if local_path.is_file():
                relative_path = local_path.relative_to(CHROMA_LOCAL_PATH)
                blob_path = f"chroma_db/{relative_path}"
                blob = self._bucket.blob(blob_path)
                blob.upload_from_filename(str(local_path))
        print(f"Synced ChromaDB files to {CHROMA_GCS_PATH}")

    def _create_document(self, episode, transcript_text: str) -> Document:
        """
        Create a Document with episode metadata.

        Args:
            episode: Episode object containing metadata
            transcript_text: The transcript text content

        Returns:
            Document with metadata
        """
        return Document(
            page_content=transcript_text,
            metadata={
                "title": episode["title"],
                "date": str(episode["pub_date"]),
                "guid": episode["guid"],
            },
        )

    def _chunk_document(self, document: Document) -> List[Document]:
        """
        Split a document into chunks while preserving metadata.

        Args:
            document: The document to split

        Returns:
            List of document chunks
        """
        chunks = self._text_splitter.split_documents([document])
        print(f"Created {len(chunks)} chunks from document")
        return chunks

    def _persist_to_store(self, chunks: List[Document]) -> Chroma:
        """
        Create and persist a Chroma vector store from document chunks.

        Args:
            chunks: List of document chunks

        Returns:
            The created vector store
        """
        # Initialize embeddings
        embeddings = OpenAIEmbeddings()

        # Create and persist the vector store
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            client=self._chroma_client,
            collection_name="transcripts",
        )

        print(f"Vector store created and persisted to {CHROMA_LOCAL_PATH}")

        # Sync to GCS
        self._sync_to_gcs()

        return vectorstore

    def process(self, episode, transcript_text: str) -> Chroma:
        """
        Process an episode's transcript and persist it to the vector store.

        Args:
            episode: Episode object containing metadata
            transcript_text: The transcript text content

        Returns:
            The created vector store
        """
        # Create document with metadata
        document = self._create_document(episode, transcript_text)

        # Chunk the document
        chunks = self._chunk_document(document)

        # Persist to vector store
        return self._persist_to_store(chunks)


if __name__ == "__main__":
    import os
    from pathlib import Path

    # Check for OpenAI API key and GCP credentials
    if "OPENAI_API_KEY" not in os.environ:
        print("Please set your OPENAI_API_KEY environment variable")
        exit(1)
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set your GOOGLE_APPLICATION_CREDENTIALS environment variable")
        exit(1)

    # Test transcript content
    test_transcript = (
        Path(PROJECT_ROOT)
        .joinpath(
            "data/episodes/transcripts/episode-080-breaking-cycles-reflection-transcript-converted.txt"
        )
        .read_text()
    )
    test_episode = json.loads(
        Path(PROJECT_ROOT)
        .joinpath("data/episodes/info/ep080-breaking-cycles-reflection-info.json")
        .read_text()
    )

    # Initialize embedder
    embedder = TranscriptEmbedder()

    # Process test data
    vectorstore = embedder.process(test_episode, test_transcript)
    print("Test processing completed successfully")
