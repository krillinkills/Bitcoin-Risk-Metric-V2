import re

# Sample data (rows)
rows = [
    "I love chocolate and vanilla ice cream Beauty Balm.",
    "Blue and green are my favorite colors.",
    "Taste is subjective, but I prefer optimize over optimise.",
    "Mentioning @doveuk here, and #blue for hashtags.",
]

# Example query
query = """((BB OR "Beauty Balm" OR "Blemish Balm" OR "beauty-balm" OR "blemish-balm" NOT blue) NEAR/2 (cream OR creams)) AND Nice"""


def handle_or(query):
    return query.replace(" OR ", "|")


def handle_and(query):
    return query.replace(" AND ", ".*")


def handle_not(query):
    return re.sub(r"NOT\s+(\w+)", r"^(?!.*\b\1\b)", query)


def handle_exact_phrases(query):
    # Replace exact phrases inside double quotes with regex pattern
    return re.sub(r'"(.*?)"', lambda m: r"\b" + re.escape(m.group(1)) + r"\b", query)


def handle_near_x(query):
    near_pattern = re.compile(r'(\w+|"[^"]*")\s+NEAR/(\d+)\s+(\w+|"[^"]*")')
    while near_pattern.search(query):
        match = near_pattern.search(query)
        term1, distance, term2 = match.groups()
        term1 = term1.strip('"')
        term2 = term2.strip('"')
        pattern = r"\b{}\b(?:\W+\w+){{0,{}}}\W+\b{}\b".format(
            term1, int(distance), term2
        )
        query = near_pattern.sub(pattern, query, 1)
    return query


def handle_wildcards(query):
    return re.sub(r"(\w+)\*", r"\1.*", query)


def handle_question_marks(query):
    return re.sub(r"(\w+)\?", lambda m: f"{m.group(1)}.", query)


def handle_mentions(query):
    return re.sub(r"at_mention:\((.*?)\)", r"@\b\1\b", query)


def handle_hashtags(query):
    return re.sub(r"hashtag:\((.*?)\)", r"#\b\1\b", query)


def process_inner_parentheses(query):
    # Process innermost parentheses first
    def replace_match(m):
        inner = m.group(1)
        return f"(?:{process_query(inner)})"

    return re.sub(r"\(([^()]+)\)", replace_match, query)


def handle_parentheses(query):
    # Recursively handle parentheses
    previous_query = None
    while previous_query != query:
        previous_query = query
        query = process_inner_parentheses(query)
        # Handle cases where there may be nested parentheses
        query = re.sub(
            r"\(([^()]*\([^()]*\)[^()]*)\)",
            lambda m: f"(?:{process_query(m.group(1))})",
            query,
        )
    return query


def process_query(query):
    query = handle_or(query)
    query = handle_and(query)
    query = handle_not(query)
    query = handle_exact_phrases(query)
    query = handle_parentheses(query)
    query = handle_near_x(query)
    query = handle_wildcards(query)
    query = handle_question_marks(query)
    query = handle_mentions(query)
    query = handle_hashtags(query)
    return query


query = handle_or(query)
query = handle_and(query)
query = handle_not(query)
query = handle_exact_phrases(query)
print(query)
