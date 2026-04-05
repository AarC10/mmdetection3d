_base_ = ['../pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py']

fp16 = dict(loss_scale=512.0)