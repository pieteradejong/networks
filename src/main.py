import logging
from dotenv import load_dotenv
import network


def init():
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logging.info("Initializing application...")
    logging.info("Loaded environment variables")


def main():
    logging.info("Running application...")
    network.run_analysis()


if __name__ == "__main__":
    init()
    main()
