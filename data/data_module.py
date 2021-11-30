from pytorch_lightning import LightningDataModule
from torch.utils.data.dataloader import DataLoader
from .utils import DriveData
from torch.utils.data import random_split
from typing import Optional

class DriveDataModule(LightningDataModule):

    def __init__(self, data_root: str, mode="fold-validation"):
        assert mode in ["fold-validation", "inference"]

        drive_data = DriveData(data_root)
        
        train_data = drive_data.get_train()
        test_data = drive_data.get_test()

        if mode == "fold-validation":
            train_len = len(train_data)
            train_data, test_data = random_split(train_data, [train_len - train_len // 10, train_len // 10])

        self.train_data = DataLoader(train_data, batch_size=9, pin_memory=True)
        self.test_data = DataLoader(test_data, batch_size=1, pin_memory=True)

    def setup(self, stage: Optional[str] = None) -> None:
        print(f"stage: {stage}")

    def prepare_data(self) -> None:
        return super().prepare_data()

    def train_dataloader(self) -> DataLoader:
        return self.train_data

    def val_dataloader(self) -> DataLoader:
        return self.test_data

    def test_dataloader(self) -> DataLoader:
        return self.test_data