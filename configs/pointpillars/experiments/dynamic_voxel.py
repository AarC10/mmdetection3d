_base_ = ['../pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py']

# arxiv.org/abs/1910.06528

# Pointpillars paper specifies .16 xy resolution
# See pointpillars_hv_secfpn_kitti.py middle_encoder has 432 x 496
# 432 * .16 = 69.12
# 496 * .16 = 79.36

voxel_encoder=dict(
    type='DynamicPillarFeatureNet',
    in_channels=4,
    feat_channels=[64],
    voxel_size=[0.16, 0.16, 4],
    point_cloud_range=[0, -39.68, -3, 69.12, 39.68, 1],
)

data_preprocessor=dict(
    type='Det3DDataPreprocessor',
    voxel=True,
    voxel_type='dynamic',
    voxel_layer=dict(
        max_num_points=-1,
        max_voxels=-1,
        voxel_size=[0.16, 0.16, 4],
        point_cloud_range=[0, -39.68, -3, 69.12, 39.68, 1],
    )
)