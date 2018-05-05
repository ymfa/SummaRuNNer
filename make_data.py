import sys, os, re, glob, subprocess, json

def tokenize(filepath_pattern):
  filepaths = sorted(glob.glob(filepath_pattern))
  dash = re.compile(r'-+$')
  print("Tokenzing %d files..." % len(filepaths))
  docs = []
  for filepath in filepaths:
    command = ['java', 'edu.stanford.nlp.process.DocumentPreprocessor', '-tokenizerOptions', 'asciiQuotes=true,normalizeParentheses=false,normalizeOtherBrackets=false', filepath]
    result = subprocess.check_output(command, encoding='utf-8')
    sentences = []
    for sentence in result.splitlines():
      new_tokens = []
      for token in sentence.split():
        if dash.match(token):
          new_tokens.append('--')  # distinguish dash from hyphen
        else:
          for i, part in enumerate(token.split('-')):
            if i > 0: new_tokens.append('-')
            new_tokens.append(part)
      sentences.append(' '.join(new_tokens).lower())
    docs.append(sentences)
  print("Finished tokenizing.")
  return docs

def write_json(docs, output_filename):
  with open(output_filename, 'w') as f:
    for sents in docs:
      labels = ['0'] * len(sents)
      ex = {'doc':'\n'.join(sents), 'labels':'\n'.join(labels), 'summaries':''}
      f.write(json.dumps(ex, ensure_ascii=False) + "\n")
  print("Finished writing file %s." % output_filename)

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print("Usage: python make_data.py <filepath_pattern> <output_filepath>")
    print("Notes:")
    print("1. <filepath_pattern> containing wildcards has to be quoted to be read correctly.")
    print("2. The path to stanford-corenlp-3.7.0.jar must be `export`ed as CLASSPATH in Bash.")
    sys.exit()
  file_pattern = sys.argv[1]
  out_path = sys.argv[2]

  docs = tokenize(file_pattern)
  write_json(docs, out_path)
