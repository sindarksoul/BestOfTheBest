# 🥇 Best Of The Best (BOTB)

BOTB is a high-performance automation tool for power users, red teamers, and analysts.  
It seamlessly handles folder renaming, Base64 decoding, credential extraction, and log generation — all in one go.

---

## 🚀 Features

- ✅ Smart folder renaming (preserves nested structure)
- 🔐 Auto-extracts and compiles credentials from `.txt` files
- 🧪 Executes post-extraction automation (`dline.py`)
- 📝 Generates logs: `debug.txt`, `jobdone.txt`, `compilation.txt`
- 🔁 Step-by-step, auto-synchronized process (no overlaps or skips)
- ⚡ Progress tracker with visible numbered steps
- 🧠 Handles large datasets (tested with **150GB**+)

---

## 🛠 How It Works

1. **User inputs a target folder path** (prompted on launch)
2. BOTB:
   - Renames all folders/subfolders
   - Decodes Base64 files
   - Extracts and compiles credentials from valid `.txt` files
   - Deletes unneeded `.txt` files from root
3. Runs `dline.py` for post-processing
4. Writes all logs to designated files
5. Exits cleanly once all tasks are done

---

## 🖥️ How to Use

### 🔹 Option 1: Run the Precompiled `.exe`

1. Download the latest release from the [Releases](https://github.com/sindarksoul/BestOfTheBest/releases) page.
2. Extract the `.zip` file.
3. Double-click `BOTB.exe` **or** run via terminal:

```bash
BOTB.exe


