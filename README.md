# ArchConfig · Catppuccin Mocha

My Arch Linux / Hyprland desktop, using Catppuccin Mocha with mauve accents,
small rounded corners, and the Adwaita cursor.

The repository keeps XDG configs in `config/`, executable helpers in `bin/`,
and monitor/GPU choices in `hosts/`. Installed configs link back to this checkout,
so editing a live config is also editing the versioned source.

## Layout

```text
config/                 Hyprland, Kitty, Waybar, Rofi, GTK/Qt, SwayNC, user services
bin/                    Clipboard picker, dropdowns, workspace and display controls
hosts/generic/          Automatic monitors, no GPU assumptions
hosts/chandler-workstation/  Personal monitor layout and NVIDIA settings
scripts/                Theme setup and installation rollback
install.py              Installer with backups and a dry-run mode
packages.txt            Official Arch dependencies
```

Clipboard contents, app accounts, cookies, Wi-Fi credentials, binary dconf state,
and machine-local overrides are not part of this repository.

## Installation

Clone into a permanent location; the links depend on this checkout staying there.

```sh
git clone https://github.com/ChandlerWeeks/ArchConfig.git ~/dotfiles
cd ~/dotfiles
```

Review `packages.txt` and install the listed packages using your package manager.
The Kvantum Mocha theme is also required: `kvantum-theme-catppuccin-git` from the
AUR provides the configured theme. `papirus-folders-catppuccin-git` is optional
for matching mauve folder icons. The GTK asset installer downloads the pinned
Catppuccin v1.0.3 theme from its official release; it does not run downloaded code.

```sh
./scripts/install-themes
python3 install.py --dry-run --host generic
python3 install.py --host generic
./scripts/apply-theme
```

On my workstation, use `--host chandler-workstation` instead. Installation writes
the selected host file to ignored `config/hypr/local.conf`. Adjust that file for
unshared local changes, or add another directory under `hosts/`. Subsequent
`python3 install.py` runs preserve the selected local configuration.

Log into Hyprland, or apply changes in the current session:

```sh
systemctl --user daemon-reload
~/.local/bin/desktop-startup
hyprctl reload
```

The startup helper imports Wayland variables before starting user services.
There is no requirement to use UWSM. App launch shortcuts assume Dolphin,
Flatpak Zen, Discord, Steam, VS Code, Slack, and Prism Launcher; change those
bindings to fit the apps installed on another machine.

## Shortcuts

| Shortcut | Action |
| --- | --- |
| Super + Enter | Kitty |
| Super + R | Rofi app launcher |
| Super + Left / Right | Cycle all workspaces on the current monitor, including empty ones |
| Super + H / J / K / L | Focus windows left / down / up / right |
| Super + Shift + H / L | Move a window between this workstation's monitors |
| Super + Shift + V | Search clipboard history |
| Super + N | Notification center |
| Super + Shift + N | Do Not Disturb |
| Super + Shift + B | Toggle warm display lighting |
| Super + Escape | Lock screen |
| Super + S | Screenshot region |
| Super + Shift + S | Screenshot region to clipboard |

Both physical Alt keys act as Ctrl; both physical Ctrl keys act as Alt.
In Kitty, **physical Alt + T / W** opens / closes a tab, and **physical Alt +
Left / H / K** or **Right / J / L** switches tabs. Kitty uses 92% background
opacity. New Kitty processes are required when enabling dynamic opacity for
the first time.

## Clipboard history

Two user services capture copied text and images with `wl-paste` and `cliphist`.
The picker uses the same Mocha Rofi theme as the app launcher.

- Enter: copy the selected item back to the clipboard, then paste normally.
- Delete: remove the selected history entry.
- Shift + Delete: clear history after confirmation.

History is capped at 500 entries. The database stays in the user's cache directory
and is not versioned. `systemctl --user stop cliphist-text cliphist-image` pauses
capture; `cliphist wipe` clears stored entries.

## Warm displays

The schedule in `config/hypr/hyprsunset.conf` uses the system's local timezone:

| Time | Temperature |
| --- | --- |
| 07:00 | 5000K |
| 18:00 | 4000K |
| 21:00 | 3500K, continuing overnight |

Click the moon/sun in the bar or press Super + Shift + B to toggle the filter.
Right-click the icon to restore the current scheduled profile. To change the
schedule, edit the config and run `systemctl --user restart hyprsunset`.

## Notification center and desktop controls

Click the bell for grouped notification history, Clear all, and Do Not Disturb.
Sound, microphone, Wi-Fi, Bluetooth, and calendar dropdowns are separate bar
controls. Gmail, Outlook, and Slack must have their own desktop notifications
enabled; mail sites also need notification permission in Zen.

## Updating and restoring

After editing a config, inspect and commit it:

```sh
cd ~/dotfiles
git diff
git add config bin hosts scripts README.md install.py packages.txt .gitignore .editorconfig
git commit -m "Describe the desktop change"
```

Keep the Git remote as desired and push explicitly when ready to publish.
The installer saves replaced files and a JSON manifest under
`~/.local/state/dotfiles-backups/<timestamp>/`. Undo one installation with:

```sh
python3 scripts/restore.py ~/.local/state/dotfiles-backups/<timestamp>/manifest.json --dry-run
python3 scripts/restore.py ~/.local/state/dotfiles-backups/<timestamp>/manifest.json
```

Rollback only replaces links that still point to this checkout; it preserves
files changed independently after installation. Reload the affected apps after
restoring. The previous `~/.config/sysconfig` checkout is retained as a migration
backup, including its original uncommitted changes and local runtime state.

## Credits

- [Catppuccin](https://github.com/catppuccin) for the palette and GTK / Kvantum themes.
- [Hyprland](https://hypr.land), [Waybar](https://github.com/Alexays/Waybar),
  [SwayNotificationCenter](https://github.com/ErikReider/SwayNotificationCenter),
  [cliphist](https://github.com/sentriz/cliphist), and
  [hyprsunset](https://github.com/hyprwm/hyprsunset).

The contour wallpaper is generated from the included SVG. Theme assets installed
outside this checkout retain their upstream licenses.
