import abc


class PartitionDetectionServiceInterface(abc.ABC):
    @abc.abstractmethod
    def get_partition_table_type(self, device: str) -> str:
        pass
