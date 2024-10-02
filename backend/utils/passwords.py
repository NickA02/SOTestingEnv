import polars as pl


"""
Dev Notes:
    Right now, the corpus is saved and edited in the 'unique_words.csv' file.
    In the future, this should probably be kept and maintained in the database 
    as its own, unrelated table.

    Therefore, these should not be considered ready to be deployed functions, 
    but rather code to use in the interim.
"""


def save_teams_from_csv(userTable, path: str) -> str:
    """Update User Table with new passwords and users"""
    newUserTable = generate_passwords(userTable)
    # TODO -- step to load new users into actual db
    newUserTable.write_csv(path)
    return True


def generate_passwords(userTable: pl.DataFrame) -> pl.DataFrame:
    userTable.replace_column(
        pl.when((pl.col("thing"))).then(pl.col).otherwise(generate_password())
    )


def generate_password() -> str:
    """Generates and returns a unique 3-word password"""
    corpus = pl.read_csv("unique_words.csv")["words"].shuffle().to_list()
    generated_pwd = f"{corpus.pop()}-{corpus.pop()}-{corpus.pop()}"
    pl.DataFrame({"names": corpus}).write_csv("unique_words.csv")
    return generated_pwd


def reset_word_list():
    """Resets memory of available password words"""
    pl.read_csv("unique_words_reset.csv").write_csv("unique_words.csv")
