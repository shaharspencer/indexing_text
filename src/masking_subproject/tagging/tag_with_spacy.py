"""
This file converts the conllu formatted data to the following format:
John NOUN
loves VERB
Mary NOUN

Bobby NOUN
likes VERB
to PRP
run VERB

with spaCy tags
"""


import spacy
from conllu import parse
from docopt import docopt

usage = '''
word_pos_converter CLI.
number of 
Usage:
    word_pos_converter.py <file_to_proccess> <n_sentences>
'''

def convert_conllu_to_tagged_text(conllu_content, output_file,
                                  sentence_limit):
    with open(output_file, 'w', encoding='utf-8') as f:
        sentence_count = 0
        for sentence in conllu_content:
            sentence_text = " ".join([token_info['form'] for token_info in sentence])
            doc = nlp(sentence_text)

            for token in doc:
                f.write(f"{token.text} {token.pos_}\n")

            f.write("\n")
            sentence_count += 1

            if sentence_limit is not None and sentence_count >= sentence_limit:
                break

if __name__ == '__main__':
    args = docopt(usage)
    file_to_process = args["<file_to_proccess>"]
    n_sentences = int(args["<n_sentences>"]) if args["<n_sentences>"] != \
                                                "None" else None

    output_file = f'../files/tags_data/output_with_pos_SPACY_tags_{n_sentences}.txt'

    nlp = spacy.load("en_core_web_lg")

    with open(file_to_process, 'r', encoding='utf-8') as conllu_file:
        conllu_content = parse(conllu_file.read())

    convert_conllu_to_tagged_text(conllu_content, output_file,
                                  sentence_limit=n_sentences)

    print(f'data converted and saved to {output_file} with spaCy POS tags')