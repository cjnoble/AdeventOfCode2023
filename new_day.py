DAY = 21

day_str = f"{DAY:02d}"


with open(f"day_template.py", "r") as f_template:
    with open(f"day_{day_str}.py", "a") as f:
        day = f_template.readlines()
        day[21] = f"    DAY = \"{day_str}\"\n"
        f.writelines(day)

with open(f"test_template.py", "r") as f_template:
    with open(f"day_{day_str}_test.py", "a") as f:
        test = f_template.readlines()
        
        test[1] = f"import day_{day_str} as day\n"
        test[3] = f"DAY = \"{day_str}\"\n"

        f.writelines(test)

open(f"{day_str}.txt", "a")
open(f"{day_str}_test.txt", "a")