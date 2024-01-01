from tabulate import tabulate

table_data = [
    ["Name", "Age", "Job"],
    ["Mike", "22", "Programmer"],
    ["John", "24", "Teacher"],
    ["Jane", "23", "Designer"],
    ["Jack", "25", "Manager"]
]

print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid", showindex="always"))