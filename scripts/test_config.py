from src.commitsage.config import settings, PROJECT_ROOT


def main():
    print("CommitSage configuration test")
    print("-" * 40)

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Embedding model: {settings.embedding_model}")
    print(f"Chroma collection: {settings.chroma_collection_name}")
    print(f"Top K: {settings.top_k}")
    print(f"Rerank Top K: {settings.rerank_top_k}")

    print("-" * 40)
    print("Configuration loaded successfully!")


if __name__ == "__main__":
    main()

