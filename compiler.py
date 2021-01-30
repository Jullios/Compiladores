import lexic
import sintatic
import semantic


def run():
    tokens = lexic.get_tokens()
    table = sintatic.run(tokens)
    semantic.run(table)
    # print("tokens", tokens)
