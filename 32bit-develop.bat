conda config --env --set subdir win-32
conda infoconda create -n pykiwoom_32 python=3.8 conda activate pykiwoom_32 conda config --env --set subdir win-32 conda install python=3.8
python
import platform print(platform.architecture())
exit()
