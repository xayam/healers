import math

from n3utils import colorize_swap, get_sum_width, list_to_str


def n3c_recovery(width: int,
                 false_operation: int,
                 count: int,
                 ones: int,
                 position: int,
                 tool: int,
                 tool_change: int,
                 verbose: int=0) -> str:
    best = [1] * ones + [0] * (width - ones)
    if false_operation:
        return list_to_str(best)
    count += 1
    limit = 2 ** math.ceil(get_sum_width(width - 1))

    origin_position = position
    origin_tool_change = tool_change

    last_use_position = origin_position
    tool_change = origin_tool_change
    position = last_use_position
    data = best[:]
    while (count + tool_change > 0) and (tool_change > - limit):
        if verbose > 0:
            print(f"f={false_operation} c={count} o={ones} p={position} t={tool} " +
                  f"e={tool_change}, current={data}")
        if tool == 0:
            exist_exchange = False
            exist_pos = 0
            for i in range(position, width - 1):
                if (data[i] == 1) and (data[i + 1] == 0):
                    exist_exchange = True
                    exist_pos = i
                    break
            if not exist_exchange:
                tool = 1
                if tool_change == 0:
                    tool = 0
                    position -= 1
                else:
                    tool_change -= 1
                    position += 1  # origin_tool_change - tool_change + 1
                if verbose > 0:
                    print(f"f={false_operation} c={count} o={ones} p={position} t={tool} " +
                          f"e={tool_change}, current={data}")
                continue
            else:
                position = exist_pos
            message = f"{colorize_swap(data, position, position + 1)} -> "
            data[position], data[position + 1] = data[position + 1], data[position]
            message += f"{colorize_swap(data, position, position + 1)}"
            if verbose > 0:
                print(message)
            count -= 1
            position += 1
        elif tool == 1:
            exist_exchange = False
            exist_pos = 0
            for i in range(position, width - 1):
                if (data[i] == 1) and (data[i + 2] == 0):
                    exist_exchange = True
                    exist_pos = i
                    break
            if not exist_exchange:
                tool = 0
                tool_change -= 1
                position += 1  # origin_tool_change - tool_change + 1
                if verbose > 0:
                    print(f"f={false_operation} c={count} o={ones} p={position} t={tool} " +
                          f"e={tool_change}, current={data}")
                continue
            else:
                position = exist_pos
            message = f"{colorize_swap(data, position, position + 2)} -> "
            data[position], data[position + 2] = data[position + 2], data[position]
            message += f"{colorize_swap(data, position, position + 2)}"
            if verbose > 0:
                print(message)
            count -= 1
            position += 2
    return list_to_str(data)

# if position == width - 1:
#     position = 0
# elif degrees[position] == 1:
#     if position == width - 1:
#         tool = 0
#         tool_change -= 1
#     elif degrees[position + 2] == 1:
#         if degrees[position + 1] == 1:
#             position += 2
#         else:
#             pass
#     else:
#         message = f"{colorize_swap(degrees, position, position + 2)} -> "
#         degrees[position], degrees[position + 2] = degrees[position + 2], degrees[position]
#         message += f"{colorize_swap(degrees, position, position + 2)}"
#         if verbose > 0:
#             print(message)
#         count -= 1
#         position += 2
# else:
#     position += 1
