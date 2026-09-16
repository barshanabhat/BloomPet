# 🌸 BloomPet

BloomPet is a lightweight Windows desktop virtual pet built with Python and PySide6.

It runs quietly in the background and appears as a cute desktop companion to remind the user to drink water at regular intervals.

The main reminder message is:

> **“Despite it all, she still blooms. 🌸”**

The goal of BloomPet is to make simple productivity and wellness reminders feel more friendly and personal than a normal Windows notification.

---

## ✨ Features

BloomPet currently includes:

- 🐾 Cute desktop virtual pet
- 💧 Water reminder every 30 minutes
- ⏱️ Reminder remains visible for 60 seconds
- 🎈 Gentle floating / bouncing animation
- 💬 Custom speech bubble reminder
- 🪟 Transparent frameless window
- 📌 Always-on-top desktop companion
- 🖥️ Runs quietly in the Windows system tray
- ▶️ Show Pet manually from the tray
- ⏸️ Pause reminders
- ▶️ Resume reminders
- 🔄 Restart the reminder timer
- 🚀 Optional Start with Windows support
- 🛡️ Prevents multiple copies of BloomPet from running at the same time
- 📦 Can be packaged into a standalone Windows `.exe`
- 🧪 Includes a test mode for faster development

---

## 🖼️ How BloomPet Works

When BloomPet starts, it runs quietly in the background.

In normal mode:

1. BloomPet starts in the Windows system tray.
2. A timer begins running.
3. After 30 minutes, the virtual pet appears on the desktop.
4. The pet displays the message:

   **💧 Drink some water!**

   **Despite it all, she still blooms. 🌸**

5. The pet stays visible for 60 seconds.
6. The pet automatically disappears.
7. The 30-minute reminder cycle continues.

The user can also manually show the pet at any time from the system tray.

---

## 🖥️ System Tray Controls

Right-clicking the BloomPet icon in the Windows system tray provides several controls.

### Show Pet

Immediately displays the pet and reminder without waiting for the next scheduled reminder.

### Pause Reminders

Stops the automatic reminder timer.

BloomPet will remain running in the background, but reminders will not appear automatically.

### Resume Reminders

Starts the reminder timer again after it has been paused.

### Restart Timer

Resets the reminder timer.

For example, if the reminder is scheduled every 30 minutes and you restart the timer, BloomPet will begin counting another 30 minutes from that moment.

### Start with Windows

Allows BloomPet to automatically launch when the user signs into Windows.

This feature uses the Windows Registry:

```text
HKEY_CURRENT_USER
Software
Microsoft
Windows
CurrentVersion
Run