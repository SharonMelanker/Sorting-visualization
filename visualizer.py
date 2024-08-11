"""
Imports
"""
import sys
import pygame
import random
import math

"""
Initialization of pygame properties
"""
pygame.init()
pygame.mixer.init()

"""
Sounds initialization
"""
start_sort_sound = pygame.mixer.Sound("mixkit-game-ball-tap-2073.wav")
end_sort_sound = pygame.mixer.Sound("mixkit-unlock-game-notification-253.wav")

"""
Constants
"""
# Colors
BAR_COLOR = pygame.Color('dodgerblue')
BAR_COLOR2 = pygame.Color(105, 119, 249)
BAR_COLOR3 = pygame.Color(95, 105, 220)
BACKGROUND_COLOR = pygame.Color('black')
TEXT_COLOR = pygame.Color('white')
HIGHLIGHT_COLOR1 = pygame.Color('green')
HIGHLIGHT_COLOR2 = pygame.Color('RED')

# Gradient
BAR_COLORS = [BAR_COLOR, BAR_COLOR2, BAR_COLOR3]

# Fonts
FONT = pygame.font.SysFont('comicsans', 30)

# Sizes
WIDTH = 1366
HEIGHT = 768


# TEXTS
MAIN_CAPTION = "Sorting Algorithms Visualization"
SWAP = "swap"



class DrawInformation:
    """
    Draw informaion class that handles all drawing operations within pygame
    """
    def __init__(self, bar_list: list[int]):
        """
        Constructor of the DrawInformation class
        :param bar_list: list of integers (The values to sort)
        """
        self.start_x = None
        self.block_height = None
        self.block_width = None
        self.max_val = None
        self.min_val = None
        self.bar_list: list[int] = bar_list
        self.width: int= WIDTH
        self.height: int = HEIGHT
        self.action_log = []
        self.SIDE_PAD: int = 100
        self.TOP_PAD: int = 150

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(MAIN_CAPTION)
        self.set_list(self.bar_list)


    def log_action(self, action) -> None:
        """
        a function that log that last operation and stores it in order to be able to go back.
        :param action: the action to log, a 5 elements tuple (action, index1, value1, index2, value2)
        :return: None
        """
        self.action_log.append(action)

    def undo(self) -> None:
        """
        This function operates the "undo" of the action
        when the user click 'u', the sorting algorithm returns 1 step back.
        :return: Nonde
        """
        if self.action_log:
            action = self.action_log.pop()
            if action[0] == SWAP:
                # destruct from the tuple the variables to change
                _, idx1, val1, idx2, val2 = action
                self.bar_list[idx1], self.bar_list[idx2] = val1, val2
                self.draw_bars(self.bar_list)
                pygame.display.flip()

    def set_list(self, bar_list):
        """
        Initializing the list as a view
        :param bar_list: the list to generate view from.
        :return: None
        """
        self.bar_list = bar_list
        self.min_val = min(self.bar_list)
        self.max_val = max(self.bar_list)

        self.block_width = round((self.width - self.SIDE_PAD) / len(self.bar_list))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

    def draw_text_middle(self, text, font, color, y) -> None:
        """
        draw a line of text in the middle of the window
        :param text: the text to draw
        :param font: the font of the text
        :param color: the color of the text
        :param y: the height
        :return: None
        """
        label = font.render(text, 1, color)
        self.window.blit(label, (self.width / 2 - (label.get_width() / 2), y))

    def draw_bars(self, bar_list, color_positions=None):
        """

        :param bar_list: the bar list to draw
        :param color_positions: possible dictionary of colors for each index of the swap
        :return:
        """
        if color_positions is None:
            color_positions = {}
        bar_width = self.width // len(bar_list)
        for i, val in enumerate(bar_list):
            x = i * bar_width
            bar_height = int((val / max(bar_list)) * (self.height - 150))
            color = BAR_COLORS[i % 3]
            if i in color_positions:
                color = color_positions[i]
            pygame.draw.rect(self.window, color, (x, self.height - bar_height, bar_width, bar_height))

    def fill_background(self) -> None:
        """
        A function that fills the background of the window
        :return: None
        """
        self.window.fill(BACKGROUND_COLOR)

    def clear_actions(self):
        self.action_log = []


