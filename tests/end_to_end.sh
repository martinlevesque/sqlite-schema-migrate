set -e

export BASE_CMD="python __main__.py"

for script in tests/end_to_end_scenarios/*.sh; do
    echo ""
    echo "###"
    echo "# Running test $script"
    echo "###"
    echo ""
    bash $script
done