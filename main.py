from core.eclat import eclat
from utils.data_io import save_rules


def main() -> None:
    rules = eclat()
    save_rules(rules)


if __name__ == "__main__":
    main()
