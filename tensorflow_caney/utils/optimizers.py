import sys
import tensorflow as tf
import segmentation_models as sm
import tensorflow_addons as tfa
from typing import Any


def get_optimizer(optimizer: str) -> Any:
    """
    Get optimizer function from string evaluation.
    Args:
        optimizer (str): string with optimizer callable.
    Returns:
        Callable.
    """
    try:
        optimizer = eval(optimizer)
    except NameError as err:
        sys.exit(f'{err}. Accepted optimizers from {tf}, {sm}, {tfa}')
    return optimizer
