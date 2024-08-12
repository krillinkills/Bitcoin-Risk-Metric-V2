import re


def handle_near_x(query):
    # Regular expression to match the NEAR/x pattern
    near_pattern = re.compile(r'(\w+|"[^"]*")\s+NEAR/(\d+)\s+(\w+|"[^"]*")')

    # Search for the NEAR/x pattern in the query
    match = near_pattern.search(query)
    if match:
        term1, distance, term2 = match.groups()
        term1 = term1.strip('"')
        term2 = term2.strip('"')

        # Construct the regex pattern
        pattern = r"\b{}\b(?:\W+\w+){{0,{}}}\W+\b{}\b".format(
            term1, int(distance) - 1, term2
        )

        # Replace the NEAR/x pattern with the constructed regex pattern
        query = near_pattern.sub(pattern, query)

    return query


# Example query
query = """blue NEAR/3 green"""

# Handle the NEAR/x operator in the query
regex_pattern = handle_near_x(query)

print(f"Generated regex pattern: {regex_pattern}")

# Sample data (rows)
rows = [
    "I love blue and green.",
    "Blue and green are my favorite colors.",
    "Taste is subjective, but I prefer blue over green.",
    "Mentioning @doveuk here, and #blue for hashtags.",
]

# Apply regex to rows
for row in rows:
    if re.search(
        regex_pattern, row, re.IGNORECASE
    ):  # Added re.IGNORECASE for case-insensitive matching
        print(f"Match found: {row}")
    else:
        print(f"No match: {row}")
