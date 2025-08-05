import os
from collections import Counter

stop_words = {"the", "and", "or", "is", "in", "to", "a", "of", "for", "on", "with", "as", "at", "by", "an"}


def process_file(file_path, case_sensitive=False):
    if not os.path.exists(file_path):
        print(f"Error: '{file_path}' not found.")
        return


    wc = 0  
    cws = 0 
    cwo = 0 
    lc = 0 
    pc = 0 
    words = []
    sentences = 0
    longest = ""
    shortest = None

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

  
    paragraphs = text.split('\n\n')
    pc = len(paragraphs)
    lines = text.splitlines()
    lc = len(lines)


    for line in lines:
        line_words = line.split()
        wc += len(line_words)
        cws += sum(len(word) for word in line_words)
        cwo += sum(len(word.replace(" ", "")) for word in line_words)

        for word in line_words:
            word = word if case_sensitive else word.lower()
            words.append(word)
            if len(word) > len(longest): longest = word
            if shortest is None or len(word) < len(shortest): shortest = word
        sentences += line.count('.') + line.count('!') + line.count('?')


    unique_words = set(words)
    vocab_size = len(unique_words)
    word_freq = Counter(words)
    most_common = word_freq.most_common(10)


    avg_words_per_sentence = wc / sentences if sentences else 0
    avg_chars_per_word = cwo / wc if wc else 0
    reading_time = wc / 200 

    print("\n--- Word Count Analysis ---")
    print(f"Words: {wc}, Characters (with spaces): {cws}, Characters (without spaces): {cwo}")
    print(f"Lines: {lc}, Paragraphs: {pc}, Vocabulary size: {vocab_size}")
    print(f"Longest word: {longest}, Shortest word: {shortest}")
    print(f"Avg words per sentence: {avg_words_per_sentence:.2f}")
    print(f"Avg characters per word: {avg_chars_per_word:.2f}")
    print(f"Estimated reading time: {reading_time:.2f} minutes")
    print("\nTop 10 most frequent words:")
    for word, freq in most_common:
        if word not in stop_words:
            print(f"{word}: {freq}")

    with open(f"{file_path}_summary.txt", 'w', encoding='utf-8') as summary_file:
        summary_file.write(f"Word Count Analysis for {file_path}\n")
        summary_file.write(f"Words: {wc}\nCharacters (with spaces): {cws}\n")
        summary_file.write(f"Characters (without spaces): {cwo}\nLines: {lc}\n")
        summary_file.write(f"Paragraphs: {pc}\nVocabulary size: {vocab_size}\n")
        summary_file.write(f"Longest word: {longest}\nShortest word: {shortest}\n")
        summary_file.write(f"Avg words per sentence: {avg_words_per_sentence:.2f}\n")
        summary_file.write(f"Avg characters per word: {avg_chars_per_word:.2f}\n")
        summary_file.write(f"Estimated reading time: {reading_time:.2f} minutes\n")
        summary_file.write("\nTop 10 most frequent words:\n")
        for word, freq in most_common:
            if word not in stop_words:
                summary_file.write(f"{word}: {freq}\n")

    print(f"\nSummary saved to: {file_path}_summary.txt")


def main():
    file_path = input("enter file path : ").strip()
    case_sensitive = input("Case-sensitive counting? (yes/no): ").strip().lower() == 'yes'
    process_file(file_path, case_sensitive)


if __name__ == "__main__":

    main()
