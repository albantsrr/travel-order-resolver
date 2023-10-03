[Version]
Python : 3.10.11

[Execute]
python generation.py [-h] [--csv CSV] [--name NAME] [--gen GEN] [--nb NB]

[Option]
-h, --help   show this help message and exit
  --csv CSV    0 : disabled | 1 : enabled
  --name NAME  csv name
  --gen GEN    0 : all | 1 : sentence_1 | 2 : sentence_2 | 3 : sentence_3
  --nb NB      setence number

[Example]
(win) %PATH_PYTHON% .\generation.py --csv 1 --name dataSet --gen 0 --nb 300