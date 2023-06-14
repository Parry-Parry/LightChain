from lightchain.chain import Chain, LambdaChain, TerrierChain
from lightchain.prompt import Prompt, FewShotPrompt
from lightchain.object import Model
import fire
import ir_datasets as irds
from .helper import *


def main(dataset, eval_set, model_name, cut=10):
    eval_set = irds.load(dataset).get_topics()

    retriever = None % cut
    terrier = TerrierChain(model=retriever)
    parse = LambdaChain(lambda x: x)

    keywords_prompt = Prompt('Generate Keywords that describe these documents \n {examples} Keyword:', ['examples'], name='keywords')
    entities_prompt = Prompt('Generate a list of Entities that describe these examples \n {examples} \n Entities:', ['examples'], name='entities')
    summary_prompt = Prompt('Generate a Summary of these examples \n {examples} \n Summary:', ['examples'], name='summary')

    generate = Llama(model_name, keep_prompt=False)

    first_pass = terrier >> parse
    extract = keywords_prompt | entities_prompt | summary_prompt

    chained_tasks = first_pass >> extract  >> generate

if __name__ == '__main__':
    fire.Fire(main)