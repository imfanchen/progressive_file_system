def get_substring_slow(passage: str, scores: list[float], threshold=0.5) -> str:
    """
    O(n^2) version: finds the max contiguous substring with scores >= threshold.
    """
    words = passage.split(" ")

    global_max = 0
    start_index = 0
    end_index = 0

    for i, score in enumerate(scores):
        if score >= threshold:
            j = i + 1
            current_sum = score
            while j < len(scores) and scores[j] >= threshold:
                current_sum += scores[j]
                j += 1
            if current_sum > global_max:
                global_max = current_sum
                start_index = i
                end_index = j
    substring = " ".join(words[start_index:end_index])
    return substring


def get_substring_fast(passage: str, scores: list[float], threshold=0.5) -> str:
    """
    O(n) version: finds the max contiguous substring with scores >= threshold.
    """
    words = passage.split(" ")
    global_max = 0
    start_index = 0
    end_index = 0
    current_sum = 0
    current_start = None
    for i, score in enumerate(scores):
        if score >= threshold:
            if current_start is None:
                current_start = i
            current_sum += score
        else:
            if current_sum > global_max:
                global_max = current_sum
                start_index = current_start
                end_index = i
            current_sum = 0
            current_start = None
    # Check if the last segment is the maximum
    if current_sum > global_max:
        global_max = current_sum
        start_index = current_start
        end_index = len(scores)
    substring = " ".join(words[start_index:end_index])
    return substring


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Find max relevant substring.")
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    passage = "if it does. Ultimately, tests will help ensure that people can get back to work and will help reestablish public confidence in various sectors."
    scores = [0.09, 0.01, 0.0, 0.9, 1.0, 0.4, 0.2, 0.6, 0.7, 0.9, 0.8, 0.9, 0.8, 0.7, 0.6, 0.02, 0.1, 0.01, 0.5, 0.2, 0.3, 0.0, 0.01, 0.00]

    if args.debug:
        words = passage.split(" ")
        for i, (w, s) in enumerate(zip(words, scores)):
            print(i, w, s)
    # print(get_substring_slow(passage, scores))
    print(get_substring_fast(passage, scores))