import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)

######################################################################

# Prepare data:

def prepare_sequence(seq, to_ix):
    idxs = [to_ix[w] for w in seq]
    # print (idxs)
    return torch.tensor(idxs, dtype=torch.long)

def import_training_data(filename, markfile):
    combined = []
    with open(filename) as text:
        with open(markfile) as mark:
            xlines = text.readlines()
            ylines = mark.readlines()

            for i in range(len(xlines)):

                xline_words_array = xlines[i].split(",")
                xline_words_array = [ x.replace('\n',"") for x in xline_words_array] # get rid of '\n'
                # trim the length and replace character
                length = len(xline_words_array)
                yline_words_array = ylines[i].split(",")
                yline_words_array = yline_words_array[:length]

                for i, x in enumerate(yline_words_array):
                    if(x=='#'):
                        yline_words_array[i] = "V"
                    elif (x == '@'):
                        yline_words_array[i] = "NN"
                    else:
                        yline_words_array[i] = "DET"

                # print(( xline_words_array, yline_words_array) )
                line = ( xline_words_array, yline_words_array)
                combined.append(line)
    return combined

corpus_data_name = "cookingTutorialCrawlEdit.csv"
marked_corpus_data = "mark_CT.csv"

# training_data = [
#     ("the dog ate the apple".split(), ["DET", "N1", "V", "DET", "N2"]),
#     ("everybody read that book".split(), ["N1", "V", "DET", "N2"]),
#     ("Tom feed the dog".split(), ["N1", "V", "DET","N2"]),
#     # ("Tom feed the dog".split(), ["NN", "V", "DET","NN"]),
#     ("prepare the grill".split(), ["V", "DET", "N2"]),
#     ("cook the peppers on the grill and give the skin a little charring".split(), ["V", "DET", "N2", "DET", "DET", "N3", "DET", "V", "DET", "N2", "DET", "DET", "N2"])
# ]
training_data = import_training_data(corpus_data_name, marked_corpus_data)

word_to_ix = {}
for sent, tags in training_data:
    for word in sent:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)
# print(word_to_ix)
tag_to_ix = {"DET": 0, "NN": 1, "V": 2}
ix_to_tag = {0: "DET", 1: "NN", 2: "V"}


# These will usually be more like 32 or 64 dimensional.
# We will keep them small, so we can see how the weights change as we train.
EMBEDDING_DIM = 6
HIDDEN_DIM = 6
EPOCH = 300
######################################################################
# Create the model:


class LSTMTagger(nn.Module):

    def __init__(self, embedding_dim, hidden_dim, vocab_size, tagset_size):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim

        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)

        # The LSTM takes word embeddings as inputs, and outputs hidden states
        # with dimensionality hidden_dim.
        self.lstm = nn.LSTM(embedding_dim, hidden_dim)

        # The linear layer that maps from hidden state space to tag space
        self.hidden2tag = nn.Linear(hidden_dim, tagset_size)
        self.hidden = self.init_hidden()

    def init_hidden(self):
        # Before we've done anything, we dont have any hidden state.
        # Refer to the Pytorch documentation to see exactly
        # why they have this dimensionality.
        # The axes semantics are (num_layers, minibatch_size, hidden_dim)
        return (torch.zeros(1, 1, self.hidden_dim),
                torch.zeros(1, 1, self.hidden_dim))

    def forward(self, sentence):
        embeds = self.word_embeddings(sentence)
        lstm_out, self.hidden = self.lstm(
            embeds.view(len(sentence), 1, -1), self.hidden)
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        tag_scores = F.log_softmax(tag_space, dim=1)
        return tag_scores

######################################################################
# Train the model:


model = LSTMTagger(EMBEDDING_DIM, HIDDEN_DIM, len(word_to_ix), len(tag_to_ix))
loss_function = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

# See what the scores are before training
# Note that element i,j of the output is the score for tag j for word i.
# Here we don't need to train, so the code is wrapped in torch.no_grad()
with torch.no_grad():
    inputs = prepare_sequence(training_data[0][0], word_to_ix)
    tag_scores = model(inputs)
    # print(tag_scores)

for epoch in range(EPOCH):  # again, normally you would NOT do 300 epochs, it is toy data
    print('epoch ',epoch)
    for sentence, tags in training_data:
        # Step 1. Remember that Pytorch accumulates gradients.
        # We need to clear them out before each instance
        model.zero_grad()

        # Also, we need to clear out the hidden state of the LSTM,
        # detaching it from its history on the last instance.
        model.hidden = model.init_hidden()

        # Step 2. Get our inputs ready for the network, that is, turn them into
        # Tensors of word indices.
        sentence_in = prepare_sequence(sentence, word_to_ix)
        targets = prepare_sequence(tags, tag_to_ix)

        # Step 3. Run our forward pass.
        tag_scores = model(sentence_in)

        # Step 4. Compute the loss, gradients, and update the parameters by
        #  calling optimizer.step()
        loss = loss_function(tag_scores, targets)
        loss.backward()
        optimizer.step()

# See what the scores are after training
with torch.no_grad():
    inputs = prepare_sequence("Take,croutons,and,toss,it,with,the,vegetables".split(","), word_to_ix)
#     inputs = prepare_sequence(training_data[2][0], word_to_ix)
    tag_scores = model(inputs)

    # The sentence is "the dog ate the apple".  i,j corresponds to score for tag j
    # for word i. The predicted tag is the maximum scoring tag.
    # Here, we can see the predicted sequence below is 0 1 2 0 1
    # since 0 is index of the maximum value of row 1,
    # 1 is the index of maximum value of row 2, etc.
    # Which is DET NOUN VERB DET NOUN, the correct sequence!

    #     print(tag_scores)
    max_list = torch.max(tag_scores, 1)
    seq_list = [item.tolist() for item in max_list]
    print("index: ", seq_list[1])
    result_list = []
    for idx in seq_list[1]:
        result_list.append(ix_to_tag[idx])
    print(result_list)
