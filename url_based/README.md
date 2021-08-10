# URL-based phishing detection

> We performed an initial exploration in phishing detection using one class neural network classifier.

TODO

1. [x] Solve dataset inconsistences
2. [x] Deduplicate dataset
3. [x] Find promissing URL embeddings
4. [x] Test one class classifier
5. Grid search

1.) The dataset was labeled using GSB. Because of that some samples has two different labels. Those samples were setted as phishing.

2.) All duplicated URL was removed. For that we had used the netloc information.

3.) We just tested two word embeddings model: `paraphrase-MiniLM-L6-v2` and `msmarco-distilbert-base-v3`.
We decided to use `paraphrase-MiniLM-L6-v2` model because the similarity between two URLs when only the path changes is higher than the ones computed using `msmarco-distilbert-base-v3` model.
Also, when the URL domain changes only a letter or word (a tell-tale sing of phishing), the similarity is lower for `msmarco-distilbert-base-v3` embeddings, which is bad.

4.) We built a simple fully-connected neural network (One Class SVM does not run on GPU, then we move on to NNs). The results showed *the model sucks*.
  - All phishing URLs was classified as safe.
  - The loss on validation and test stage are high.
  - The dataset is imbalanced
