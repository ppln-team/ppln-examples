experiment_name = 'ResNet18'

# model settings
model = dict(type='torchvision.models.resnet18', pretrained=True)

# transform settings
pre_transforms = [
    dict(type='LongestMaxSize', max_size=64),
    dict(type='PadIfNeeded', min_height=64, min_width=64),
]
post_transforms = [dict(type='Normalize'), dict(type='ToTensor')]
augmentations = [
    dict(type='HorizontalFlip'),
    dict(type='ShiftScaleRotate', shift_limit=0.11, scale_limit=0.13, rotate_limit=7)
]
transforms = dict(
    train=pre_transforms + augmentations + post_transforms,
    val=pre_transforms + post_transforms,
    test=pre_transforms + post_transforms
)

# dataset settings
data = dict(
    data_root='/data/cifar10',
    images_per_gpu=128,  # images per gpu
    workers_per_gpu=4,  # data workers per gpu
    pin_memory=False
)

# ddp settings
dist_params = dict(backend='nccl')

# optimizer and learning rate
optimizer = dict(type='torch.optim.Adam', lr=3e-4)
scheduler = dict(type='torch.optim.lr_scheduler.ReduceLROnPlateau', factor=0.1, mode='min', patience=0)

# runtime settings
work_dir = f'/data/dumps/{experiment_name}'
max_epochs = 20

# hook settings
hooks = [
    dict(type='ProgressBarLoggerHook', bar_width=10),
    dict(type='TextLoggerHook'),
    dict(type='TensorboardLoggerHook', log_dir=f'/data/dumps/{experiment_name}'),
    dict(type='CheckpointHook', num_checkpoints=5, metric_name='acc_top1', mode='max'),
    dict(type='LRSchedulerHook', metric_name='base_loss', by_epoch=True),
    dict(type='ApexInitializeHook', opt_level='O1', loss_scale=128.0),
    dict(type='ApexOptimizerHook', max_norm=1),
    dict(type='ApexSyncBNHook'),
    dict(type='ApexDDPHook', delay_allreduce=True),
    dict(type='EarlyStoppingHook', metric_name='base_loss', patience=10, verbose=True, mode='min')
]
