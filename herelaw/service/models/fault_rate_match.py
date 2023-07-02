def match(fault_rate_name):
    """
    이름
    """
    with open(f"herelaw/service/data/fault_rate/{fault_rate_name}", "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    print(match("fault_rate_0.txt"))
