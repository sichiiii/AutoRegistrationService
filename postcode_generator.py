from faker import Faker
from app_logger import get_logger


class PostcodeGenerator:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.uk_faker = Faker('en_GB')

    def generate_postcode(self):
        try:
            postcode = self.uk_faker.postcode()
            return postcode
        except Exception as ex:
            self.logger.error(str(ex))
