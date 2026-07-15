"""Small, testable functions for the programming chapter."""


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def describe_temperature(celsius: float) -> str:
    """Return a stable human-readable description."""
    if celsius < 0:
        return "below freezing"
    if celsius == 0:
        return "freezing point"
    if celsius < 20:
        return "cool"
    return "warm"


if __name__ == "__main__":
    value = 20.0
    print(f"{value:.1f} C = {celsius_to_fahrenheit(value):.1f} F")
    print(describe_temperature(value))
