# DANCER

# Trial NCF Commands
$ cd examples

python3 run_exp.py --task TART --mode NCF --setting naive --lr 1e-2 --reg 1e-4 <br />
python3 run_exp.py --task TART --mode NCF --setting naive --lr 1e-2 --reg 1e-4 <br />
python3 run_exp.py --task TART --mode NCF --setting StaticIps --lr 1e-2 --reg 1.0 <br />
python3 run_exp.py --task TART --mode NCF --setting StaticIps --lr 1e-3 --reg 1e-1 <br />
python3 run_exp.py --task TART --mode NCF --setting DANCER --lr 1e-4 --reg 1e-3 <br />
python3 run_exp.py --task TART --mode NCF --setting DANCER --lr 1e-4 --reg 1e-3 <br />


# Original RQ3 Commands
cd examples

python run_exp.py --task TART --mode MF_v --setting naive --lr 1e-2 --reg 1e-4 <br />
python run_exp.py --task TART --mode TMF_v --setting naive --lr 1e-2 --reg 1e-4 <br />
python run_exp.py --task TART --mode MF_v --setting StaticIps --lr 1e-2 --reg 1.0 <br />
python run_exp.py --task TART --mode TMF_v --setting StaticIps --lr 1e-3 --reg 1e-1 <br />
python run_exp.py --task TART --mode MF_v --setting DANCER --lr 1e-4 --reg 1e-3 <br />
python run_exp.py --task TART --mode TMF_v --setting DANCER --lr 1e-4 --reg 1e-3 <br />
