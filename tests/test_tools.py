# Copyright (c) OpenMMLab. All rights reserved.
import tempfile
from pathlib import Path
from subprocess import PIPE, Popen
from unittest import TestCase

import numpy as np
from PIL import Image

MMPRE_ROOT = Path(__file__).parent.parent


class TestConfusionMatrix(TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmpdir.name)

        self.config_file = MMPRE_ROOT / (
            'configs/deeplabv3plus'
            '/deeplabv3plus_r50-d8_4xb4-80k_potsdam-512x512.py')

        self.result_dir = self.dir
        matrix = np.random.randint(1, 7, size=(512, 512), dtype=np.uint8)
        img = Image.fromarray(matrix, mode='L')
        img.save(self.result_dir / '2_10_0_0_512_512.png')

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_run(self):
        command = [
            'python',
            'tools/analysis_tools/confusion_matrix.py',
            str(self.config_file),
            str(self.result_dir),
            str(self.result_dir),
            '--cfg-options',
            'test_dataloader.dataset.data_root'
            '=tests/data/pseudo_potsdam_dataset',
            'test_dataloader.dataset.data_prefix.img_path=img_dir',
            'test_dataloader.dataset.data_prefix.seg_map_path=ann_dir',
        ]
        Popen(command, cwd=MMPRE_ROOT, stdout=PIPE).wait()
