from nltk import pos_tag, ne_chunk, word_tokenize, tree


def extract_all_names(raw):
    toks = word_tokenize(raw)
    pos = pos_tag(toks)
    chunked_nes = ne_chunk(pos)
    return set([' '.join(map(lambda x: x[0], ne.leaves()))
                for ne in chunked_nes if isinstance(ne, tree.Tree)])
