import datasets
import numpy as np
import pandas as pd
from datasets import Dataset
from transformers import pipeline, AutoTokenizer, AutoModel
#TODO figure out if map for dataset will be faster than apply AND make requirements file
from transformers import RobertaTokenizer
from transformers import RobertaModel
import torch

#https://www.youtube.com/watch?v=ZMDRoscHe5o - tensorflow: possibly can do using code

#TODO time efficiency!!!!!!!!!!!1

#C:\Users\User\anaconda3\envs\myCreativeEnv\python.exe C:\Users\User\PycharmProjects\CreativeLanguageWithVenv\src\extract_creative_sentences_by_dim\Embeddings\bert_embeddings.py
# Some weights of the model checkpoint at roberta-base were not used when initializing RobertaModel: ['lm_head.layer_norm.bias', 'lm_head.layer_norm.weight', 'lm_head.dense.bias', 'lm_head.bias', 'lm_head.dense.weight']
# - This IS expected if you are initializing RobertaModel from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPreTraining model).
# - This IS NOT expected if you are initializing RobertaModel from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
# Some weights of RobertaModel were not initialized from the model checkpoint at roberta-base and are newly initialized: ['roberta.pooler.dense.weight', 'roberta.pooler.dense.bias']
# You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.

class ContextualizedEmbeddings:

        def __init__(self):
            """
               Initializes an instance of the ContextualizedEmbeddings
               class. The constructor loads the pre-trained 'roberta-base'
               model and tokenizer.
            """
            self.device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu")
            print(f"using device: {self.device}")
            model_name = 'roberta-base'
            self.__model = AutoModel.from_pretrained(model_name).to(self.device)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        def process_dataset(self, dataset)->Dataset:
            """
               Processes the CSV data to compute contextualized embeddings for each row.

               Args:
                   csv (pd.DataFrame): The input DataFrame containing the data.

               Returns:
                   pd.DataFrame: The updated DataFrame with the computed embeddings.
            """

            embeddings_dataset = dataset.apply(self.contextualized_embeddings, axis=1)

            filename = "see_tensor_file.tsv"
            embed_lst = embeddings_dataset["context embedding"].to_list()
            # np.savetxt(filename, embed_lst, delimiter="\t")

            return embeddings_dataset




        @torch.no_grad()
        def contextualized_embeddings(self, row, name_of_index_col,
                                      name_of_sent_col)\
                ->torch.tensor:
            """
                   Returns the contextualized embeddings for a specific verb
                   in a tokenized sentence.
                   Args:
                       row (pd.Dataframe): row containing information
                       about the sentence.
                       name_of_index_col (str): the name of the column in which
                                    the token indices are stored.
                       name_of_sent_col (str): the name of the column in which the
                                                tokenized sentences are stored.
                   Returns:
                       torch.tensor: The embeddings of the verb as a tensor.
                   Raises:
                       IndexError: If the verb_index is out of range for the
                        tokenized_text.

            """
            token_index = row[name_of_index_col]
            tokenized_sent = row[name_of_sent_col]
            input_ids = self.tokenizer.convert_tokens_to_ids(tokenized_sent)
            input_ids_tensor = torch.tensor([input_ids], device=self.device)
            outputs = self.__model(input_ids_tensor)
            embeddings = outputs.last_hidden_state[0][token_index]. \
                cpu().numpy()
            row["contextualized embedding"] = embeddings
            return row
        #https://huji.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=06d1c8ff-e73e-4237-b97f-afe000587e95
        # recitation about transformers and token ids
        # i want encoder-only

        # check if i can use pipeline with pretokenized text





if __name__ == '__main__':
    # Example usage
    # obj = ContextualizedEmbeddings()
    # text = ("i", "love", "you")
    # obj.contextualized_embeddings(text, 2)
    dtypes = {
        'lemma': str,
        'word form': str,
        'sentence': str,
        'doc index': int,
        'sent index': int,
        'token index': int,
    }
    converters = {'tokenized sentence': eval}
    c = pd.read_csv("see_VERB.csv", encoding='utf-8', dtype=dtypes,
                    converters=converters)

    csv_filename = "see_VERB_meta_file.csv"
    
    c.to_csv(csv_filename, sep='\t', index=False)

    d = ContextualizedEmbeddings().process_dataset(c)




