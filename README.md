# DrQA-Elastic - Steps to push data to ElasticSearch

<ul>
  <li>python ./DrQA-Elastic/build_elastic_db.py ../articlesections.txt ../DB/elastic</li>
  <li>python ./DrQA-Elastic/build_elastic_tfidf.py ../DB/elastic ../DB</li>
<li>python ./DrQA-Elastic/interactive.py --model ../DB/elastic-tfidf-ngram\=2-hash\=16777216-tokenizer\=simple.npz</li>
<ul>

