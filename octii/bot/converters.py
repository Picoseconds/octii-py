import inspect

from typing import List

def int_converter(raw_arg):
    return int(raw_arg)

converters = {
    'int': lambda x, _: int(x),
    'str': lambda x, _: x,
    'Message': lambda msg_id, bot: bot._api_client.fetch_message(msg_id)
}

def convert_args(func, bot, params_data: List[inspect.Parameter], *args):
    parameters = list(params_data)[1:]
    func_args = []

    for i, param in enumerate(parameters):
        func_args.append(converters['str' if param.annotation == inspect.Parameter.empty else param.annotation.__name__](args[i], bot))

    return func_args
