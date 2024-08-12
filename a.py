from nltk import word_tokenize
import re


def convert_to_python_operators(query):
    """
    Takes the query with symbol operators and replace with python equivalent
    so can be evaluated by eval() function
    :param query: The input query
    :return query: The query with operators replaced with Python operators (and, not, or) so that Python can evaluate
     the query
    """
    query = re.sub(r"\!\!", "not", query, flags=re.UNICODE)
    query = re.sub(r"\&\&", "and", query, flags=re.UNICODE)
    query = re.sub(r"\|\|", "or", query, flags=re.UNICODE)

    return query


quoted_word_pattern = re.compile('"(.*?)"', flags=re.UNICODE)
question_mark_pattern = re.compile(r"\w+?\.[a-z]*", flags=re.UNICODE)


def parse_near(parsed_query, input_text):
    """
    Takes a NEAR statement, evaluates it and returns the full query with the parsed NEAR statement.
    :param parsed_query: The query associated with a topic
    :param input_text: The input text
    :return parsed_query: The output query once it has been parsed with the NEAR operator
    """
    parsed_query = parsed_query.lower()
    parsed_query = parsed_query.replace("?", ".")

    # Find all the near statements in the query
    # \(?([^\)\(]*?)\)?(?:\s)((?:near\/)([0-9]+))(?:\s)\(?(.*?)\)  (\(\(?(.*?)\)?(?:\s)((?:near\/)([0-9]+))(?:\s)\(?(.*?)\)?\))
    near_strings = re.findall(
        r"(\(?([^\)\(]*?)\)?(?:\s)((?:near\/)([0-9]+))(?:\s)\(?(.*?)\))",
        parsed_query,
        flags=re.UNICODE,
    )

    for nstring in near_strings:
        # Strip whitespace
        words = [word.strip() for word in nstring]

        # Get the number after NEAR/ in the query
        sepdist = words[3]

        # Get the words in the LHS of the query
        lhs = words[1]

        # Get the words in the RHS of the query
        rhs = words[4]

        keywords = ["(", ")", "||", "&&", "!!"]

        # Find quoted phrases
        quoted_left = quoted_word_pattern.findall(lhs)
        quoted_right = quoted_word_pattern.findall(rhs)
        n_quoted_left = []
        for w in quoted_left:
            n_quoted_left.append('"' + w + '"')
        quoted_left = n_quoted_left
        n_quoted_right = []
        for w in quoted_right:
            n_quoted_right.append('"' + w + '"')
        quoted_right = n_quoted_right
        # Extract words to match with input text before and after near and append quoted phrases
        words_left = [
            w
            for w in word_tokenize(re.sub('"(.*?)"', "", lhs, flags=re.UNICODE))
            if w.lower() not in keywords
        ] + quoted_left
        words_right = [
            w
            for w in re.sub('"(.*?)"', "", rhs, flags=re.UNICODE).split()
            if w not in keywords
        ] + quoted_right

        # We sort them so quoted words come first to prevent issue where words inside quoted words aren't replaced
        words_left = sorted(words_left)
        words_right = sorted(words_right)

        words_near = []

        # Appending regex symbol /w to match any word character(s) before the next space
        for a in words_left:
            for b in words_right:
                if a[-1:] == "*":
                    match_a = re.escape(re.sub(r"\*", "", a, flags=re.UNICODE)) + r"\w*"
                else:
                    question_mark = question_mark_pattern.findall(a)

                    if a in question_mark:
                        match_a = a
                    else:
                        match_a = re.escape(a)

                if b[-1:] == "*":
                    match_b = re.escape(re.sub(r"\*", "", b, flags=re.UNICODE)) + r"\w*"
                else:
                    question_mark = question_mark_pattern.findall(b)

                    if b in question_mark:
                        match_b = b
                    else:
                        match_b = re.escape(b)

                match_a_nq = match_a.strip('"')
                match_b_nq = match_b.strip('"')

                # Check distance between each pair of words on each side of NEAR is less than required
                m = re.search(
                    r"\b(?:"
                    + match_a_nq
                    + r"\W+(?:\w+\W+){0,"
                    + re.escape(sepdist)
                    + r"}?"
                    + match_b_nq
                    + r"|"
                    + match_b_nq
                    + r"\W+(?:\w+\W+){0,"
                    + re.escape(sepdist)
                    + r"}?"
                    + match_a_nq
                    + r")\b",
                    input_text,
                    flags=re.UNICODE,
                )

                if m:
                    x = True

                else:
                    x = False

                words_near.append((a, b, x))

        eval_left = lhs.lower()

        # for each word in query on lhs, check it satisfies condition on rhs
        for word_left in words_left:

            match_dict = {wn[1]: wn[2] for wn in words_near if wn[0] == word_left}

            eval_right = rhs

            for key, value in match_dict.items():
                if key[0] == '"':
                    # We match direct on key as we add in the quotes in quoted_right
                    eval_right = re.sub(key, str(value), eval_right, flags=re.UNICODE)
                else:
                    eval_right = re.sub(
                        r"\b" + key + r"\b", str(value), eval_right, flags=re.UNICODE
                    )

            # Replace asterisks so that each side can be evaluated
            eval_left = re.sub(r"\*", "", eval_left, flags=re.UNICODE)
            eval_right = re.sub(r"\*", "", eval_right, flags=re.UNICODE)
            eval_left = convert_to_python_operators(eval_left)
            eval_right = convert_to_python_operators(eval_right)
            eval_right = eval_right.replace('"', "")

            if word_left[0] == '"':
                # We match direct on key as we add in the quotes in quoted_left
                eval_left = re.sub(
                    word_left, str(eval(eval_right)), eval_left, flags=re.UNICODE
                )
            else:
                eval_left = re.sub(
                    r"\b" + word_left + r"\b",
                    str(eval(eval_right)),
                    eval_left,
                    flags=re.UNICODE,
                )

        eval_left = eval_left.replace('"', "")

        final_eval = eval(eval_left)

        parsed_query = parsed_query.replace(nstring[0], str(final_eval))

    return parsed_query


parsed_query = "(apple NEAR/2 orange)"
input_text = "I ate an apple and an orange yesterday."

result = parse_near(parsed_query, input_text)
print(result)
