def pre_process(sentence):
    '''
    The stop words have different uses depending on the input sentence.
    please consider that and un-comment the relevant function in the final part
    '''
    import os
    from docx import Document
    import re
    import pandas as pd
    def open_file(file_path):
        file_name, file_ext = os.path.splitext(file_path)

        if file_ext == '.doc' or file_ext == '.docx':
            document = Document(file_path)
            full_text = "\n".join([paragraph.text for paragraph in document.paragraphs])
            return full_text
        elif file_ext == '.csv':
            df = pd.read_csv(file_path, delimiter='\t', on_bad_lines='skip',encoding="utf-8", quoting=1)
            return df
        elif file_ext == '.dat':
            df = pd.read_csv(file_path,delimiter='\t', header=None)
            return df
        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                data = file.read()
                return data
        else:
            print(f"Unsupported file format for: {file_path}")
            return None
    stop_words=pd.read_csv(r'C:\Users\user\Downloads\stopwords.dat',delimiter='\t', header=None)
    indicies = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,20,23,31,33,46,49,68,72,77,90,102,109,388]
    final_stop_words = stop_words.loc[indicies]
    final_stop_words=final_stop_words.reset_index(drop=True)



    def remove_consecutive_duplicates1(text):
        result = ""
        previous_char = None

        for char in text:
            if char != previous_char:
                result += char
            previous_char = char

        return result


    def modify_sentence(sentence):
        words = sentence.split()
        if words[-1].endswith('ه'):
            words[-1] = words[-1][:-1] + ' ' + 'است'
        modified_sentence = ' '.join(words)
        return modified_sentence
    def remove_stop_words_sent(sentence):
        stop_words = final_stop_words
        words = sentence.split()
        filtered_words = [word for word in words if word not in stop_words]
        return ' '.join(filtered_words)
    
    def remove_stop_words_csv(comment_column):
        stop_words = final_stop_words  # Load your stop words file
        words = comment_column.str.split()
        words = words.apply(lambda word_list: [word for word in word_list if word not in stop_words.iloc[:, 0].tolist()])
        return words.apply(lambda word_list: ' '.join(word_list))
    
    def fix_half_space(text):
        half_space = "\u200C"
        normal_space = " "

        fixed_text = text.replace(half_space, normal_space)
        return fixed_text

    def clean_iranian_sentences(sentence):
    # Remove punctuation marks and replace them with a space
        sentence = re.sub(r'[،.,!?؟]', ' ', sentence)
    
    # Remove standalone digits
        sentence = re.sub(r'\b\d+\b', ' ', sentence)

    # Split the sentence into words
        words = sentence.split()

    # Remove trailing punctuation from each word
        cleaned_words = [re.sub(r'[،.,!?؟]$', '', word) for word in words]

    # Join the cleaned words into a sentence
        cleaned_sentence = ' '.join(cleaned_words)

        return cleaned_sentence


    cleaned_sentence = clean_iranian_sentences(sentence)
    modified_sentence = modify_sentence(cleaned_sentence)
    fixed_sentence = fix_half_space(modified_sentence)
    #stop_words_removed=remove_stop_words_csv(fixed_sentence)
    #stop_words_removed = remove_stop_words_sentence(fixed_sentence)
    deduplicated_comment = remove_consecutive_duplicates1(fixed_sentence)

    return deduplicated_comment

