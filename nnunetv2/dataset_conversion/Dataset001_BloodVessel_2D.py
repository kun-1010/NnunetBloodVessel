import multiprocessing
import shutil
from multiprocessing import Pool

from batchgenerators.utilities.file_and_folder_operations import *

from nnunetv2.dataset_conversion.generate_dataset_json import generate_dataset_json
from nnunetv2.paths import nnUNet_raw
from skimage import io
from acvl_utils.morphology.morphology_helper import generic_filter_components
from scipy.ndimage import binary_fill_holes


def load_and_covnert_case(input_image: str, input_seg: str, output_image: str, output_seg: str,
                          min_component_size: int = 50):
    # 加载输入图像和分割图
    seg = io.imread(input_seg)
    seg[seg == 255] = 1
    image = io.imread(input_image)
    # 将3通道图像压缩到2D
    # 如果是灰度图像，则无需进行压缩操作
    if len(image.shape) == 3:
        image = image.sum(2)

    # 创建一个掩码，用于处理图像中没有信息但可能存在道路分割的白色区域
    mask = image == (3 * 255)

    # 使用自定义过滤函数来移除掩码中的小组件（默认最小大小为50）
    mask = generic_filter_components(mask, filter_fn=lambda ids, sizes: [i for j, i in enumerate(ids) if
                                                                         sizes[j] > min_component_size])

    # 填充掩码中的孔洞
    mask = binary_fill_holes(mask)

    # 在掩码区域将分割图设为0
    seg[mask] = 0

    # 保存输出分割图
    io.imsave(output_seg, seg, check_contrast=False)

    # 复制输入图像到输出路径
    shutil.copy(input_image, output_image)


if __name__ == "__main__":
    # 源数据集路径
    source = r'F:\DATA\blood-vessel-segmentation'

    dataset_name = 'Dataset001_BloodVessel_2D'

    # 输出图像和分割图路径
    imagestr = join(nnUNet_raw, dataset_name, 'imagesTr')
    imagests = join(nnUNet_raw, dataset_name, 'imagesTs')
    labelstr = join(nnUNet_raw, dataset_name, 'labelsTr')
    labelsts = join(nnUNet_raw, dataset_name, 'labelsTs')

    # 创建必要的文件夹
    maybe_mkdir_p(imagestr)
    maybe_mkdir_p(imagests)
    maybe_mkdir_p(labelstr)
    maybe_mkdir_p(labelsts)

    # 训练集和测试集源路径
    train_source = join(source, 'train')
    test_source = join(source, 'test')

    # 使用多进程池进行并行处理
    with multiprocessing.get_context("spawn").Pool(8) as p:

        # 获取训练集中有效的分割图ID
        valid_ids = subfiles(join(train_source, 'output'), join=False, suffix='tif')
        num_train = len(valid_ids)

        # 启动多进程任务
        r = []
        for v in valid_ids:
            r.append(
                p.starmap_async(
                    load_and_covnert_case,
                    ((
                         join(train_source, 'input', v),
                         join(train_source, 'output', v),
                         join(imagestr, v[:-4] + '_0000.tif'),
                         join(labelstr, v),
                         50
                     ),)
                )
            )

        # 对测试集执行相同的操作
        valid_ids = subfiles(join(test_source, 'output'), join=False, suffix='tif')
        for v in valid_ids:
            r.append(
                p.starmap_async(
                    load_and_covnert_case,
                    ((
                         join(test_source, 'input', v),
                         join(test_source, 'output', v),
                         join(imagests, v[:-4] + '_0000.tif'),
                         join(labelsts, v),
                         50
                     ),)
                )
            )

        # 等待所有任务完成
        _ = [i.get() for i in r]

    # 生成JSON配置文件
    # 因为只有一个通道，所以修改三通道channel_names为单通道灰度
    generate_dataset_json(join(nnUNet_raw, dataset_name), {0: 'Grey'}, {'background': 0, 'vessel': 1},
                          num_train, '.tif', dataset_name=dataset_name)

