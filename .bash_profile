gc() {
    python ~/development/scripts/git_clone.py git@github.com https://api.github.com xxx username && cd $(ls -t | head -1)
}
export -f gc
# ================================
git() {
    if [[ "$1" == "log" && "$@" != *"--help"* ]]; then
        shift 1
        command git l "$@"
    else
        command git "$@"
    fi
}
export -f git
