import lexic
import sintatic


def run():
    tokens = lexic.get_tokens()
    sintatic.run(tokens)
    # print("tokens", tokens)
