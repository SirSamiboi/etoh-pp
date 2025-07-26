import bisect, json, math, os, requests, time
import datetime as dt
import matplotlib.pyplot as pyplot
from matplotlib import style
from sty import fg, rs


# ==================== Initialising variables ==================== #


univ_id = 3264581003
user_id = None
towers = [] # tower_name, tower_abbr, tower_diff, badge_id, badge_id_old
towers_completed = [] # *towers, date_completed, datetime_completed
username = None
displayname = None

diff_names = ["Easy", "Medium", "Hard", "Difficult", "Challenging", "Intense", "Remorseless", "Insane", "Extreme", "Terrifying", "Catastrophic", "Horrific", "Unreal", "Nil"]
diff_colors = [(118, 244, 71), (255, 255, 0), (254, 124, 0), (255, 50, 50), (160, 0, 0), (71, 97, 128), (201, 0, 200), (0, 0, 255), (2, 138, 255), (0, 255, 255), (255, 255, 255), (150, 145, 255), (75, 0, 200), (121, 121, 129)]

milestones = {}
milestone_descriptions = {
    "50pp": "Intermediate - Reach a total of 50pp. It's clear that you've got potential. Good luck beating your \
        \nfirst Hard towers.",
    "100pp": "Capable - Reach a total of 100pp. You're becoming more accomplished as you approach your first \
        \nDifficult towers. Things are beginning to ramp up.",
    "200pp": "Skilled - Reach a total of 200pp. Reaching this point already takes a special amount of effort and \
        \nperseverance, so you should be proud of your progress so far.",
    "500pp": "Adept - Reach a total of 500pp. You're reaching a level of skill that surpasses the majority of \
        \nobbyists, as you begin to weave through obstacles with more agility and confidence.",
    "1000pp": "Talented - Reach a total of 1,000pp. Towers are becoming much harder and more demanding, and yet \
        \nyou push on. You've shown a proper talent in clearing towers one after the other, and you see \
        \nhardship as an invitation.",
    "2000pp": "Elite - Reach a total of 2,000pp. By now you're likely to have beaten your first Soul Crushing \
        \ntower, and can confidently proclaim your status as an elite obbyist.",
    "5000pp": "Expert - Reach a total of 5,000pp. You're pushing deeper into the Soul Crushing difficulties and \
        \nare reaching Extreme territory. Good luck on your journey even farther up the difficulty ladder.",
    "10000pp": "Master - Reach a total of 10,000pp. You continue to improve at an ever-increasing rate, and you \
        \nfind that you can easily blitz through towers that previously seemed impossibly difficult.",
    "20000pp": "Phenomenal - Reach a total of 20,000pp. Few can compare to your ability, as you've engraved \
        \nyourself into the upper echelons of the obbying community. You're one of the rare few even amongst \
        \nSoul Crushing victors.",
    "50000pp": "Legendary - Reach a total of 50,000pp. You've reached the peak of the difficulty chart and \
        \nhave conquered the Catastrophic difficulty. You can only look down upon all who aspire to achieve \
        \nyour level of skill, and you stand near unmatched, with the only exception being the absolute best.",
    "100000pp": "Unreal - Reach a total of 100,000pp. Most players will never even come close to your skill level. \
        \nEither start playing Pit of Misery or go outside.",
    "1t": "Getting Started - Beat your first tower. I hope you find enjoyment in overcoming the challenges \
        \nthat lie ahead. Good luck with your journey.",
    "10t": "Novice - Beat 10 towers. Well done, there's still a long way to go but you're making good progress.",
    "20t": "Amateur - Beat 20 towers. You're gaining skill and experience as you venture down through \
        \nThe Great Inferno, and up into the expansive Spatial System.",
    "50t": "Seasoned - Beat 50 towers. You're quickly improving, and the hours you've spent grinding towers \
        \nhave prepared you to tackle harder challenges.",
    "100t": "Triple Digits - Beat 100 towers. A monumental milestone that you should be very proud of. \
        \nYou've proven yourself to be a cut above the rest.",
    "200t": "Checklist Champion - Beat 200 towers. Through your vast gathering of experience, you've gained deep \
        \nunderstanding of EToH mechanics. It's clear that you greatly enjoy clearing tower after tower, \
        \nwading through the highs and lows of the game to claim more victories and complete entire areas.",
    "300t": "Seen It All - Beat 300 towers. You've poured hundreds of hours into beating towers one after \
        \nanother, and it shows. Keep pushing forward, you're almost at the endpoint. These final few towers \
        \nwill be the hardest, but you're capable of overcoming them with your fantastic skill and willpower.",
    "all_non_sc": "Completionist - Beat every non-Soul Crushing tower in the game. If you'd like to keep living a \
        \nproper life outside of EToH, this is more than a reasonable point to end your jorney. But don't be \
        \nsurprised if you come crawling back for more. ;)",
    "all_sc": "Unbreakable Spirit - Beat every Soul Crushing tower in the game. You never face away from even the \
        \nmost daunting and insurmountable of challenges. Few can even comprehend the skill and experience \
        \nyou've built up with each Soul Crushing completion, and you've now overcome every single challenge \
        \nin your way. Godspeed, your excellent talent and dedication have proven themselves.",
    "all_towers": "Perfectionist - Beat every single tower in the game. You're an absolute legend! The hundreds of \
        \nhours you've dedicated to grinding tower after tower have now paid off in their fullest. By now, \
        \nyour journey has shaped you into one of the greatest obbyists of all time, and you deserve the \
        \nright to proclaim that you've achieved the hardest 100% completion in all of Roblox."
}

