import argparse
import logging
import os
import time
from queue import Queue
from threading import Semaphore, Thread

import sourcing
from processing import Processing

inp_semaphore = Semaphore(value=0)


def parse_args():
    """
    Function used for parsing input arguments.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rows",
        required=False,
        default=1024,
        type=int,
        help="Image height to generate",
    )
    parser.add_argument(
        "--columns",
        required=False,
        type=int,
        default=768,
        help="Image width to generate",
    )
    parser.add_argument(
        "--channels",
        required=False,
        type=int,
        default=3,
        help="Image channels to generate",
    )
    parser.add_argument(
        "--iterations",
        required=False,
        default=100,
        type=int,
        help="number of images to generate",
    )
    parser.add_argument(
        "--output",
        required=False,
        default="processed",
        help="name of folder for processed images",
    )
    return parser.parse_args()


def consumer(input_queue: Queue, output_queue: Queue, processing):
    """ Consumer service function.
    Gets image from one queue runs it into processing pipeline
    and then stores into another queue and writes it down
    to desired output folder.
    Args:
        input_queue (Queue): Queue with raw images
        output_queue (Queue): Queue with processed images
        processing (_type_): Processing class instance
    """
    logging.info("Thread consumer is working")

    while inp_semaphore.acquire():
        if not input_queue.empty():
            frame = input_queue.get()
            processed = processing.transform_image(frame)
            output_queue.put(processed)

            output_queue.task_done()
        else:
            logging.info("Thread consumer has finished")
            break


def producer(input_queue: Queue, source: sourcing.Source, iterations: int):
    """Producer service function.
    Fetches image from source, writes it down into queue and releases
    the semaphore.
    Args:
        input_queue (Queue): Queue to save raw images
        source (sourcing): Source class instance
        iterations (int): number of processed images
    """

    logging.info("Thread Producer is working")

    for _ in range(iterations):
        data = source.get_data()
        input_queue.put(data)
        inp_semaphore.release()
        time.sleep(0.05)

    inp_semaphore.release()  # release the semaphore, to finish consumer thread
    logging.info("Thread Producer has finished")


def main():
    """
    Main function used for running the entire application
    """

    formatting = "%(asctime)s: %(message)s"
    logging.basicConfig(format=formatting, level=logging.INFO, datefmt="%H:%M:%S")

    args = parse_args()
    os.makedirs(os.path.join(os.getcwd(), args.output), exist_ok=True)
    processing = Processing((args.rows, args.columns, args.channels))
    source = sourcing.Source((args.rows, args.columns, args.channels))

    # Making queues for future use
    queue_A = Queue(maxsize=1)  # variable should be lowercase, but there was capital letter in instruction
    queue_B = Queue(maxsize=-1)  # variable should be lowercase, but there was capital letter in instruction

    # Creating threads
    prod = Thread(target=producer, args=(queue_A, source, args.iterations))
    csr = Thread(
        target=consumer,
        args=(queue_A, queue_B, processing),
    )

    # Starting threads
    logging.info("Main    : Before starting the thread")
    prod.start()
    csr.start()

    logging.info("Main    : wait for the threads to finish")

    # Joining threads
    prod.join()
    csr.join()
    processing.save_images(args.output, queue_B, args.iterations)  # saving images

    logging.info("Main    : all done")


if __name__ == "__main__":
    main()
