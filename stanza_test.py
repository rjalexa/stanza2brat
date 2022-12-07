""" minimal Stanford STANZA demo
    runs under the stanza environment
    conda activate stanza
    Will read a text from the IN_TXT constant in this code
    Will generate the corresponding BRAT files to display the results
"""
# import libraries
import pandas as pd
import stanza

# declare constants and other variables
TOKLET = "T"  # used by BRAT to prefix Token unique IDs
RELLET = "R"  # used by BRAT to prefix Relationship unique IDs
LANG = "it"
UPOSCOLSDICT = {
    "ADJ": "pink",
    "ADP": "#FF99FF",
    "ADV": "beige",
    "AUX": "#FF6699",
    "CCONJ": "lavender",
    "DET": "orange",
    "INTJ": "lime",
    "NOUN": "yellow",
    "NUM": "green",
    "PART": "cyan",
    "PRON": "orchid",
    "PROPN": "aqua",
    "PUNCT": "lemonchiffon",
    "SCONJ": "grey",
    "SYM": "gold",
    "VERB": "#99FFFF",
    "X": "orange",
}
uposcolsdf = pd.DataFrame(
    UPOSCOLSDICT.items(), columns=["pos", "col"]
)  # upos tag and corresponding color dataframe
# input text
IN_TXT = """
Il paziente Dante Alighieri è stato ricoverato presso il reparto di cardiochirurgia con un quadro di ischemia coronarica acuta.
La determinazione elettrocardiografica ed i marker plasmatici (troponina fast 5.6 mg/dl) hanno orientato verso una diagnosi di NSTEMI trattata con stenting coronarico.
Paziente dimesso in condizioni stabili.
Terapia:
POLIX*25mg 2cp al giorno ogni 12 ore lontano dai pasti
"""
IN_TXT = "Noi stiamo al sole. Chi sta al bar? Che bello questo pomeriggio."
# get Stanford's STANZA do its magic
# download appropriate language model
stanza.download(LANG, verbose=False)
# instantiate a analysis pipeline
nlp = stanza.Pipeline(
    LANG, processors="tokenize,lemma,pos,depparse", verbose=False, use_gpu=False
)
# finally generate a STANZA document from the given text via the pipeline
doc = nlp(IN_TXT)
# initialize empty dataframes to hold token and syntactic relations
t_df = pd.DataFrame(columns=["text", "start", "end", "upos"])
r_df = pd.DataFrame(columns=["srcupos", "deprel", "destid"])
# cycle through STANZA's Document, Sentence, Token, Words and add dataframe rows
for i, sentence in enumerate(doc.sentences):
    for t in sentence.tokens:
        for w in t.words:
            # fill a token spans and a relationships dataframe
            eid = f"{i+1}_{t.id[0]}"  # build a unique ID
            text = f"{t.text}"
            start = f"{t.start_char}"
            end = f"{t.end_char}"
            upos = f"{w.upos}"
            tlist = [text, start, end, upos]
            t_df.loc[
                f"{TOKLET}{eid}"
            ] = tlist  # add list for a token as new to dataframe row and use tid as the index value
            srcupos = f"{w.upos}"
            deprel = f"{w.deprel}"
            destid = f"{i+1}_{w.head}"
            rlist = [srcupos, deprel, destid]
            r_df.loc[
                f"{eid}"
            ] = rlist  # add list of relations as row to dataframe with id index value

### now reading from the dataframes write all BRAT Standoff files
## These are the corresponding txt and ann anallysis files
# txt file
with open("test.txt", "w", encoding="utf-8") as f:
    f.write(IN_TXT)
# ann file
with open("test.ann", "w", encoding="utf-8") as f:
    for row in t_df.itertuples():
        f.write(
            f"{row.Index}\t{row.upos} {row.start} {row.end}\t{row.text}\n"
        )  # entity annotations
    for row in r_df.itertuples():
        if row.deprel != "root":
            f.write(
                f"{RELLET}{row.Index}\t{row.deprel.replace(':','_')} Arg1:T{row.Index} Arg2:{TOKLET}{row.destid}\n"
            )  # relation annotations
## These are the annotation.con and visual.conf configuration files
# annotation.conf file
with open("annotation.conf", "w", encoding="utf-8") as f:
    f.write("[entities]\n")
    for row in uposcolsdf.itertuples():
        f.write(row.pos + "\n")
    f.write("[relations]\n")
    for row in r_df.itertuples():
        if row.deprel != "root":
            destupos = t_df.loc[f"{TOKLET}{row.destid}"].upos
            f.write(
                f"{row.deprel.replace(':','_')}\tArg1:{row.srcupos}, Arg2:{destupos}\n"
            )
    f.write("[events]\n")
    f.write("[attributes]\n")

# visual.conf file
with open("visual.conf", "w", encoding="utf-8") as f:
    f.write("[labels]\n")
    f.write("[drawing]\n")  # write UPOS tags and corresponding chosen colors
    for row in uposcolsdf.itertuples():
        f.write(f"{row.pos}\tbgColor:{row.col}\n")