BERD_SCALING = 2.5 # How much harder each difficulty is than the last (default: 2.5 → 2.5x per difficulty)
WEIGHT_SCALING = 0.95 # The factor by which pp is reduced, per rank (default: 0.95 → 5% reduction)
MAIN_PATH = "/".join(os.path.dirname(__file__).split("\\")) # Location of program folder


# ==================== Defining subprograms ==================== #


# Clears screen
def clear():
    os.system("cls")


# Extracts information about all towers from tower_info_full.txt and returns it
def get_towers():
    towers = []
    
    tower_info_file = open(f"{MAIN_PATH}/tower_info_full.txt","r",encoding="utf-8-sig")
    tower_info_list = [line for line in tower_info_file.read().replace("\ufeff","").split("\n") if "/" in line and "#" not in line]
    tower_info_file.close()
    
    for tower_info in tower_info_list:
        tower_info = tower_info.split("/")
        if len(tower_info) < 5:
            tower_info.append("0")
        name, abbr, diff, badge_id, badge_id_old = tower_info
        
        towers.append({"tower_name":name, "tower_abbr":abbr, "tower_diff":float(diff), "badge_id":int(badge_id), "badge_id_old":int(badge_id_old)})
    
    return towers


# Returns the userId of the given username
def get_user_id(username):
    # This part checks if the player's userId has previously been found, by checking user_id_list.txt which contains a list of every checked player and their userId
    user_id_file = open(f"{MAIN_PATH}/user_id_list.txt","r",encoding="utf-8-sig")
    user_id_cache = sorted(line for line in user_id_file.read().replace("\ufeff","").split("\n") if "/" in line and "#" not in line)
    user_id_file.close()

    for line in user_id_cache:
        name, user_id, displayname = line.split("/")
        if name == username.lower():
            return (int(user_id), displayname)


    url = f"https://users.roblox.com/v1/users/search?keyword={username.lower()}&limit=10"
    
    try:
        response = requests.get(url)
    except:
        clear()
        print("ERROR: Couldn't connect to the Roblox server. Please check your internet connection and try again.\n")
        return (None, None)
    
    if response.status_code != 200:
        clear()
        if response.status_code == 429:
            print(f"ERROR: Too many requests. Please wait a minute and try again.\n")
        else:
            print(f"ERROR: Couldn't reach server. Please wait and try again.\n")

        return (None, None)
    
    data = response.json()

    if any(ord(char) > 127 for char in data["data"][0]["displayName"]): # handles non-ascii characters
        data["data"][0]["displayName"] = data["data"][0]["name"]

    if data["data"][0]["name"].lower() == username.lower():
        user_id_file = open(f"{MAIN_PATH}/user_id_list.txt","a")
        user_id_file.write(f"\n{username.lower()}/{data['data'][0]['id']}/{data['data'][0]['displayName']}")
        user_id_file.close()
        return (data["data"][0]["id"], data["data"][0]["displayName"])

    else:
        clear()
        print("ERROR: Username does not exist.\n")
        return (None, None)


