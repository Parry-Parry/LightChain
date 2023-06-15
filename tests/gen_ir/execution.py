from lightchain.chain import LambdaChain
from lightchain.prompt import Prompt
import fire
import ir_datasets as irds
from .helper import *


def main(dataset, eval_set, model_name, cut=50, examples_per_query=3):
    eval_set = irds.load(dataset).get_topics()

    retriever = None % cut
    reranker = None
    collect = LambdaChain(lambda x : parse_chains(x, chains=['keywords', 'entities', 'summary']))

    keywords_prompt = Prompt('Generate Keywords that describe these documents \n {examples} Keywords:', ['examples'], name='keywords')
    entities_prompt = Prompt('Generate a list of Entities that describe these examples \n {examples} \n Entities:', ['examples'], name='entities')
    summary_prompt = Prompt('Generate a Summary of these examples \n {examples} \n Summary:', ['examples'], name='summary')

    generate = Llama(model_name, keep_prompt=False)

    extract = keywords_prompt | entities_prompt | summary_prompt
    expand = generate >> collect

    chained_tasks = extract  >> expand
    transformer_chain = ExpansionChain(model=chained_tasks, out_attr='expansion', name='transformer_chain')

    pipeline = retriever >> transformer_chain >> reranker
    scores = pipeline(eval_set.queries_iter())

if __name__ == '__main__':
    fire.Fire(main)