# etoh-pp
A Python program that let's you see the skill level of any EToH player, including you and your friends, by assigning them performance points (or pp) based on the towers they've beaten. Inspired by osu! and ScoreSaber's own pp systems.

## Installation

To get started you will need to do the following:

1) Install Python if you have not already. Official downloads can be found at https://www.python.org/downloads/
2) Download the [latest release](https://github.com/SirSamiboi/etoh-pp/releases/latest). If you are unsure which file to download, choose `Source code (zip)`.
3) Unzip the file, then open the unziped folder in a terminal of your choosing. Note: Make sure you are in the correct directory. You can run `ls` to verify that you have `etoh_pp_system.py` listed as one of the files.
4) Now you'll want to install the needed dependencies, run `pip install -r requirements.txt` OR `py -m pip install -r requirements.txt`. If one of these doesn't work, try the other.
5) To start the program, run `py etoh_pp_system.py`! You can also double-click the `etoh_pp_system.py` file in the program folder. From there, follow the text prompts.
6) You can create a desktop shortcut of `etoh_pp_system.py` for easier access. By right-clicking the shortcut, then selecting Properties → Change Icon, you can go to the program folder and use the `icon` file as the shortcut's icon.

## How does it work?

• First, a player's username is taken and a list of the towers they have beaten is obtained, by using the Roblox Badges API.

• By considering every tower difficulty to be around 2.5x harder than the last, we can calculate the relative difficulty of a certain tower compared to a Baseline Easy (1.00) tower.

• This Baseline Easy Relative Difficulty, or BERD, is calculated for every tower a player has beaten, using the formula `2.5 ^ (diff - 1)`, where `diff` is the difficulty of a certain tower.

• Towers are then sorted by difficulty (hardest first), and each tower is then weighted relative to its rank. Weighting is done by multiplying every tower's BERD by `0.95 ^ (rank - 1)`, where a player's hardest completion has rank 1, their second hardest is rank 2, and so on. This leaves us with the pefromance points awarded by each tower.

• Finally, the pp of all completed towers are added up, giving the total pp of the player.

This is very similar to what the ranking systems of osu! and Beat Saber do, and now I've made the equivalent for EToH.
The program also allows you to see a graph of anyone's pp history, so you can see how they've improved over time, including when they've beaten a new hardest tower!

DM me on discord @sirsamiboi if there are any incorrect difficulties. Thank you for using my program :)
