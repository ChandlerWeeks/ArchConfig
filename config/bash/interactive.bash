# Shared interactive-shell extras. Sourced from ~/.bashrc by install.py.
# Show once per terminal session, including new Kitty tabs, not nested shells.
if [[ $- == *i* && -t 0 && -t 1 && ${TERM:-dumb} != dumb ]] && command -v fastfetch >/dev/null 2>&1; then
    _desktop_terminal_session="${KITTY_PID:-terminal}:$(tty)"
    if [[ ${DOTFILES_FETCH_SESSION:-} != "$_desktop_terminal_session" ]]; then
        export DOTFILES_FETCH_SESSION="$_desktop_terminal_session"
        fastfetch
    fi
    unset _desktop_terminal_session
fi
