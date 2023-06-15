from lightchain.prompt import Prompt
from lightchain.chain import LambdaChain
import fire
import ir_datasets as irds
from .helper import *


def main(dataset, eval_set, model_name, cut=50, examples_per_query=3):
    eval_set = irds.load(dataset)

    retriever = None % cut # any First pass retriever
    reranker = None # Assume GRF ranker with weights for expansion

    keywords_prompt = Prompt('Generate Keywords that describe these documents \n {examples} Keywords:', ['examples'], name='keywords')
    entities_prompt = Prompt('Generate a list of Entities that describe these examples \n {examples} \n Entities:', ['examples'], name='entities')
    summary_prompt = Prompt('Generate a Summary of these examples \n {examples} \n Summary:', ['examples'], name='summary')

    extract = keywords_prompt | entities_prompt | summary_prompt

    chained_tasks = extract  >> Llama(model_name, keep_prompt=False) >> LambdaChain(func=lambda x : [' '.join(item.values()) for item in x])
    transformer_chain = ExpansionChain(model=chained_tasks, out_attr='expansion', examples_per_query=examples_per_query, name='transformer_chain')

    pipeline = retriever >> transformer_chain >> reranker
    scores = pipeline(eval_set.queries_iter())

if __name__ == '__main__':
    fire.Fire(main)