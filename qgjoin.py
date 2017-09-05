from collections import defaultdict

encoding_table = {
                    # Punctuation
                    ' ': 28, '-': 28, '_': 28,

                    # Numbers
                    '0': ord("O") - ord('@'), '1': ord("I") - ord('@'),
                    '2': ord("Z") - ord('@'), '3': 27,
                    '4': ord("A") - ord('@'), '5': ord("S") - ord('@'),
                    '6': ord("G") - ord('@'), '7': ord("T") - ord('@'),
                    '8': ord("B") - ord('@'), '9': ord("Q") - ord('@'),

                    # Letters
                    'a': ord("A") - ord('@'), 'A': ord("A") - ord('@'),
                    'b': ord("B") - ord('@'), 'B': ord("B") - ord('@'),
                    'c': ord("C") - ord('@'), 'C': ord("C") - ord('@'),
                    'd': ord("D") - ord('@'), 'D': ord("D") - ord('@'),
                    'e': ord("E") - ord('@'), 'E': ord("E") - ord('@'),
                    'f': ord("F") - ord('@'), 'F': ord("F") - ord('@'),
                    'g': ord("G") - ord('@'), 'G': ord("G") - ord('@'),
                    'h': ord("H") - ord('@'), 'H': ord("H") - ord('@'),
                    'i': ord("I") - ord('@'), 'I': ord("I") - ord('@'),
                    'j': ord("J") - ord('@'), 'J': ord("J") - ord('@'),
                    'k': ord("K") - ord('@'), 'K': ord("K") - ord('@'),
                    'l': ord("L") - ord('@'), 'L': ord("L") - ord('@'),
                    'm': ord("M") - ord('@'), 'M': ord("M") - ord('@'),
                    'n': ord("N") - ord('@'), 'N': ord("N") - ord('@'),
                    'o': ord("O") - ord('@'), 'O': ord("O") - ord('@'),
                    'p': ord("P") - ord('@'), 'P': ord("P") - ord('@'),
                    'q': ord("Q") - ord('@'), 'Q': ord("Q") - ord('@'),
                    'r': ord("R") - ord('@'), 'R': ord("R") - ord('@'),
                    's': ord("S") - ord('@'), 'S': ord("S") - ord('@'),
                    't': ord("T") - ord('@'), 'T': ord("T") - ord('@'),
                    'u': ord("U") - ord('@'), 'U': ord("U") - ord('@'),
                    'v': ord("V") - ord('@'), 'V': ord("V") - ord('@'),
                    'w': ord("W") - ord('@'), 'W': ord("W") - ord('@'),
                    'x': ord("X") - ord('@'), 'X': ord("X") - ord('@'),
                    'y': ord("Y") - ord('@'), 'Y': ord("Y") - ord('@'),
                    'z': ord("Z") - ord('@'), 'Z': ord("Z") - ord('@'),
                  }


def encode_qgram(q_gram):
    """Encodes the given qgram to 5-bit ASCII characters as a tuple

    :param q_gram: string to encode
    :return: tuple of converted qgram characters as int
    """
    return (encoding_table[c] for c in q_gram.upper())


def get_qgrams(t, q_size):
    """Extract Qgrams of length q_size from string t.

    :param t: string to extract qgrams from
    :param q_size: int defining size of qgrams
    :return: tuple of qgrams extracted from t
    """
    if len(t) < q_size:
        return ()
    elif len(t) == q_size:
        return encode_qgram(t)
    else:
        return (encode_qgram(t[i:i+5]) for i in range(len(t) - q_size))


def assign_weight(w, qgram, S):
    """Assign the weight calculated from given w to Index of string in S to
    which given QGram qgram belongs to.

    w is the power of 2, which we use as the weight. While not necessary for this
    rudimentary implementation, it allows developers to save the position of the
    qgram in string t (since weight = 2 to the power of index of qgram).

    :param w: index of qgram in string t
    :param qgram: qgram to add weight for
    :param S: Hashmap of qgrams of Strings to look up qgram in.
    :return: dict of weights for qgram with index:weight pairs
    """
    weight = 2 ** w
    return {i: weight for i in S[qgram]}


def merge_weights(*dicts):
    """Merge weights of given dicts and combine them into single dict.

    :param dicts: dicts as output by assign_weight()
    :return: dict of index:weight pairs
    """
    I = defaultdict(int)
    for d in dicts:
        for k in d:
            I[k] += d[k]
    return I


def convert_to_bitstreak_dict(d):
    """Convert dict of index:weight pairs to index:bitstreak pairs.

    :param d: dict as output by merge_weights()
    :return: dict of index:bitstreak pairs
    """
    return {k: bin(v).count("1") for k, v in d.items()}


def max_streak_indices(d):
    """Returns a tuple of all indices with the biggest bit streak in given dict.

    :param d: dict as output by convert_to_bitstreak_dict(d)
    :return: tuple of indices with biggest bitstreak
    """
    max_streak = max(d.values())
    return max_streak, (k for k in d if d[k] == max_streak)


def compare_t(t, Qgrams_of_S, q_size=5):
    """Compare string t against Qgrams of S and return the indices of strings
    which match best.

    :param t: string of minimum length 5
    :param Qgrams_of_S: dict of qgrams of all strings to compare t against
    :param q_size: int defining length of a single qgram
    :return: maximum streak length, tuple of indices of strings matching t
    """
    if len(t) < q_size:
        return None, ()
    qgrams = get_qgrams(t, q_size)
    weights = merge_weights(assign_weight(w, qgram, Qgrams_of_S)
                            for w, qgram in enumerate(qgrams))
    bitstreaks = convert_to_bitstreak_dict(weights)
    max_streak, matches = max_streak_indices(bitstreaks)
    return max_streak, matches


def generate_qgrams_of_strings(S, q_size):
    """Generate a dict of qgrams of all strings in S with size q_size, whose
    values are the indices of the string each Qgram belongs to.
    
    :param S: array of strings
    :param q_size: int defining length of qgrams
    :return: dict of qgram:list_of_related_string_indices
    """
    Q_of_S = defaultdict(tuple)
    for i, s in enumerate(S):
        for qgram in get_qgrams(s, q_size):
            Q_of_S[qgram] += (i,)
    return Q_of_S


def qgjoin(left, right, q_size):
    """Fuzzy join left data with right data using qgrams of size q_size.

    :param left: str, file path to smaller list
    :param right: str, file path to bigger list
    :param q_size: int defining size of qgram length
    :return: None
    """
    f = open(left, 'r')
    left_strings = (l.strip('\n') for l in  f.readlines())
    f.close()
    qgrams_of_left_strings = generate_qgrams_of_strings(left_strings, q_size)

    with open(right, 'r') as f:
        for line in f:
            t = line.strip('\n')
            streak_length, matches = compare_t(t, qgrams_of_left_strings, q_size)
            for index_of_match in matches:
                print("%s\t%s\t%s\n" % (t, left_strings[index_of_match], streak_length))



