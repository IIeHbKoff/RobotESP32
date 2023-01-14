ampy rm config.py
ampy rm main.py
ampy rm boot.py
ampy rmdir libs
ampy rmdir networking
ampy rmdir skills
ampy rmdir common_files

ampy put config.py
ampy put main.py
ampy put boot.py
ampy put libs
ampy put networking
ampy put skills
ampy mkdir common_files
ampy put ../RobotCommonFiles common_files
