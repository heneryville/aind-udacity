import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        print('Starting BIC selection')

        def bic(model):
            LL = model.score(self.X, self.lengths)
            p = model.n_components
            n_features = len(self.lengths)
            N = model.n_components**2 + 2*model.n_components*n_features -1
            return -2 * LL + p * math.log(N)

        # TODO implement model selection based on BIC scores
        models = [ self.base_model(n_components) for n_components in range(self.min_n_components, self.max_n_components+1)]
        scored_models = [ (bic(model), model) for model in models ]
        score, model = max(scored_models)
        return model

class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        def dic(model):
            def score_classes(classes):
              print(self.words, list(range(len(self.words))))
              indexes = [i for i in range(len(self.words)) if self.words[i] in classes] # Indexes of all the words in classes
              X, lengths = combine_sequences(indexes,self.all_word_sequences) # Combine all of those selections together to get what we're scoring on
              return model.score(X, lenghts)

            other_words = list(set(self.words) - set(self.this_word))
            return score_classes([self.this_word]) - score_classes(other_words)/len(other_words)

        # TODO implement model selection based on DIC scores
        models = [ self.base_model(n_components) for n_components in range(self.min_n_components, self.max_n_components+1)]
        scored_models = [ (dic(model), model ) for model in models ]
        score, model = max(scored_models)
        return model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        print('Running CV selector on', self.this_word)
        # TODO implement model selection using CV
        def cross_validate(n_components):
            try:
                liklihoods = []
                sequencesCnt = len(self.sequences)
                split_method = KFold( min(3, sequencesCnt) )
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                    # We clobber the X and lengths since the base_model function uses those to do the fit
                    self.X, self.lengths = combine_sequences(cv_train_idx, self.sequences)
                    testX, testLengths = combine_sequences(cv_test_idx, self.sequences)
                    print('Running cross validation for n_components', n_components)
                    model = self.base_model(n_components)
                    liklihoods.append(model.score(testX, testLengths))
                return sum(liklihoods)/len(liklihoods)
            except:
                print('Failed to train with n_components',n_components)
                return 0

        likelihoods = [ (cross_validate(n_components), n_components) for n_components in range(self.min_n_components, self.max_n_components+1)]
        likelihood, best_n_components = max(likelihoods)
        # We've got to train the model against the full data set
        # Reset the X and lengths since they were crudely mutated above
        self.X, self.lengths = self.hwords[self.this_word]
        return self.base_model(best_n_components)
