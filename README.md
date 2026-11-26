# Mysterious Hearts

Mysterious Hearts is a desktop RPG I'm making about the people who live in Winterfield. Pick someone to play as and you'll get their phone, their contacts, and their history with the people around them. Playing as Rei means digging into what happened to Marcus. Playing as Garrett means looking for Charles. You can also leave the investigation for tomorrow and see who's at the chess café.

## Getting started on Windows

Install Python 3.12 or newer with Tk support. From the game folder, run these commands.

~~~powershell
python -m pip install -r requirements.txt
python game.py
~~~

After that, you can double-click **Launch Mysterious Hearts.cmd**. Pick **New story** to choose your character, or open **Saved stories & backups** to get back to an existing playthrough.

I use a local model for conversations. Load Qwen 3.5 9B Abliterated in Locally Uncensored, start its Local API on port 8129, then open **AI & account** in the game to enter your LU token and select the model. If you prefer to use your ChatGPT account, the setup guide covers the optional Node.js sign-in bridge and how plan usage works. [Local AI setup](DEVELOPMENT_HISTORY.md#local-ai-setup) · [ChatGPT setup](DEVELOPMENT_HISTORY.md#chatgpt-sign-in-option)

## What to try first

- **Text someone you know.** Open Messages and write what you want to say. If you're stuck, **Suggest replies** gives you four options. Each relationship keeps its own conversation history.
- **Meet up in town.** Check the map to see who's around, then use the in-person window when you arrive. At the chess café, head to the Playing room for a game. Come back later and you can look up what happened the last time you played that opponent, right down to the pieces you both captured.
- **Start Rei's investigation.** Play as Rei and open **In person → Stories, guards & gang properties → Rei's story**. Follow the records, talk to the people at Kurose House, and decide what Rei should do about the Hamayashi-kai.

I play with voice recordings for Rei and Fox on my own machine. The GitHub build shows their dialogue as text while I check whether I can share the recordings.

Your active story autosaves as you play. I keep each playthrough's backups under `saves/stories/` so you can start another character and come back to the first one later.

## Following the project

I keep the player-facing changes in the [patch notes](patch_notes/PATCH_NOTES.md). I've also kept the [project roadmap](ROADMAP.md) here if you're interested in how I planned the updates. For the longer feature write-ups, controls, and setup details from earlier builds, see the [development history](DEVELOPMENT_HISTORY.md).
