from core.eclat import eclat


def main() -> None:
    rules = eclat()
    for rule in rules:
        print(rule)


if __name__ == "__main__":
    main()