# Gets a list of the player's completions
def get_completions(user_id):
    towers_completed = []

    try:
        completions_file = open(f"{MAIN_PATH}/completions/{user_id}.txt", "r")
        completions = [line.strip().split("/") for line in completions_file.readlines() if line.strip() != "" and "/" in line]
        completions_file.close()
    except FileNotFoundError:
        completions = []

    for idx, data in enumerate(completions):
        name, abbr, diff, datetime = data

        is_canon = False # Ensures that removed towers are no longer used by the program

        for tower in towers:
            if tower["tower_name"] == name:
                diff = tower["tower_diff"] # Updates a completed tower's difficulty, in case the difficulty changed since last check
                is_canon = True
                break
        
        if not is_canon:
            continue

        year, month, day, hour, minute, second = datetime.split(",")
        date = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        datetime = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        if 1 <= float(diff) <= 14.99: # Ensures that the difficulty is valid
            towers_completed.append({"tower_name":name, "tower_abbr":abbr, "tower_diff":float(diff), "badge_id":0, "badge_id_old":0, "date_completed":date, "datetime_completed":datetime})


    towers_completed_names = [tower["tower_name"] for tower in towers_completed]

    
    old_tower_badge_ids = [tower["badge_id_old"] for tower in towers if tower["tower_name"] not in towers_completed_names and tower["badge_id_old"] != 0]
    loading_count = 0 # Purely for visual feedback

    # Old place badges
    for group in range((len(old_tower_badge_ids)-1)//100+1):

        url = f"https://badges.roblox.com/v1/users/{user_id}/badges/awarded-dates?badgeIds={','.join([str(badge_id) for badge_id in old_tower_badge_ids[group*100:(group+1)*100]])}"

        try:
            response = requests.get(url)
        except:
            clear()
            print("ERROR: Couldn't connect to the Roblox server. Please check your internet connection and try again.\n")
            return []
        
        clear()
        print(f"Getting {displayname}'s completions{'.' * (loading_count % 3 + 1)}\n")
        loading_count += 1

        if response.status_code != 200:
            clear()
            print("ERROR: Too many requests. Please wait a minute and try again.\n")
            return []
        
        data = response.json()

        for badge in data["data"]:
            for tower in towers:
                if badge["badgeId"] == tower["badge_id_old"]:
                    tower_completed = tower
                    break
            
            date_completed = badge["awardedDate"][:19].replace("T"," ")
            tower_completed["date_completed"] = date_completed
                
            datetime_completed = dt.datetime.strptime(date_completed, "%Y-%m-%d %H:%M:%S")
            tower_completed["datetime_completed"] = datetime_completed

            towers_completed.append(tower_completed)
            towers_completed_names.append(tower_completed["tower_name"])
    
    tower_badge_ids = [tower["badge_id"] for tower in towers if tower["tower_name"] not in towers_completed_names]

    # New place badges
    for group in range((len(tower_badge_ids)-1)//100+1):

        url = f"https://badges.roblox.com/v1/users/{user_id}/badges/awarded-dates?badgeIds={','.join([str(badge_id) for badge_id in tower_badge_ids[group*100:(group+1)*100]])}"
        
        try:
            response = requests.get(url)
        except:
            clear()
            print("ERROR: Couldn't connect to the Roblox server. Please check your internet connection and try again.\n")
            return []
        
        clear()
        print(f"Getting {displayname}'s completions{'.' * (loading_count % 3 + 1)}\n")
        loading_count += 1

        if response.status_code != 200:
            clear()
            print("ERROR: Too many requests. Please wait a minute and try again.\n")
            return []
        
        data = response.json()

        for badge in data["data"]:
            for tower in towers:
                if badge["badgeId"] == tower["badge_id"]:
                    tower_completed = tower
                    break
            
            date_completed = badge["awardedDate"][:19].replace("T"," ")
            tower_completed["date_completed"] = date_completed
                
            datetime_completed = dt.datetime.strptime(date_completed, "%Y-%m-%d %H:%M:%S")
            tower_completed["datetime_completed"] = datetime_completed

            towers_completed.append(tower_completed)


    # Writing tower completions to file
    completions_file = open(f"{MAIN_PATH}/completions/{user_id}.txt", "w")

    for tower in towers_completed:
        name = tower["tower_name"]
        abbr = tower["tower_abbr"]
        diff = tower["tower_diff"]
        datetime = tower["datetime_completed"]
        datetime = [datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute, datetime.second]

        data = "/".join([name, abbr, str(diff), ",".join([str(num).zfill(2) for num in datetime])])

        completions_file.write(f"{data}\n")
    
    completions_file.close()
    
    if len(towers_completed) == 0:
        clear()
        print(f"{displayname} has not beaten any towers.\n")
        return []


    return sorted(towers_completed, key=lambda tower:tower["date_completed"])


# Extracts the player's non-canon tower completions from their respective text file
def load_non_canon_completions():
    try:
        non_canon_file = open(f"{MAIN_PATH}/non_canon_completions/{user_id}.txt", "r")
        non_canon_completions = [line.strip().split("/") for line in non_canon_file.readlines() if line.strip() != "" and "/" in line]
        non_canon_file.close()
    except FileNotFoundError:
        return towers_completed

    for idx, data in enumerate(non_canon_completions):
        name, abbr, diff, datetime = data

        year, month, day, hour, minute, second = datetime.split(",")
        date = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        datetime = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        if 1 <= float(diff) <= 14.99: # Ensures that the difficulty is valid
            towers_completed.append({"tower_name":name, "tower_abbr":abbr, "tower_diff":float(diff), "badge_id":0, "badge_id_old":0, "date_completed":date, "datetime_completed":datetime})

    return towers_completed


# Displays a list of a player's completions sorted by an attribute
def display_sorted_completions(order):
    if order == "name":
        sorted_completions = sorted(towers_completed, key=lambda tower:tower["tower_name"])

    elif order == "abbr":
        sorted_completions = sorted(towers_completed, key=lambda tower:tower["tower_abbr"])

    elif order == "diff":
        sorted_completions = sorted(towers_completed, key=lambda tower:tower["tower_diff"])

    elif order == "date":
        sorted_completions = sorted(towers_completed, key=lambda tower:tower["date_completed"])

    else:
        print("ERROR: Invalid option.")
        return None

    print(f"========== List of towers beaten by {displayname} ==========\n")

    for tower in sorted_completions:
        name = tower["tower_name"]
        abbr = tower["tower_abbr"]
        diff = tower["tower_diff"]
        date = tower["date_completed"]
        
        diff_color = diff_colors[min(math.floor(diff) - 1, 13)]

        print(f"{fg(*diff_color)}{abbr} / {name} [{diff:.2f}] {fg(100,100,100)}({date[:10]}){rs.fg}")

        time.sleep(0.002)

    print("")


# info_mode 0: no info, 1: short tower names and pp, 2: long tower names and completion dates
def calculate_pp(towers_completed, info_mode=0):
    completions = sorted(towers_completed, key=lambda tower:tower["tower_diff"], reverse=True)
    total_pp = 0
    
    if info_mode == 0:
        for rank, tower in enumerate(completions):
            diff = tower["tower_diff"]
            
            berd = BERD_SCALING ** (diff - 1)
            weight = WEIGHT_SCALING ** rank
            pp = berd * weight
            total_pp += pp
        return total_pp
    

    print(f"========== {displayname}'s top completions ==========")

    if info_mode == 1:
        print(f"\nName [Difficulty] → pp amount {fg(100,100,100)}(BERD * weight){rs.fg}\n")
    elif info_mode == 2:
        print(f"\nShort / Full tower name [Difficulty]                         → pp amount {fg(100,100,100)}(BERD * weight) Completion date{rs.fg}\n")
    
    for rank, tower in enumerate(completions):
        name = tower["tower_name"]
        abbr = tower["tower_abbr"]
        diff = tower["tower_diff"]
        date = tower["date_completed"]
        
        berd = BERD_SCALING ** (diff - 1)
        weight = WEIGHT_SCALING ** rank
        pp = berd * weight
        total_pp += pp
        
        if rank < 100: # shows top 100 scores
            diff_color = diff_colors[min(math.floor(diff) - 1, 13)]
            
            if info_mode == 1:
                tail = f"→ {pp:,.2f}pp {fg(100,100,100)}({berd:.2f} * {weight:.0%}){rs.fg}"
                gap = " " * (14 - len(abbr) - len(f"{diff:.2f}"))
                print(f"{fg(*diff_color)}{abbr} [{diff:.2f}]{rs.fg} {gap}{tail}")

            elif info_mode == 2:
                tail = f"→ {pp:,.2f}pp {fg(100,100,100)}({berd:.2f} * {weight:.0%}) {date[:10]}{rs.fg}"
                gap = " " * (54 - len(abbr) - len(name) - len(f"{diff:.2f}"))
                print(f"{fg(*diff_color)}{abbr} / {name} [{diff:.2f}]{rs.fg} {gap}{tail}")
            
            time.sleep(0.005)
    
    diff_completions = [[math.floor(tower["tower_diff"]) for tower in towers_completed].count(i+1) for i in range(len(diff_names))]

    # The pp total's color found by finding the average BERD of the player's top 5 hardest towers, then taking the 2.5th log of this average
    # pp_color_data = [2.5 ** (tower["tower_diff"]) for tower in completions[:5]]
    # pp_color_data = math.log(sum(pp_color_data) / len(pp_color_data), 2.5)
    # pp_color = diff_colors[math.floor(pp_color_data) - 1]

    # The pp total's color is found by passing its value into this formula, and then selecting the corresponding difficulty color
    # The exact formula was found solely through testing and data, and may be inaccurate (does it really matter though?)
    pp_color_data = math.log(1 + total_pp / 5, 2.5)
    pp_color = diff_colors[min(math.floor(pp_color_data), 13)]

    print("")

    for idx, diff_name in enumerate(diff_names):
        if diff_completions[idx] > 0:
            diff_color = diff_colors[idx]
            print(f"{fg(*diff_color)}{diff_name} towers beaten: {diff_completions[idx]}{rs.fg}")
            time.sleep(0.005)
    
    print(f"\nTotal towers beaten: {len(towers_completed)}")

    print(f"\n{displayname} has a total of {fg(*pp_color)}{total_pp:,.2f}pp{rs.all}.\n")


# Returns a list of a player's pp on each day since their first completion, along with their hardest tower completion at the time
def calculate_history():
    pp_history = []
    completions = sorted(towers_completed, key=lambda tower:tower["datetime_completed"])
    date_check = completions[0]["datetime_completed"].replace(hour=0, minute=0, second=0)
    date_current = dt.datetime.now()

    completions_count = 0 # This variable is used to avoid recalculating pp if no towers have been beaten within a given day
    completion_difficulties = []

    tower_index = 0
    hardest = completions[0]

    while date_check < date_current:
        while tower_index < len(completions) and completions[tower_index]["datetime_completed"] < date_check + dt.timedelta(days=1):
            tower = completions[tower_index]
            bisect.insort(completion_difficulties, tower["tower_diff"])

            if tower["tower_diff"] > hardest["tower_diff"]:
                hardest = tower

            tower_index += 1
        
        if completions_count < tower_index:
            pp_then = 0

            for rank, diff in enumerate(completion_difficulties[::-1]):
                berd = BERD_SCALING ** (diff - 1)
                weight = WEIGHT_SCALING ** rank
                pp = berd * weight
                pp_then += pp

        completions_count = tower_index

        pp_history.append({"date":date_check, "pp":pp_then, "hardest":hardest})
        
        date_check = date_check + dt.timedelta(days=1)

    return pp_history


# Creates and displays a graph of a player's pp over time, including markers for when they beat a new hardest tower
def plot_history_graph(pp_history):
    xpoints = []
    ypoints = []

    pyplot.style.use("seaborn-v0_8")
    fig, graph = pyplot.subplots(facecolor="0.235")
    fig.canvas.manager.set_window_title(f"Graph of {displayname}'s pp history")
    
    graph.set_facecolor((194/255, 194/255, 204/255))
    graph.grid(color=(218/255, 218/255, 230/255))
    graph.set_title(f"{displayname}'s pp history", size="x-large", color="1")
    graph.set_xlabel("Date", size="large", color="1")
    graph.set_ylabel("Performance points", size="large", color="1")
    graph.tick_params(labelcolor=(218/255, 218/255, 230/255))

    for idx, data in enumerate(pp_history):
        date = data["date"]
        pp = data["pp"]
        hardest = data["hardest"]

        xpoints.append(date)
        ypoints.append(pp)

        if idx == 0 or hardest != pp_history[idx-1]["hardest"]: # adds star for new hardest
            diff_color = diff_colors[math.floor(hardest["tower_diff"]) - 1]
            diff_color_reg = tuple(val / 255 for val in diff_color)
            graph.plot(date, pp, marker="*", markersize=10, color=diff_color_reg, zorder=15)
            graph.text(date, pp, f"{hardest['tower_abbr']}  ", weight="bold", color=diff_color_reg, horizontalalignment="right", zorder=15)
            print(f"{fg(*diff_color)}{str(date)[:10]}: {pp:,.2f}pp * {hardest['tower_abbr']}{rs.fg}")

        elif pp != pp_history[idx-1]["pp"]: # adds point for change in pp
            graph.plot(date, pp, marker=".", markersize=8, color="C0", zorder=10)
            print(f"{fg(100,100,100)}{str(date)[:10]}: {pp:,.2f}pp{rs.fg}")
        
        elif idx != len(pp_history) - 1 and pp != pp_history[idx+1]["pp"]: # adds point before change in pp
            graph.plot(date, pp, marker=".", markersize=8, color="C0", zorder=10)
    
    graph.plot(xpoints, ypoints, linewidth=2, color="C0", zorder=5)

    print("\nHistory graph loaded!\n")
    pyplot.show()


# Checks which milestones have been achieved by a player
def check_milestones(pp_history):
    milestones = {milestone:False for milestone in [
        "50pp", "100pp", "200pp", "500pp", "1000pp", "2000pp", "5000pp", "10000pp", "20000pp", "50000pp", "100000pp",
        "1t", "10t", "20t", "50t", "100t", "200t", "300t",
        "all_non_sc", "all_sc", "all_towers"
    ]}

    for idx, data in enumerate(pp_history):
        date = data["date"] + dt.timedelta(days=1) - dt.timedelta(seconds=1)
        pp = data["pp"]
        hardest = data["hardest"]
        completions = [tower for tower in towers_completed if tower["datetime_completed"] < date]

        diff_completions = [[math.floor(tower["tower_diff"]) for tower in completions].count(i) for i in range(1,14)]

        for milestone in [50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]:
            if milestones[f"{milestone}pp"] == False and pp >= milestone:
                milestones[f"{milestone}pp"] = date

        for milestone in [1, 10, 20, 50, 100, 200, 300]:
            if milestones[f"{milestone}t"] == False and len(completions) >= milestone:
                milestones[f"{milestone}t"] = date

        if milestones["all_non_sc"] == False and sum(diff_completions[:7]) \
            == len([tower for tower in towers if tower["tower_diff"] < 8]):
            milestones["all_non_sc"] = date
        
        if milestones["all_sc"] == False and sum(diff_completions[7:]) \
            == len([tower for tower in towers if tower["tower_diff"] >= 8]):
            milestones["all_sc"] = date

        if milestones["all_towers"] == False and milestones["all_non_sc"] != False and milestones["all_sc"] != False:
            milestones["all_towers"] = date
    
    milestones_achieved = len([date for date in list(milestones.values()) if date != False])

    clear()
    print(f"========== {displayname}'s milestones ==========")

    for milestone, date in milestones.items():
        if date != False:
            print(f"\n{fg(0,255,0)}{milestone_descriptions[milestone]}{fg(100,100,100)}\n(achieved on {str(date)[:10]}){rs.fg}")
        else:
            print(f"\n{fg(64,48,48)}{milestone_descriptions[milestone]}{rs.fg}")
        
        time.sleep(0.005)

    print(f"\n{displayname} has achieved {milestones_achieved}/{len(milestones)} milestones.\n")


# Adds a non-canon tower to a player's completions
def add_non_canon_completion():
    name, abbr, diff = "", "", 0
    datetime = [-1, -1, -1, -1, -1, -1]

    try:
        non_canon_file = open(f"{MAIN_PATH}/non_canon_completions/{user_id}.txt", "r")
        non_canon_completions = [line.strip().split("/") for line in non_canon_file.readlines() if line.strip() != "" and "/" in line]
        non_canon_file.close()
    except FileNotFoundError:
        non_canon_completions = []

    names_list = [tower[0] for tower in non_canon_completions]

    clear()
    while len(name.strip()) == 0 or name in names_list:
        name = input("Enter the tower's name: ")
        if len(name.strip()) == 0:
            clear()
            print("ERROR: A name must be entered.\n")
        elif name in names_list:
            clear()
            print("ERROR: Tower completion has already been recorded.\n")
    
    abbr = "".join(word[0] for word in name.split() if word != "")

    clear()
    while diff < 1 or diff > 14.99:
        try:
            diff = float(input("Enter the tower's difficulty: "))
            if diff < 1 or diff > 14.99:
                clear()
                print("ERROR: Difficulty must be a value between 1 and 14.99.\n")
        except ValueError:
            clear()
            print("ERROR: Input must be a number.\n")
    
    clear()
    while datetime == [-1, -1, -1, -1, -1, -1]:
        for idx, time_unit in enumerate(["year", "month", "day", "hour", "minute", "second"]):
            while datetime[idx] == -1:
                try:
                    datetime[idx] = int(input(f"Enter {time_unit} of completion: "))
                except ValueError:
                    clear()
                    print("ERROR: Input must be an integer.\n")
            clear()

        try:
            datetime_test = dt.datetime(*datetime)
            if datetime_test < dt.datetime(2018, 1, 1, 0, 0, 0):
                print("ERROR: Date of completion cannot be before 2018.\n")
                datetime = [-1, -1, -1, -1, -1, -1]
        except:
            clear()
            print("ERROR: Date and time of completion invalid.\n")
            datetime = [-1, -1, -1, -1, -1, -1]
    
    data = "/".join([name, abbr, str(diff), ",".join([str(num).zfill(2) for num in datetime])])

    diff_color = diff_colors[min(math.floor(diff) - 1, 13)]
    
    clear()
    confirmation = input(f"{fg(*diff_color)}{abbr} / {name} [{diff:.2f}]{rs.fg} \
        \n\nType YES to add this to {displayname}'s non-canon tower completions: ").lower()

    clear()
    if confirmation == "yes":
        non_canon_file = open(f"{MAIN_PATH}/non_canon_completions/{user_id}.txt", "a")
        non_canon_file.write(f"{data}\n")
        non_canon_file.close()

        year, month, day, hour, minute, second = [str(num).zfill(2) for num in datetime]
        date = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        datetime = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        towers_completed.append({"tower_name":name, "tower_abbr":abbr, "tower_diff":float(diff), "badge_id":0, "badge_id_old":0, "date_completed":date, "datetime_completed":datetime})
        
        print(f"{fg(*diff_color)}{name}{rs.fg} has been added to {displayname}'s non-canon tower completions!\n")
    
    else:
        print(f"{fg(*diff_color)}{name}{rs.fg} has been discarded.\n")


# Removes a non-canon tower from a player's completions
def remove_non_canon_completion():
    try:
        non_canon_file = open(f"{MAIN_PATH}/non_canon_completions/{user_id}.txt", "r")
        non_canon_completions = [line.strip().split("/") for line in non_canon_file.readlines() if line.strip() != "" and "/" in line]
        non_canon_file.close()
    except FileNotFoundError:
        clear()
        print(f"{displayname} does not have any recorded non-canon tower completions.\n")
        return None
    
    if len(non_canon_completions) == 0:
        clear()
        print(f"{displayname} does not have any recorded non-canon tower completions.\n")
        return None

    non_canon_completions = sorted(non_canon_completions, key=lambda tower:tower[3])

    for idx, data in enumerate(non_canon_completions):
        name, abbr, diff, datetime = data

        year, month, day, hour, minute, second = datetime.split(",")
        date = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        datetime = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

        non_canon_completions[idx] = {"tower_name":name, "tower_abbr":abbr, "tower_diff":float(diff), "badge_id":0, "badge_id_old":0, "date_completed":date, "datetime_completed":datetime}

    names_list = [tower["tower_name"].lower() for tower in non_canon_completions]
    selection = " "

    clear()
    while selection != "" and selection not in names_list:
        print(f"========== {displayname}'s non-canon completions ==========\n")

        for tower in non_canon_completions:
            name = tower["tower_name"]
            abbr = tower["tower_abbr"]
            diff = tower["tower_diff"]
            date = tower["date_completed"]
            
            diff_color = diff_colors[min(math.floor(diff) - 1, 13)]

            print(f"{fg(*diff_color)}{abbr} / {name} [{diff:.2f}] {fg(100,100,100)}({date[:10]}){rs.fg}")
        
        print("")
        
        selection = input(f"Enter the name of the tower, or press ENTER to return: ").lower()
        if selection != "" and selection not in names_list:
            clear()
            print("ERROR: Tower not in list of non-canon completions.\n")
        
    if selection == "":
        clear()
        return None
    
    tower_removed = non_canon_completions[names_list.index(selection)]

    name = tower_removed["tower_name"]
    abbr = tower_removed["tower_abbr"]
    diff = tower_removed["tower_diff"]
    date = tower_removed["date_completed"]
    
    diff_color = diff_colors[min(math.floor(diff) - 1, 13)]

    removal_message = f"{fg(*diff_color)}{name}{rs.fg} has been removed from {displayname}'s non-canon tower completions.\n"

    clear()
    confirmation = input(f"{fg(*diff_color)}{abbr} / {name} [{diff:.2f}]{rs.fg} \
        \n\nType YES to remove this from {displayname}'s non-canon tower completions: ").lower()

    if confirmation != "yes":
        clear()
        print(f"{fg(*diff_color)}{name}{rs.fg} will not be removed.\n")
        return None
    
    non_canon_file = open(f"{MAIN_PATH}/non_canon_completions/{user_id}.txt", "w")
    data = ""
    file_empty = True

    for tower in non_canon_completions:
        name = tower["tower_name"]
        abbr = tower["tower_abbr"]
        diff = tower["tower_diff"]
        datetime = tower["datetime_completed"]
        datetime = [datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute, datetime.second]

        data = "/".join([name, abbr, str(diff), ",".join([str(num).zfill(2) for num in datetime])])

        if name.lower() != selection:
            non_canon_file.write(f"{data}\n")
            file_empty = False
    
    non_canon_file.close()

    if file_empty: # Checks to see if nothing has been written to the player's file, i.e. they do not have any non-canon tower completions
        os.remove(f"{MAIN_PATH}/non_canon_completions/{user_id}.txt") # May not work on all computers

    global towers_completed
    towers_completed = [tower for tower in towers_completed if tower["tower_name"] != tower_removed["tower_name"] or tower["badge_id"] != 0]

    clear()
    print(removal_message)


# Displays info about how the program works
def display_info():
    clear()
    print(f"========== Information about the pp system ========== \
        \n\nBaseline Easy Relative Difficulty, or BERD, is a measure of how difficult a tower is. For \
        \nsimplicity's sake, every difficulty is considered to be 2.5x as hard as the last. \
        \n\nFor example, {fg(*diff_colors[2])}ToH{rs.fg}, a {fg(*diff_colors[2])}Mid Hard{rs.fg} tower with a difficulty of 3.42, has a BERD of 9.18, whereas {fg(*diff_colors[5])}CoLS{rs.fg}, a \
        \n{fg(*diff_colors[5])}Low-Mid Intense{rs.fg} citadel with a difficulty of 6.5, has a BERD of 154.41. From this, we can say that \
        \n{fg(*diff_colors[5])}CoLS{rs.fg} is around 16.8x harder than {fg(*diff_colors[2])}ToH{rs.fg}. \
        \n\nWith {fg(*diff_colors[12])}Peak Unreal (13.99){rs.fg} being the highest humanly possible difficulty, the hardest possible tower \
        \nwould have a BERD of 147,652.47, meaning it would be considered around 1,000x harder than {fg(*diff_colors[5])}CoLS{rs.fg}. \
        \n\nThe performance points system calculates the BERD of each completed tower, then calculates the \
        \nweighted sum, where towers are ranked in order of difficulty and each tower awards 5% less pp than \
        \nthe one above it. This would mean that a completion of {fg(*diff_colors[12])}ToTDTHL{rs.fg} would award 147,652.47pp \
        \nby itself, while a {fg(*diff_colors[5])}CoLS{rs.fg} completion would reward 154.41pp if it were a user's hardest completed \
        \ntower. However, if {fg(*diff_colors[5])}CoLS{rs.fg} were instead the player's 10th hardest tower, i.e. they would have beaten \
        \nnine towers harder than {fg(*diff_colors[5])}CoLS{rs.fg}, then it would only award 97.32pp. This is because towers have a \
        \nlesser impact on a player's skill if the player is able to easily beat said towers. \
        \n\nThis program uses the Roblox Badges API to get a list of all EToH badges owned by a select player, \
        \nand then generates a list of towers beaten by that player, which is used to calculate the user's \
        \nperformance points and create a graph of their pp over time. \
        \n\nDon't be demotivated if your pp total is barely increasing! The main factor that decides your pp \
        \nis the limit of your skill, i.e. beating hard towers that push you to the limit. Expect your pp to \
        \nincrease very slightly when beating towers multiple difficulties below your hardest. Spending lots \
        \nof time playing does not directly translate to a much higher pp total. Also, the aforementioned \
        \nBERD and pp values may not be entirely up to date. \
        \n\n\n{fg(255,255,200)}Thank you so much for using this program!{rs.fg} I would also like to thank the people behind {fg(220,45,45)}jtoh.pro{rs.fg}, \
        \n{fg(77,92,191)}towerstats.com{rs.fg}, {fg(255,102,170)}osu!{rs.fg}, {fg(254,223,21)}Score{fg(233,189,32)}Saber{rs.fg} and {fg(150,29,144)}Beat{fg(119,31,157)}Leader{rs.fg} for inspiring me to make this program and for \
        \nkeeping me motivated. \
        \n\n- Sam\n\n")


# ==================== Main program ==================== #


running = True

towers = get_towers()

print("========== List of towers ==========\n")

for tower in towers:
    name = tower["tower_name"]
    abbr = tower["tower_abbr"]
    diff = tower["tower_diff"]

    diff_color = diff_colors[min(math.floor(diff) - 1, 13)]
    print(f"{fg(*diff_color)}{abbr} / {name} [{diff:.2f}]{rs.fg}")

print(f"\nTotal number of towers: {len(towers)}\n")


while running:
    user_id = None
    
    while user_id == None:
        username = input("Enter the player's username: ")
        user_id, displayname = get_user_id(username)
    
    clear()
    print(f"Getting {displayname}'s completions...\n")
    
    towers_completed = get_completions(user_id)

    if len(towers_completed) == 0:
        continue

    towers_completed = load_non_canon_completions()
    
    clear()
    print(f"Completed towers loaded!\n")
    
    display_sorted_completions("date")
    
    menu_option = " "
    
    while menu_option not in ["0", ""] and len(towers_completed) > 0:
        menu_option = input("Please select an option: \
            \n\n[1] View pp and top completions \
            \n[2] View pp with more details \
            \n[3] View pp history and graph \
            \n[4] View sorted completions list \
            \n[5] View player milestones \
            \n[6] Modify non-canon tower completions \
            \n[7] Show info about pp system \
            \n[0] Check another player \
            \n\nOr press ENTER to quit. \
            \n> ")
        
        clear()

        if menu_option == "1":
            calculate_pp(towers_completed, 1)
        
        elif menu_option == "2":
            calculate_pp(towers_completed, 2)
        
        elif menu_option == "3":
            pp_history = calculate_history()
            plot_history_graph(pp_history)
        
        elif menu_option == "4":
            clear()
            sub_option = " "
            while sub_option not in ["name", "diff", "date", ""]:
                sub_option = input("What would you like to sort by? \
                    \n\n[name] Tower name \
                    \n[diff] Tower difficulty \
                    \n[date] Date of completion \
                    \n\nOr press ENTER to go back. \
                    \n> ")

                if sub_option not in ["name", "diff", "date", ""]:
                    clear()
                    print("Invalid option.\n")
                    
            clear()
            if sub_option != "":
                display_sorted_completions(sub_option)

        elif menu_option == "5":
            pp_history = calculate_history()
            check_milestones(pp_history)

        elif menu_option == "6":
            clear()
            sub_option = " "
            while sub_option not in ["add", "remove", ""]:
                sub_option = input("What would you like to do? \
                    \n\n[add] Add a non-canon tower completion \
                    \n[remove] Remove a non-canon tower completion \
                    \n\nOr press ENTER to go back. \
                    \n> ")

                if sub_option not in ["add", "remove", ""]:
                    clear()
                    print("Invalid option.\n")
            
            clear()

            if sub_option == "add":
                add_non_canon_completion()
            
            elif sub_option == "remove":
                remove_non_canon_completion()
        
        elif menu_option == "7":
            display_info()

        elif menu_option not in ["0", ""]:
            print("Invalid option.\n")
    
    if menu_option == "":
        running = False