from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from typing import Union, List

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class EncoderBackend():
    """ Sentence-Bert embedding model

    The Encoder class is used to generate document, sentence or word embeddings.

    Arguments:
        embedding_model: A sentence-transformers embedding model

    Usage:
        To create a model, you need to load a sentence_transformers model:
        ```python
            from backend import EncoderBackend
            sentence_model = EncoderBackend("paraphrase-MiniLM-L6-v2")
        ```

    or  you can instantiate a model yourself:

    ```python
        from backend import EncoderBackend
        from sentence_transformers import SentenceTransformer

        embedding_model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        sentence_model = EncoderBackend(embedding_model)
    ```
    """

    def __init__(self, embedding_model: Union[str, SentenceTransformer]):
        super().__init__()

        if isinstance(embedding_model, str):
            self.embedding_model = SentenceTransformer(embedding_model)

        elif isinstance(embedding_model, SentenceTransformer):
            self.embedding_model = embedding_model

        else:
            raise ValueError("Please select a valid SentenceTransformers model: \n"
                            "`from sentence_transformers import SentenceTransformer` \n"
                            "`model = SentenceTransformer('paraphrase-MiniLM-L6-v2')`")

    def embed(self,
        documents: Union[List[str], str, pandas.core.series.Series],
        progress_bar: bool=False, device: str="cuda",
        batch_size: int=1e3, to_numpy: bool=True):

        """ Embed a list of documents, sentences or words into an n-dimensional
        matrix of embeddings

        Arguments:
            documents: A list of documents or to be embedded
            progress_bar: Controls the verbosity of the process
            device: Where the models will run, CPU or GPU
            batch_size: The size of the batch
            to_numpy: Controls the output type

        Returns:
            Documents embeddings with shape (n, m) with `n` are the size of the corpus
            with embeddings of size `m`

        """

        embeddings = self.embedding_model.encode(documents,
                    device=device,  show_progress_bar=progress_bar,
                    convert_to_numpy=to_numpy, batch_size=batch_size)

        return embeddings