def generate_starting_list(n: int, min_val: int, max_val: int) -> list[int]:
    """
    A function that generates the starting list of integers to sort
    :param n:  number of values to generate
    :param min_val: minimum value
    :param max_val: maximum value
    :return:
    """
    lst: list[int] = []

    for _ in range(n):
        val: int = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info: DrawInformation, ascending=True) -> None:
    """
    a bubble sort algorithm implementation
    :param draw_info: and draw info instance
    :param ascending: whether the sorting algorithm is ascending or descending
    :return: None
    """
    lst: list[int] = draw_info.bar_list

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                draw_info.log_action((SWAP, j, lst[j], j + 1, lst[j + 1]))
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_info.draw_bars(lst, {j: HIGHLIGHT_COLOR1, j + 1: HIGHLIGHT_COLOR2})
                yield True

    return lst


def insertion_sort(draw_info: DrawInformation, ascending=True) -> None:
    """
    an insertion sort algorithm implemenation
    :param draw_info: the draw info instance
    :param ascending: whether the sorting algorithm is ascending or descending
    :return: None
    """
    lst = draw_info.bar_list

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break
            draw_info.log_action((SWAP, i, lst[i], i-1, lst[i-1]))
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_info.draw_bars(lst, {i - 1: HIGHLIGHT_COLOR1, i: HIGHLIGHT_COLOR2})
            yield True

    return lst


def selection_sort(draw_info: DrawInformation, ascending=True) -> None:
    """
    a selection sort algorithm implementation
    :param draw_info: a draw info instance
    :param ascending: whether the sorting algorithm is ascending or descending
    :return: None
    """
    lst = draw_info.bar_list
    for i in range(len(lst)):
        min_index = i
        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[min_index] and ascending) or (lst[j] > lst[min_index] and not ascending):
                min_index = j
            draw_info.draw_bars(lst, {j: HIGHLIGHT_COLOR2})
            yield True
        draw_info.log_action((SWAP, i, lst[i], min_index, lst[min_index]))
        lst[i], lst[min_index] = lst[min_index], lst[i]
        print("draw")
        draw_info.draw_bars(lst, {i: HIGHLIGHT_COLOR1, min_index: HIGHLIGHT_COLOR2})
        yield True


def merge(draw_info: DrawInformation, ascending: bool, l: int, mid: int, r: int) -> None:
    """
    merge function help for the merge sort algorithm implementation
    :param draw_info: the draw info instance
    :param l: left index
    :param mid: middle index
    :param r: right index
    :param ascending: wether the sorting algorithm is ascending or descending
    :return: None
    """
    lst = draw_info.bar_list
    n1 = mid - l + 1
    n2 = r - mid
    L = lst[l:mid + 1]
    R = lst[mid + 1: r + 1]
    i = 0
    j = 0
    k = l
    while i < n1 and j < n2:
        if (L[i] < R[j] and ascending) or (L[i] > R[j] and not ascending):
            draw_info.log_action((SWAP, k, lst[k], i, L[i]))
            lst[k] = L[i]
            i += 1
        else:
            draw_info.log_action((SWAP, k, lst[k], j, R[j]))
            lst[k] = R[j]
            j += 1
        draw_info.draw_bars(lst, {k: HIGHLIGHT_COLOR1})
        yield True
        k += 1
    while i < n1:
        draw_info.log_action((SWAP, k, lst[k], i, L[i]))
        lst[k] = L[i]
        i += 1
        k += 1
        draw_info.draw_bars(lst, {k: HIGHLIGHT_COLOR1})
        yield True
    while j < n2:
        lst[k] = R[j]
        j += 1
        k += 1
        draw_info.draw_bars(lst, {k: HIGHLIGHT_COLOR1})
        yield True


