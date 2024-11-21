import sys

from build_data import get_data

def load_operations(filename):
    try:
        with open(filename, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: Cannot open file {filename}")
        sys.exit(1)


def apply_filter_state(counties, state_abbr):
    filtered = [county for county in counties if county.state == state_abbr]
    print(f"Filter: state == {state_abbr} ({len(filtered)} entries)")
    return filtered


def apply_filter_gt(counties, field, value):
    filtered = [county for county in counties if getattr(county, field, None) > value]
    print(f"Filter: {field} gt {value} ({len(filtered)} entries)")
    return filtered


def apply_filter_lt(counties, field, value):
    filtered = [county for county in counties if getattr(county, field, None) < value]
    print(f"Filter: {field} lt {value} ({len(filtered)} entries)")
    return filtered


def display(counties):
    for county in counties:
        print(f"County: {county.county}, State: {county.state}")
        # Add additional details as needed


def population_total(counties):
    total_pop = sum(county.population for county in counties)
    print(f"2014 population: {total_pop}")


def population_field(counties, field):
    total_pop_field = sum(getattr(county, field, 0) * county.population / 100 for county in counties)
    print(f"2014 {field} population: {total_pop_field}")


def percent_field(counties, field):
    total_pop = sum(county.population for county in counties)
    total_field = sum(getattr(county, field, 0) * county.population / 100 for county in counties)
    percent = (total_field / total_pop) * 100 if total_pop else 0
    print(f"2014 {field} percentage: {percent:.2f}")


def process_operations(operations, counties):
    for idx, operation in enumerate(operations):
        try:
            operation = operation.strip()
            if not operation:
                continue  # Skip empty lines

            parts = operation.split(":")
            cmd = parts[0]

            if cmd == "display":
                display(counties)
            elif cmd == "filter-state":
                state_abbr = parts[1]
                counties = apply_filter_state(counties, state_abbr)
            elif cmd == "filter-gt":
                field, value = parts[1], float(parts[2])
                counties = apply_filter_gt(counties, field, value)
            elif cmd == "filter-lt":
                field, value = parts[1], float(parts[2])
                counties = apply_filter_lt(counties, field, value)
            elif cmd == "population-total":
                population_total(counties)
            elif cmd == "population":
                field = parts[1]
                population_field(counties, field)
            elif cmd == "percent":
                field = parts[1]
                percent_field(counties, field)
            else:
                print(f"Error: Invalid operation on line {idx + 1}")
        except Exception as e:
            print(f"Error: Malformed operation on line {idx + 1}: {operation.strip()}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python program.py <operations_file>")
        sys.exit(1)

    operations_file = sys.argv[1]
    operations = load_operations(operations_file)

    counties = get_data()
    print(f"Loaded {len(counties)} counties")

    process_operations(operations, counties)

main()