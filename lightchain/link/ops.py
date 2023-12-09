from functools import partial
from types import FunctionType
from matchpy import Wildcard, Operation, Arity
from abc import abstractmethod
from typing import Any, Iterable
from lightchain.object import Link, chainable

def get_link(link) -> Any:
    """
    Coerces a given object into a chainable Link object if possible.

    Args:
        link (Any): The object to be coerced into a Link object.

    Returns:
        Any: The coerced Link object if possible, otherwise raises a ValueError.

    Raises:
        ValueError: If the passed object cannot be coerced into a Link object.
    """
    if isinstance(link, Wildcard):
        return link
    if issubclass(type(link), Link):
        return link
    if isinstance(link, FunctionType):
        return chainable(link)
    if isinstance(link, list):
        return SequentialPipeline(link)
    raise ValueError("Passed parameter %s of type %s cannot be coerced into a chain" % (str(link), type(link)))

class Pipeline(Link, Operation):
    """
    The Pipeline class represents a sequence of operations (Links) to be performed in a specific order.
    It inherits from both the Link and Operation classes.

    Attributes:
        name (str): The name of the Pipeline object. Default is 'Pipeline'.
        arity (Arity): The matchpy arity of the Pipeline object. Effectively can it take >2 operands Default is Arity.polyadic.
        links (dict): A dictionary mapping link names to Link objects. It is populated in the initializer.

    Args:
        operands (Iterable): An iterable of objects to be coerced into Link objects and added to the pipeline.
        **kwargs: Additional keyword arguments are passed to the super class initializers.
    """
    name = 'Pipeline'
    arity = Arity.polyadic
    def __init__(self, operands : Iterable, **kwargs):
        super().__init__(operands=operands, **kwargs)
        self.links = {link.name : get_link(link) for link in operands}

    def __getitem__(self, i) -> Any:
        return self.links[i]

    def __len__(self) -> int:
        return len(self.links)

    @abstractmethod
    def __call__(self, input) -> Any:
        raise NotImplementedError

class SequentialPipeline(Pipeline):
    """
    The SequentialPipeline class represents a sequence of operations (Links) to be performed in a specific order.
    It inherits from the Pipeline class.

    Attributes:
        name (str): The name of the SequentialPipeline object. Default is 'Sequential Pipeline'.

    Args:
        operands (Iterable): An iterable of objects to be coerced into Link objects and added to the pipeline.
        **kwargs: Additional keyword arguments are passed to the super class initializers.
    """
    name = 'Sequential Pipeline'
    def __init__(self, operands : Iterable, **kwargs):
        """
        Initializes the SequentialPipeline object. It coerces the operands into Link objects and adds them to the pipeline.
        """
        super().__init__(operands=operands, **kwargs)

    def logic(self, args, **kwargs):
        """
        Implements the logic of the SequentialPipeline. It applies each link in the pipeline to the input in order.

        Args:
            args (Any): The input to the pipeline.
            **kwargs: Additional keyword arguments are passed to the link.

        Returns:
            Any: The output of the pipeline.
        """
        out = args
        for link in self.links.values():
            if isinstance(out, dict): out = {k : link(v, **kwargs) for k, v in out.items()}
            else: out = link(out, **kwargs)
        return out

    def __call__(self, *args, **kwargs) -> Any:
        """
        Calls the 'logic' method with the given arguments.

        Args:
            *args: The input to the pipeline.
            **kwargs: Additional keyword arguments are passed to the link.

        Returns:
            Any: The output of the pipeline.
        """
        if len(args) == 1: return self.logic(args[0], **kwargs)
        else: return [*map(partial(self.logic, **kwargs), args)]

class ForkPipeline(Pipeline):
    """
    The ForkPipeline class represents a set of operations (Links) to be performed in parallel.

    Attributes:
        name (str): The name of the ForkPipeline object. Default is 'Forked Pipeline'.

    Args:
        operands (Iterable): An iterable of objects to be coerced into Link objects and added to the pipeline.
        **kwargs: Additional keyword arguments are passed to the super class initializers.
    """
    name = 'Forked Pipeline'
    def __init__(self, operands : Iterable, **kwargs):
        super().__init__(operands=operands, **kwargs)

    def __call__(self, *args, **kwargs) -> Any:
        """
        Applies each link in the pipeline to the input in parallel.

        Args:
            *args: The input to the pipeline.
            **kwargs: Additional keyword arguments are passed to the link.

        Returns:
            Any: The output of the pipeline.
        """
        if args:
            if len(args) == 1: return [self(**inp) for inp in args[0]]
            else: return map(self, args)
        elif kwargs:
            if isinstance(args[0], dict): return {k : self(v, **kwargs) for k, v in args[0].items()}
            return {link.name : link(**kwargs) for link in self.link}