def merge_sort(draw_info: DrawInformation, ascending=True, l=0, r=None ) -> None:
    """
    a merge sort algorithm implementation
    :param draw_info:  the draw info instance
    :param l: left index
    :param r: right index
    :param ascending: whether the sorting algorithm is ascending or descending
    :return: None
    """
    lst = draw_info.bar_list
    if r is None:
        r = len(lst) - 1
    if (l < r):
        mid = l + (r - l) // 2
        yield from merge_sort(draw_info, ascending, l, mid, )
        yield from merge_sort(draw_info, ascending, mid + 1, r)
        yield from merge(draw_info, ascending, l, mid, r)
        draw_info.draw_bars(lst)
        yield True


def quick_sort(draw_info: DrawInformation, ascending=True, low=0, high=None, ) -> None:
    """
    a quick sort algorithm implementation
    :param draw_info: the draw info instance
    :param low: left index
    :param high: right index
    :param ascending: whether the sorting algorithm is ascending or descending
    :return: None
    """
    if high is None:
        high = len(draw_info.bar_list) - 1
    if low < high:
        pi = yield from partition(draw_info, ascending, low, high)
        yield from quick_sort(draw_info,ascending, low, pi - 1 )
        yield from quick_sort(draw_info,ascending, pi + 1, high)


def partition(draw_info: DrawInformation,ascending: bool, low: int, high: int) -> int:
    """
    a partition helper function for quick sort algorithm
    :param draw_info: the draw info instance
    :param low: left index
    :param high: right index
    :param ascending: whether the sorting algorithm is ascending or descending
    :return: the index of the pivot
    """
    lst = draw_info.bar_list
    pivot = lst[high]
    i = low - 1
    for j in range(low, high):
        if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
            print(f"sort {ascending}")
            i += 1
            draw_info.log_action((SWAP, i, lst[i], j, lst[j]))
            lst[i], lst[j] = lst[j], lst[i]
            draw_info.draw_bars(lst, {i: HIGHLIGHT_COLOR1, j: HIGHLIGHT_COLOR2})
            yield True  # Yield for visualization update
    draw_info.log_action((SWAP, i + 1, lst[i+1], high, lst[high]))
    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    draw_info.draw_bars(lst, {i: HIGHLIGHT_COLOR1, high: HIGHLIGHT_COLOR2})

    yield True  # Yield for final pivot swap visualization
    return i + 1  # Return the index of the pivot


def heap_sort(draw_info: DrawInformation, ascending=True) -> None:
    """
    a heap sort algorithm implementation
    :param draw_info: the draw info instance
    :param ascending: whether the sorting algorithm is ascending or descending
    :return: None
    """
    n = len(draw_info.bar_list)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(draw_info, n, i, ascending, False)
    for i in range(n-1, 0, -1):
        draw_info.log_action((SWAP, 0, draw_info.bar_list[0], i, draw_info.bar_list[i]))
        draw_info.bar_list[0], draw_info.bar_list[i] = draw_info.bar_list[i], draw_info.bar_list[0]
        yield from heapify(draw_info, i, 0, ascending, True)


