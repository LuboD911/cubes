import random
import threading
import time

condition = threading.Condition()
queue = []


def build_vertical_pile(list_of_cubes):
    pile_volume = 0
    is_possible = True
    prev_element = None

    while list_of_cubes:
        first_cube = list_of_cubes[0]
        last_cube = list_of_cubes[-1]

        if last_cube > first_cube:
            removed_cube = list_of_cubes.pop()
        else:
            removed_cube = list_of_cubes.pop(0)

        if prev_element and prev_element < removed_cube:
            is_possible = False

        prev_element = removed_cube
        pile_volume += removed_cube ** 3

    if is_possible:
        print(f"Yes {pile_volume}")
    else:
        print(f"No {pile_volume}")


def produce(num_of_tests):
    for _ in range(num_of_tests):
        condition.acquire()
        num_of_cubes = int(input("number of cubes: "))
        string_input = input(f"enter {num_of_cubes} cubes: ")
        list_of_cubes = list(map(int, string_input.strip().split(' ')))
        queue.append(list_of_cubes)
        condition.notify()
        condition.release()
        time.sleep(random.randint(1, 3))


def consume(num_of_tests):
    for _ in range(num_of_tests):
        condition.acquire()
        if len(queue) == 0:
            condition.wait()
        list_of_cubes = queue.pop(0)
        build_vertical_pile(list_of_cubes)
        condition.release()
        time.sleep(random.randint(1, 3))


if __name__ == "__main__":
    num = int(input("number of test cases: "))
    producer = threading.Thread(target=produce, args=(num,))
    consumer = threading.Thread(target=consume, args=(num,))

    producer.start()
    consumer.start()
