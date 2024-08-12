import re


def handle_or(query):
    return query.replace(" OR ", "|")


def handle_and(query):
    return query.replace(" AND ", ".*")


def handle_not(query):
    return re.sub(r"NOT\s+(\w+)", r"^(?!.*\b\1\b)", query)


def handle_exact_phrases(query):
    return re.sub(r'"(.*?)"', lambda m: r"\b" + re.escape(m.group(1)) + r"\b", query)


def handle_wildcards(query):
    return re.sub(r"(\w+)\*", r"\\b\1\\w*\\b", query)


def handle_question_marks(query):
    return re.sub(r"(\w+)\?", lambda m: f"{m.group(1)}.", query)


def handle_mentions(query):
    return re.sub(r"at_mention:\((.*?)\)", r"@\b\1\b", query)


def handle_hashtags(query):
    return re.sub(r"hashtag:\((.*?)\)", r"#\b\1\b", query)


# Example query
query = """((protect* OR care OR caring OR safe* OR shield* OR defend* OR guard* OR defens*) NEAR/3 (#sun OR UV OR UVA OR UVB OR solar)) OR "anti-sun" OR "anti sun" """


query = handle_or(query)
query = handle_and(query)
query = handle_not(query)
query = handle_exact_phrases(query)
query = handle_wildcards(query)
query = handle_question_marks(query)
query = handle_mentions(query)

print(query)
