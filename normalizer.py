def text_normalizer(user_input):
    def word_normalizer(word):
        valid_letters = set(chr(i) for i in range(97, 123)) | {"-", "'", "’"}
        return "".join(c for c in word.lower() if c in valid_letters)

    def word_storage(data):
        return [word_normalizer(word) for word in data.split()]
    
    def combination_of_words(input_list):
        new_list = input_list[:]
        for terms in range(2, 5):
            for i in range(len(input_list) - terms + 1):
                new_list.append(" ".join(input_list[i:i+terms]))
        return new_list
    
    return combination_of_words(word_storage(user_input))
