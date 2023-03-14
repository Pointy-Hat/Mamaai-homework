from pathlib import Path

DATA_FILE = Path(__file__).parent / "data"


class SampleDocuments:
    @staticmethod
    def basic():
        return (DATA_FILE / "sample.pdf").open("rb")

    @staticmethod
    def pet_rock():
        return (DATA_FILE / "pet_rock.pdf").open("rb")

    @staticmethod
    def image():
        return (DATA_FILE / 'image.png').open('rb')