def heapify(draw_info: DrawInformation, n: int, i: int, ascending: bool, update_display: bool) -> None:
    """
    a helper heapify helper function for heap sort algorithm
    :param draw_info: the draw info instance
    :param n: the number of elements in the heap
    :param i: the index
    :param ascending: whether the sorting algorithm is ascending or descending
    :param update_display: whether to update the display of the heap
    :return: None
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    should_update = False

    if left < n and ((draw_info.bar_list[left] > draw_info.bar_list[largest] and ascending) or (
            draw_info.bar_list[left] < draw_info.bar_list[largest] and not ascending)):
        largest = left
    if right < n and ((draw_info.bar_list[right] > draw_info.bar_list[largest] and ascending) or (
            draw_info.bar_list[right] < draw_info.bar_list[largest] and not ascending)):
        largest = right
    if largest != i:
        draw_info.log_action((SWAP, i, draw_info.bar_list[i],i+1, draw_info.bar_list[i+1]))
        draw_info.bar_list[i], draw_info.bar_list[largest] = draw_info.bar_list[largest], draw_info.bar_list[i]
        should_update = True

    if should_update:
        if update_display:
            draw_info.draw_bars(draw_info.bar_list, {i: HIGHLIGHT_COLOR1, largest: HIGHLIGHT_COLOR2})
            pygame.display.update()
            yield True
        yield from heapify(draw_info, n, largest, ascending, update_display)

def shaker_sort(draw_info: DrawInformation, ascending=True) -> None:
    """
    a shaker sort algorithm implementation
    :param draw_info: the draw info instance
    :param ascending: whether the sorting algorithm is ascending or descending
    :return:
    """
    lst = draw_info.bar_list
    n = len(lst)
    swapped = True
    start = 0
    end = n-1
    while swapped:
        swapped = False
        for i in range(start, end):
            if (lst[i] > lst[i + 1] and ascending) or (lst[i] < lst[i + 1] and not ascending):
                draw_info.log_action((SWAP, i, lst[i], i+1, lst[i+1]))
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                draw_info.draw_bars(lst, {i: HIGHLIGHT_COLOR1, i+1: HIGHLIGHT_COLOR2})
                swapped = True
                yield True
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if (lst[i] > lst[i + 1] and ascending) or (lst[i] < lst[i + 1] and not ascending):
                draw_info.log_action((SWAP, i, lst[i], i + 1, lst[i + 1]))
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                draw_info.draw_bars(lst, {i: HIGHLIGHT_COLOR1, i+1: HIGHLIGHT_COLOR2})
                swapped = True
                yield True
        start += 1


# sorting algorithms dictionary with names and sorts for each key
sorting_algorithms = {
    pygame.K_i: ("Insertion Sort", insertion_sort),
    pygame.K_b: ("Bubble Sort", bubble_sort),
    pygame.K_s: ("Selection Sort", selection_sort),
    pygame.K_m: ("Merge Sort", merge_sort),
    pygame.K_q: ("Quick Sort", quick_sort),
    pygame.K_h: ("Heap Sort", heap_sort),
    pygame.K_c: ("Shaker Sort", shaker_sort),
}


def main() -> None:
    """
    main function
    :return: None
    """
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    bar_list = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(bar_list)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None
    draw_info.fill_background()
    draw_info.draw_bars(bar_list)
    draw_info.draw_text_middle("Bubble Sort - Ascending", FONT, TEXT_COLOR, 10)
    set_generator = False
    while run:
        draw_info.fill_background()
        draw_info.draw_bars(bar_list)
        draw_info.draw_text_middle(f"{sorting_algo_name} - {"Ascending" if ascending else "Descending"}", FONT,
                                   TEXT_COLOR, 10)
        draw_info.draw_text_middle("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", FONT, TEXT_COLOR,
                         50)
        draw_info.draw_text_middle("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | M - Merge Sort", FONT, TEXT_COLOR, 90)
        draw_info.draw_text_middle("Q - Quick Sort | H - Heap Sort | C - Shaker Sort", FONT, TEXT_COLOR, 130)

        # draw_info.draw_bars(bar_list)
        clock.tick(50)

        if sorting:
            try:

                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
                pygame.mixer.Sound.play(end_sort_sound)
        else:
            pass

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                bar_list = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(bar_list)
                draw_info.clear_actions()
                sorting = False
                set_generator = False
            elif event.key == pygame.K_SPACE and not sorting:
                pygame.mixer.Sound.play(start_sort_sound)
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_n and not sorting:
                try:
                    if not set_generator:
                        sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                        set_generator = True
                    # sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                    next(sorting_algorithm_generator)
                except StopIteration:
                    sorting = False
            elif event.key == pygame.K_u:
                # Undo last sorting action
                draw_info.undo()
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key in sorting_algorithms:
                if not sorting:
                    sorting_algo_name, sorting_algorithm = sorting_algorithms[event.key]

            # TODO:  change the elif to switch case

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
