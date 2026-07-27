import logging

from langchain_classic.retrievers import EnsembleRetriever
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_huggingface import HuggingFaceEmbeddings

from config.settings import settings

logger = logging.getLogger(__name__)


class RetrieverBuilder:
    def __init__(self):
        """Initialize the retriever builder with embeddings.

        Embeddings run locally via sentence-transformers, so no embedding API key
        is needed (the chat provider offers no embeddings endpoint). The model is
        downloaded once on first run and cached afterwards.
        """
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def build_hybrid_retriever(self, docs):
        """Build a hybrid retriever combining BM25 and vector search.

        BM25 catches exact keyword matches and vector search catches semantic
        ones, so blending them handles both precise terms and paraphrased
        questions.
        """
        try:
            # Vector store for semantic similarity
            vector_store = Chroma.from_documents(
                documents=docs,
                embedding=self.embeddings,
                persist_directory=settings.CHROMA_DB_PATH,
            )
            logger.info("Vector store created successfully.")

            # Keyword retriever
            bm25 = BM25Retriever.from_documents(docs)
            bm25.k = settings.VECTOR_SEARCH_K
            logger.info("BM25 retriever created successfully.")

            vector_retriever = vector_store.as_retriever(
                search_kwargs={"k": settings.VECTOR_SEARCH_K}
            )
            logger.info("Vector retriever created successfully.")

            # Weighted blend of the two (see HYBRID_RETRIEVER_WEIGHTS in settings)
            hybrid_retriever = EnsembleRetriever(
                retrievers=[bm25, vector_retriever],
                weights=settings.HYBRID_RETRIEVER_WEIGHTS,
            )
            logger.info("Hybrid retriever created successfully.")
            return hybrid_retriever
        except Exception as e:
            logger.error(f"Failed to build hybrid retriever: {e}")
            raise
