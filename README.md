# etoh-pp
A Python program that let's you see the skill level of any EToH player, including you and your friends, by assigning them a pp score (performance points) based on the towers they've beaten. Inspired by osu! and ScoreSaber's own pp systems.

YOU NEED TO INSTALL FOLLOWING PYTHON LIBRARIES TO RUN THE PROGRAM:
requests, datetime, matplotlib, sty

*The method:*

• First, a player's username is taken and a list of the towers they have beaten is obtained, by using the Roblox Badges API.

• Since every tower difficulty is around 2.5x harder than the last, we can calculate the relative difficulty of a certain tower compared to a Baseline Easy (1.00) tower.

• This Baseline Easy Relative Difficulty, or BERD, is calculated for every tower a player has beaten, using the formula `2.5 ^ (diff - 1)`, where `diff` is the difficulty of a certain tower.

• Towers are then sorted by difficulty (hardest first), and each tower is then weighted relative to its rank. Weighting is done by multiplying every tower's BERD by `0.95 ^ (rank - 1)`, where a player's hardest completion has rank 1, their second hardest is rank 2, and so on. This leaves us with the pp scores awarded by each tower.

• Finally, the pp scores of all completed towers are added up, giving the total pp score of the player.

This is really similar to what the ranking systems of osu! and Beat Saber do, and now I've made the equivalent for EToH.
The program also allows you to see a graph of anyone's pp history, so you can see how they've improved over time, including when they've beaten a new hardest tower!

dm me on discord @sirsamiboi if there are any incorrect difficulties!
