# 运行记录
conda create -n BloodVessel python=3.9(不加python则会导致该虚拟环境中初始没有pip导致后续使用pip会将指定包安装到base环境中，不指定版本会导致python版本过高和torch版本不适配) 
activate BloodVessel  
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 
cd NnunetBloodVessel  
pip install -e .    
pip install --upgrade git+https://github.com/FabianIsensee/hiddenlayer.git  
# idea
使用git开发  
参照Dataset120_RoadSegmentation按2D数据训练看看效果 
# date_log
## 12.5周二
因为BloodVessel中test数据集数量过少，所以使用kidney2（另一个供体的肾脏整体作为test）    
要先设置nnUNet_raw、nnUNet_preprocessed、nnUNet_results文件夹和相应的环境变量，为了方便也放在项目根目录外面    
临时环境变量设置方法：    
set nnUNet_raw=F:\DATA\NnunetBloodVessel\nnUNet_raw   
set nnUNet_preprocessed=F:\DATA\NnunetBloodVessel\nnUNet_preprocessed   
set nnUNet_results=F:\DATA\NnunetBloodVessel\nnUNet_results   
文件名命名为“Dataset001_BloodVessel_2D”。  
为了使用Dataset120_RoadSegmentation预处理流程，要给每个肾脏内数据加前缀，建立temporary临时存放文件夹。预预处理文件为pre_Dataset001_BloodVessel_2D.py      
将环境变量设置到了pycharm中。添加到项目根目录中的环境变量无法在子文件中使用，改为在运行当前文件中修改配置环境变量，成功。  
`上句方式运行采用右键运行时可用，若使用nnUNetv2_plan_and_preprocess进行预处理，则要在设置->工具->终端->环境变量中设置，则环境变量在终端可见`  
使用Dataset120_RoadSegmentation模板，但是该文件为三通道，所以计算images.sum(2)将三通道压缩为二通道要取消，同时生成json文件部分通道数量修改。    
使用pre_Dataset001_BloodVessel_2D.py给各肾脏数据加前缀并转移到固定文件夹  
使用latter_Dataset001_BloodVessel_2D.py划分训练集和验证集  
`Dataset001_BloodVessel_2D.py运行成功填充nnUNet_raw`  
entry_points.txt中存放的是终端运行命令对应的模块  
nnUNetv2_plan_and_preprocess -d 1 --verify_dataset_integrity