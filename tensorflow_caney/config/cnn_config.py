# -*- coding: utf-8 -*-

import sys
from typing import List, Optional
from omegaconf import OmegaConf
from dataclasses import dataclass, field


@dataclass
class Config:
    """
    CNN data configuration class (embedded with OmegaConf).
    """

    # directory to store all data files
    data_dir: str

    # directory to store inference output files
    inference_save_dir: str = 'results'

    # experiment name to track
    experiment_name: str = 'unet-cnn'
    
    # experiment type to track (normally embedded in the inference output)
    experiment_type: str = 'landcover'

    # seed to control the randomization
    seed: Optional[int] = 24

    # gpu devices to utilize
    gpu_devices: str = '0,1,2,3'
    
    # bool to enable mixed_precision
    mixed_precision: Optional[bool] = True

    # bool to enable linear acceleration
    xla: Optional[bool] = False

    # input bands from the incoming dataset
    input_bands: List[str] = field(
        default_factory=lambda:
            ['Blue', 'Green', 'Red', 'NIR1', 'HOM1', 'HOM2'])
    
    # output bands that will be used to train and predict from
    output_bands: List[str] = field(
        default_factory=lambda: ['Blue', 'Green', 'Red', 'NIR1'])

    # list of strings to support the modification of labels
    modify_labels: Optional[List[str]] = None

    expand_dims: bool = True
    tile_size: int = 256
    include_classes: bool = False
    augment: bool = True
    standardize: bool = True
    batch_size: int = 32
    n_classes: int = 1
    test_size: float = 0.20

    mean: List[float] = field(
        default_factory=lambda: [])
    std: List[float] = field(
        default_factory=lambda: [])

    # loss function expression, expects a loss function
    loss: str = 'tversky'

    learning_rate: float = 0.0001
    max_epochs: int = 6000
    patience: int = 7

    model_filename: str = 'model.h5'
    inference_regex: str = '*.tif'
    window_size: int = 8120
    inference_overlap: int = 2
    inference_treshold: float = 0.5
    pred_batch_size: int = 128

    # logging files
    # self.logs_dir = os.path.join(self.data_output_dir, 'logs')
    # self.log_file = os.path.join(
    #    self.logs_dir, datetime.now().strftime("%Y%m%d-%H%M%S") +
    #    f'-{self.experiment_name}.out')

    # setup directory structure, create directories
    # directories_list = [
    #    self.images_dir, self.labels_dir, self.model_dir,
    #    self.predict_dir, self.logs_dir]
    # self.create_dirs(directories_list)

    # std and means filename for preprocessing and training
    # self.std_mean_filename = os.path.join(
    #    self.dataset_dir, f'{self.experiment_name}_mean_std.npz')
    # set logger
    # self.set_logger(filename=self.log_file)


# -----------------------------------------------------------------------------
# Invoke the main
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    schema = OmegaConf.structured(Config)
    conf = OmegaConf.load("../config/config_clouds/vietnam_clouds.yaml")
    try:
        conf = OmegaConf.merge(schema, conf)
    except BaseException as err:
        sys.exit(f"ERROR: {err}")
    sys.exit(conf)
