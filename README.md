# LightChain - Stupidly Simple Chain Structures

Basic Library for CoT Prompting with general structures. Main idea is that all you really need for CoT prompting is a convienient abstract prompt template and memory structure such that you can fill in the blanks yourself.

Uses operator overrides to create CoT pipelines, currently availible is the >> sequential operator and | the fork operator to pass a single input to multiple components