import polars as pl


def generate_password() -> str:
    """Generate a unique 3-word password"""
    corpus = pl.read_csv("unique_words.txt")["words"].shuffle().to_list()
    generated_pwd = f"{corpus.pop()}-{corpus.pop()}-{corpus.pop()}"
    pl.DataFrame({"names": corpus}).write_csv("unique_words.txt")
    return generated_pwd
