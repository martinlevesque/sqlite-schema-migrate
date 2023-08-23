cd src
export BASE_CMD="python main.py"

for script in ../tests/end_to_end_scenarios/*.sh; do
    echo ""
    echo "###"
    echo "# Running test $script"
    echo "###"
    echo ""
    bash $script
done