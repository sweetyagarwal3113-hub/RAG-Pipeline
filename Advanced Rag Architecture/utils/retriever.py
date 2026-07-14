from langchain_classic.retrievers import EnsembleRetriever, MultiQueryRetriever, ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import FlashrankRerank
from langchain.chains.query_constructor.base import AttributeInfo
import logging

logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

def create_advanced_retriever(llm, parent_retriever, bm25_retriever):
    # 1. HYBRID SEARCH: Combine Dense (ParentDocument) and Sparse (BM25)
    # Weights prioritize semantic search slightly over keyword search
    ensemble_retriever = EnsembleRetriever(
        retrievers=[parent_retriever, bm25_retriever],
        weights=[0.6, 0.4]
    )

    # 2. MULTI-QUERY: Wrap the Hybrid Search in a Multi-Query Retriever
    # This uses the LLM to generate multiple variations of the user's question
    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=ensemble_retriever,
        llm=llm
    )

    # 3. RE-RANKING: Compress/Re-rank the final results
    # We use FlashRank (a fast, lightweight local Cross-Encoder)
    compressor = FlashrankRerank(top_n=3)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=multi_query_retriever
    )

    return compression_retriever
