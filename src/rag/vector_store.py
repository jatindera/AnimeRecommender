"""
VectorStoreBuilder — builds and loads a Chroma vector database for RAG.

Key features:
- Uses OpenAIEmbeddings ('text-embedding-3-large') or HuggingFace transformer
- Accepts config from Settings (paths, collection name, etc.)
- Structured logging and clear error handling
- Uses CharacterTextSplitter for chunking
"""

import os
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config.settings import Settings
from utils.logger import setup_logger

# Load environment variables early
load_dotenv()

logger = setup_logger(__name__, level=logging.INFO)
settings = Settings()


class VectorStoreBuilder:
    """Handles creating and loading a Chroma vector store from processed CSV data."""

    def __init__(self, processed_csv: str, settings: Settings = settings):
        """
        Args:
            processed_csv: Path to processed CSV file.
            settings: Global Settings instance.
        """
        self.processed_csv = processed_csv
        self.settings = settings
        self.persist_directory = settings.CHROMA_DIR
        self.collection_name = settings.CHROMA_COLLECTION

        # ✅ Use correct argument (Pydantic v2 + LangChain 1.0 compatible)
        self.embedding = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL  # <— previously model_name
        )

    # -----------------------------------------------------
    # 🧠 Create vector store from CSV
    # -----------------------------------------------------
    def create_vector_store(self) -> Chroma:
        """Load CSV, split into chunks, embed, and persist to Chroma."""
        try:
            if not os.path.exists(self.processed_csv):
                raise FileNotFoundError(f"CSV file not found: {self.processed_csv}")

            logger.info(f"📄 Loading CSV from {self.processed_csv}...")
            loader = CSVLoader(
                file_path=self.processed_csv,
                encoding="utf-8",
                metadata_columns=[],
            )
            documents = loader.load()
            logger.info(f"✅ Loaded {len(documents)} documents.")

            # Split into overlapping chunks
            logger.info("✂️ Splitting documents (chunk_size=1000, overlap=200)...")
            splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(documents)
            logger.info(f"✅ Created {len(chunks)} text chunks.")

            # Create and persist Chroma DB
            logger.info("🧠 Creating Chroma vector store...")
            vector_store = Chroma.from_documents(
                collection_name=self.collection_name,
                documents=chunks,
                embedding=self.embedding,
                persist_directory=self.persist_directory,
            )
            logger.info(
                f"✅ Vector store created and persisted at '{self.persist_directory}' "
                f"(collection: {self.collection_name})"
            )

            return vector_store

        except Exception as e:
            logger.exception(f"❌ Vector store build failed: {e}")
            raise

    # -----------------------------------------------------
    # 📦 Load existing vector store
    # -----------------------------------------------------
    def load_vector_store(self) -> Chroma:
        """Load an existing persisted Chroma vector store."""
        try:
            if not os.path.exists(self.persist_directory):
                raise FileNotFoundError(
                    f"No Chroma DB found at {self.persist_directory}. Run build first."
                )

            logger.info(
                f"📦 Loading existing Chroma vector store from '{self.persist_directory}'..."
            )
            vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embedding,
                persist_directory=self.persist_directory,
            )
            logger.info("✅ Chroma vector store loaded successfully.")
            return vector_store

        except Exception as e:
            logger.exception(f"❌ Failed to load vector store: {e}")
            raise
