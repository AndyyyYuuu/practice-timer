#!/usr/bin/env python3
import sys, time, json, random, os, select

base_dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(base_dir, "config.json")) as f:
    CONFIG = json.load(f)

def bar(value, length=20):
    blocks = [' ', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']
    max_value = 1.0
    scaled = value / max_value * length
    full_blocks = int(scaled)
    remainder = scaled - full_blocks
    fraction_index = int(remainder * (len(blocks) - 1) + 0.5)  # rounding
    
    bar = blocks[-1] * full_blocks
    if full_blocks < length:
        bar += blocks[fraction_index]
        bar = bar.ljust(length, blocks[0])
    return bar

def timer(total_time: float): 
    start_time = time.time()
    time_now = 0
    time_accumulated = 0
    while time_now < total_time:
        time_now = time_accumulated + time.time()-start_time
        if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
            input()
            time_accumulated += time.time() - start_time
            inp = input("Paused: enter to continue or enter s to skip: ").strip()
            print("\033[F\33[2K\r\033[F\033[F")
            if inp == "s": 
                return
            elif inp == "q": 
                return "q"
            start_time = time.time()
        print(f"\r|{bar(time_now / total_time)}| {int(time_now/60)}:{int(time_now%60):02d}", end='', flush=True)
        time.sleep(0.1)

def practice(routine_code): 

    for section in CONFIG["practices"][routine_code]["sections"]: 
        choices = section["choices"]
        for i in range(section.get("choose", 1)):
            chosen = random.choice(choices)
            choices.remove(chosen)
            print(f"{section['type']}: {chosen}")
            if section.get("time", False): 
                if timer(section["time"]*60) == "q": return
            input("\nNext >>>")
    print("PRACTICE COMPLETE!")
    input(">>>")

def prompt_loop(): 
    while True:
        inp = input("\033[F\r>>> ")
        for i in range(len(CONFIG["practices"])): 
            if inp.strip() == str(i+1): 
                os.system('clear')
                practice(tuple(CONFIG["practices"].keys())[i])
                return
        if inp.strip() == "q": 
            return "q"

def main(): 
    while True: 
        practices = CONFIG["practices"]
        practices_values = tuple(practices.values())
        os.system("clear")
        print("GET SOME PRACTICE")
        for i in range(len(practices)): 
            hours = int(practices_values[i]["time"]/60)
            minutes = int(practices_values[i]["time"]%60)
            print(f"[{i+1}] {practices_values[i]['name']} | {str(hours) + 'h' if hours != 0 else ''}{str(minutes) + 'm' if minutes != 0 else ''}")
        print("\n")
        if prompt_loop() == "q": 
            return 0

if __name__=="__main__":
    main()