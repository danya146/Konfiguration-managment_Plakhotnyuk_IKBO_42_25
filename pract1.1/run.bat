@echo off
start "" pythonw -m src.main --vfs ./vfs --log ./logs/log.json --script ./configs/test_script.txt
exit