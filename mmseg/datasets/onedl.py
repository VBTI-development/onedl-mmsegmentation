# Copyright (c) VBTI. All rights reserved.
import logging
from typing import List

import numpy as np
from mmpretrain.datasets._palette import DEFAULT_PALETTE

from ..registry import DATASETS
from .basesegdataset import BaseSegDataset

logger = logging.getLogger(__name__)


@DATASETS.register_module()
class OneDLDataset(BaseSegDataset):
    """Wrapper for OneDL datasets to mmsegmentation.

    For more information about OneDL datasets, please refer to
    https://onedl.ai.
    """

    def __init__(self,
                 dataset_name: str,
                 shuffle: bool = True,
                 **kwargs) -> None:
        self.dataset_name = dataset_name
        self.shuffle = shuffle
        super().__init__(**kwargs)

    def load_data_list(self) -> List[dict]:
        """Load annotation from directory or annotation file.

        Returns:
            list[dict]: All data info of dataset.
        """
        from onedl.client import Client
        client = Client()
        dataset = client.datasets.load(self.dataset_name, pull_blobs=True)
        if self.shuffle:
            # shuffle the dataset
            idx = list(range(len(dataset)))
            np.random.shuffle(idx)
            dataset = dataset[idx]

        label_map = dataset.label_map
        # this is a renaming label map that maps old labels to new once
        old_to_new_labels: dict = None

        data_list = []
        for img_path, seg_path in zip(dataset.inputs.path_iterator(),
                                      dataset.targets.path_iterator()):
            data_info = dict(
                img_path=img_path,
                seg_map_path=seg_path,
                label_map=old_to_new_labels,
                reduce_zero_label=self.reduce_zero_label,
                seg_fields=[])
            data_list.append(data_info)

        metainfo = {
            'classes': label_map.get_labels(),
            'palette': DEFAULT_PALETTE[:label_map.n_classes]
        }
        # Meta information load from annotation file will not influence the
        # existed meta information load from `BaseDataset.METAINFO` and
        # `metainfo` arguments defined in constructor.
        for k, v in metainfo.items():
            self._metainfo[k] = v
        return data_list
